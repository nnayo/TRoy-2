#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>	// open()
#include <unistd.h>	// write()

#include "twi_bus.h"

#include "sim_avr.h"
#include "avr_twi.h"
#include "sim_elf.h"
#include "sim_gdb.h"
#include "sim_vcd_file.h"


typedef struct twi_link_t {
	avr_irq_t* in;
	avr_irq_t* out;
	avr_twi_msg_irq_t msg;
} twi_link_t;

typedef struct twi_bus_t {
	// complete bus connections
	struct twi_link_t** links;	// all connected links
	int nb_links;

	// dialog state
	struct twi_link_t* origin;	// origin link is the only one not having to response
	int resp_quota;
	int nb_resp;
	int gencall;
	int gencall_nack;
	int read_mode;

	// VCD tracing
	avr_vcd_t vcd;

	// TWI frame log
	int frame_log;
} twi_bus_t;

static char msg2chr[] = { '0', '[', '@', 'D', '+', '-', 'w', ']' };

#define RED_COLOR		"\x1b[91m"
#define PURPLE_COLOR	"\x1b[95m"
#define NORMAL_COLOR	"\x1b[0m"

static void twi_bus_trace(const char* fname, avr_twi_msg_irq_t msg, uint8_t addr, struct twi_bus_t* bus)
{
	printf("["RED_COLOR"%s"NORMAL_COLOR"] ", fname);

	if (msg.bus.msg == TWI_MSG_ADDR) {
		printf(PURPLE_COLOR"%c  0x%02x+%c"NORMAL_COLOR, msg2chr[msg.bus.msg], addr >> 1, (addr & 1) ? 'R' : 'W');
	}
	else {
		printf(PURPLE_COLOR"%c  0x%02x"NORMAL_COLOR, msg2chr[msg.bus.msg], addr);
	}

	printf("  org:%p, qt:%d rp:%d gc:%d gcn:%d (t=%d)\n", bus->origin, bus->resp_quota, bus->nb_resp, bus->gencall, bus->gencall_nack, (int)bus->vcd.avr->cycle);
}


static void twi_bus_frame_log(void* caller)
{
	char buf[64];

	switch (msg.bus.msg) {
	case TWI_MSG_START:
		write(twi_bus->frame_log, (const void *)&msg2chr[msg.bus.msg], 1);
		break;

	case TWI_MSG_ADDR:
		write(twi_bus->frame_log, (const void *)&msg2chr[msg.bus.msg], 1);
		snprintf(buf, sizeof(buf) - 1, "0x%02x", msg.bus.addr >> 1);
		write(twi_bus->frame_log, (const void *)buf, strlen(buf));
		if (msg.bus.addr & 0x01) {
			write(twi_bus->frame_log, (const void *)"R ", 2);
		}
		else {
			write(twi_bus->frame_log, (const void *)"W ", 2);
		}
		break;

	case TWI_MSG_DATA:
		write(twi_bus->frame_log, (const void *)&msg2chr[msg.bus.msg], 1);
		snprintf(buf, sizeof(buf) - 1, "0x%02x ", msg.bus.data);
		write(twi_bus->frame_log, (const void *)buf, strlen(buf));
		break;

	case TWI_MSG_STOP:
		write(twi_bus->frame_log, (const void *)&msg2chr[msg.bus.msg], 1);
		write(twi_bus->frame_log, (const void *)"\n", 1);
		break;
	}

}

// dispatch message to every nodes except sender
static void twi_bus_dispatch(struct twi_bus_t* twi_bus, avr_twi_msg_irq_t msg)
{
	twi_bus_trace(__func__, msg, twi_bus->origin->msg.bus.addr, twi_bus);

	for (int i = 0; i < twi_bus->nb_links; i++) {
		if (twi_bus->links[i] == twi_bus->origin) {
			continue;
		}
		avr_raise_irq(twi_bus->links[i]->out, msg.v);
	}
}

// arbitrate stored messages
static struct avr_twi_msg_irq_t twi_bus_arbitrate(struct twi_bus_t* twi_bus)
{
	avr_twi_msg_irq_t cmd_msg;
	avr_twi_msg_irq_t rsp_msg;
	avr_twi_msg_irq_t lnk_msg;

	twi_bus_trace(__func__, twi_bus->origin->msg, twi_bus->origin->msg.bus.addr, twi_bus);

	cmd_msg = twi_bus->origin->msg;

	switch (cmd_msg.bus.msg) {
	case TWI_MSG_START:
	case TWI_MSG_STOP:
	case TWI_MSG_ACK:
	case TWI_MSG_NACK:
	case TWI_MSG_NULL:
		rsp_msg.bus.msg = TWI_MSG_NULL;
		return rsp_msg;
		break;

	case TWI_MSG_ADDR:
	case TWI_MSG_DATA:
		rsp_msg.bus.msg = TWI_MSG_NACK;
		rsp_msg.bus.addr = cmd_msg.bus.addr;
		break;

	case TWI_MSG_CLK:
		rsp_msg.bus.msg = TWI_MSG_DATA;
		rsp_msg.bus.data = 0xff;
		break;
	}

	struct twi_link_t* origin = twi_bus->origin;
	for (int i = 0; i < twi_bus->nb_links; i++) {
		if (twi_bus->links[i] == origin) {
			continue;
		}

		// find the message with the max of 0
		lnk_msg = twi_bus->links[i]->msg;
		switch (cmd_msg.bus.msg) {
		case TWI_MSG_ADDR:
		case TWI_MSG_DATA:
			if (lnk_msg.bus.msg == TWI_MSG_ACK) {
				rsp_msg = lnk_msg;
				return rsp_msg;
			}
			break;

		case TWI_MSG_CLK:
			if (lnk_msg.bus.data < rsp_msg.bus.data) {
				rsp_msg.bus.data = lnk_msg.bus.data;
			}
		default:
			break;
		}
	}

	return rsp_msg;
}

// response message to origin only
static void twi_bus_response(struct twi_bus_t* twi_bus, avr_twi_msg_irq_t msg)
{
	twi_bus_trace(__func__, msg, msg.bus.addr, twi_bus);

	avr_raise_irq(twi_bus->origin->out, msg.v);
}

// store message with its sender
static void twi_bus_store(struct twi_bus_t* twi_bus, struct avr_irq_t* irq, avr_twi_msg_irq_t msg)
{
	twi_bus_trace(__func__, msg, msg.bus.addr, twi_bus);

	for (int i = 0; i < twi_bus->nb_links; i++) {
		if (twi_bus->links[i]->in == irq) {
			twi_bus->links[i]->msg = msg;
			twi_bus->nb_resp++;
			break;
		}
	}

	if (twi_bus->origin->msg.bus.msg == TWI_MSG_ADDR && twi_bus->gencall && msg.bus.msg == TWI_MSG_NACK) {
		twi_bus->gencall_nack++;
		twi_bus->nb_resp--;
	}

	// enough responses ?
	if (twi_bus->nb_resp == twi_bus->resp_quota - twi_bus->gencall_nack) {
		// arbitrate responses and send the best
		msg = twi_bus_arbitrate(twi_bus);
		twi_bus_response(twi_bus, msg);
	}
}

// twi bus logic: where messages are dispatched and arbritration is done
static void twi_bus_logic(struct avr_irq_t* irq, uint32_t value, void* param)
{
	struct twi_bus_t* twi_bus = (struct twi_bus_t*)param;

	avr_twi_msg_irq_t msg;
	msg.v = value;

	twi_bus_trace(__func__, msg, msg.bus.addr, twi_bus);

	// waiting response(s) ?
	if (twi_bus->nb_resp < twi_bus->resp_quota - twi_bus->gencall_nack) {
		// store message
		twi_bus_store(twi_bus, irq, msg);
		return;
	}

	// new exchange
	twi_bus->nb_resp = 0;
	// find associated link and save it
	for (int i = 0; i < twi_bus->nb_links; i++) {
		if (twi_bus->links[i]->in == irq) {
			twi_bus->origin = twi_bus->links[i];
			twi_bus->origin->msg = msg;
			break;
		}
	}

	// set conditions for response
	switch (msg.bus.msg) {
	case TWI_MSG_START:
		twi_bus->read_mode = 1;
	case TWI_MSG_STOP:
		twi_bus->gencall = 0;
		twi_bus->gencall_nack = 0;
	case TWI_MSG_ACK:
	case TWI_MSG_NACK:
	case TWI_MSG_NULL:
		twi_bus->resp_quota = 0;
		break;

	case TWI_MSG_DATA:
	case TWI_MSG_CLK:
		twi_bus->resp_quota = twi_bus->gencall ? twi_bus->nb_links - 1 : 1;
		break;

	case TWI_MSG_ADDR:
		twi_bus->gencall = (msg.bus.addr == 0x00) ? 1 : 0;
		twi_bus->resp_quota = twi_bus->nb_links - 1;
		break;
	}

	// forward to other nodes
	twi_bus_dispatch(twi_bus, msg);
}


struct twi_bus_t* twi_bus_alloc(avr_t** cores, int nb_cores)
{
	struct twi_bus_t* twi_bus;

	twi_bus = (struct twi_bus_t*)malloc(sizeof(struct twi_bus_t));
	memset(twi_bus, 0, sizeof(struct twi_bus_t));
	twi_bus->links = (struct twi_link_t**)malloc(nb_cores * sizeof(struct twi_link_t*));

	avr_vcd_init(cores[0], "twi_bus.vcd", &twi_bus->vcd, 100);

	twi_bus->frame_log = open("twi_frame.log", O_WRONLY | O_CREAT | O_SYNC | O_TRUNC);

	// save connection core out irq to bus in irq
	// save connection core in irq to bus out irq
	// monitor core out irq
	avr_irq_t* core_out_irq;
	avr_irq_t* core_in_irq;
	avr_twi_msg_irq_t msg = avr_twi_irq_msg(TWI_MSG_NULL, 0);
	char name[64];

	for (int i = 0; i < nb_cores; i++) {
		core_out_irq = avr_io_getirq(cores[i], AVR_IOCTL_TWI_GETIRQ(0), TWI_IRQ_OUTPUT);
		core_in_irq = avr_io_getirq(cores[i], AVR_IOCTL_TWI_GETIRQ(0), TWI_IRQ_INPUT);

		struct twi_link_t* link = (struct twi_link_t*)malloc(sizeof(struct twi_link_t));
		twi_bus->links[i] = link;
		twi_bus->links[i]->in = core_out_irq;
		twi_bus->links[i]->out = core_in_irq;
		twi_bus->links[i]->msg = msg;

		avr_irq_register_notify(core_out_irq, twi_bus_logic, twi_bus);
		sprintf(name, "core[%d]", i);
		avr_vcd_add_signal(&twi_bus->vcd, core_out_irq, 8, name);
	}

	twi_bus->nb_links = nb_cores;

	avr_vcd_start(&twi_bus->vcd);

	return twi_bus;
}


void twi_bus_free(twi_bus_t* twi_bus)
{
	avr_vcd_stop(&twi_bus->vcd);

	for (int i = 0; i < twi_bus->nb_links; i++) {
		free(twi_bus->links[i]);
	}

	free(twi_bus->links);
	free(twi_bus);
}


