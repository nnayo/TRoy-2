#include "drivers/twi.h"
#include "avr/io.h"
#include "avr/interrupt.h"

#include "avr_mcu_section.h"

AVR_MCU(16000000, "atmega328p");

const struct avr_mmcu_vcd_trace_t simavr_conf[]  _MMCU_ = {
	{ AVR_MCU_VCD_SYMBOL("TWDR"), .what = (void*)&TWDR, },
	{ AVR_MCU_VCD_SYMBOL("TWSR"), .what = (void*)&TWSR, },
	{ AVR_MCU_VCD_SYMBOL("TWCR"), .what = (void*)&TWCR, },
	{ AVR_MCU_VCD_SYMBOL("TWAR"), .what = (void*)&TWAR, },
};


u8 data[] = {0x07, 0x17};
u8 len = sizeof(data) / sizeof(data[0]);

volatile u8 done;

void call_back(twi_state_t state, u8 nb_data, void* misc)
{
	switch (state) {
	case TWI_SL_RX_BEGIN:
	case TWI_GENCALL_BEGIN:
		TWI_sl_rx(len, data);
		break;

	case TWI_SL_RX_END:
	case TWI_GENCALL_END:
		for (u8 i = 0; i < len; i++) {
			data[i] += 0x20;
		}
		break;

	case TWI_SL_TX_BEGIN:
		TWI_sl_tx(len, data);
		break;

	case TWI_SL_TX_END:
		for (u8 i = 0; i < len; i++) {
			data[i] += 0x02;
		}
		break;

	case TWI_NO_SL:
		TWI_stop();
		break;

	case TWI_MS_TX_END:
		TWI_stop();

		for (u8 i = 0; i < len; i++) {
			data[i] += 0x30;
		}	

		break;

	case TWI_MS_RX_END:
		TWI_stop();

		for (u8 i = 0; i < len; i++) {
			data[i] += 0x01;
		}	

		break;

	case TWI_IDLE:
		done = 1;
		break;

	default:
		break;
	}
}


// test cases
#define _RX 1
#define _TX 0
#define _GC 0

// master rx
void master_rx(void)
{
#if _RX >= 1
	done = 0;
	while (KO == TWI_ms_rx(0x47, len, data))
		;
	while (!done)
		;
#endif

#if _RX >= 2
	done = 0;
	while (KO == TWI_ms_rx(0x11, len, data))
		;
	while (!done)
		;
#endif

}

// master tx
void master_tx(void)
{
#if _TX >= 1
	done = 0;
	while (KO == TWI_ms_tx(0x47, len, data))
		;
	while (!done)
		;
#endif

#if _TX >= 2
	done = 0;
	while (KO == TWI_ms_tx(0x11, len, data))
		;
	while (!done)
		;
#endif
}

// gen call
void gen_call(void)
{
#if _GC >= 1
	done = 0;
	while (KO == TWI_ms_tx(0x00, len, data))
		;
	while (!done)
		;
#endif

#if _GC >= 2
	done = 0;
	while (KO == TWI_ms_tx(0x00, len, data))
		;
	while (!done)
		;
#endif
}


void main(void)
{
	TWI_init(call_back, NULL);

	TWI_set_sl_addr(SLV_ADDR);

	TWI_gen_call(OK);

	sei();

	for (u8 i = 0; i < len; i++) {
		data[i] += SLV_ADDR;
	}

	// different start time upon the slave address
	//for (u32 i = 0; i < SLV_ADDR * 1000L; i++)
	//	;

#if SLV_ADDR == 0x11
	master_rx();
	master_tx();
	gen_call();
#endif

	while (1)
		;
}

