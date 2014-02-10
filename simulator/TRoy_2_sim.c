#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "sim_avr.h"
#include "avr_twi.h"
#include "sim_elf.h"
#include "sim_gdb.h"


static avr_t* avr_setup(const char* fname, char* vcd_filename, int gdb, int gdb_port)
{
	printf("loading %s...\n", fname);

    elf_firmware_t f;
	elf_read_firmware(fname, &f);
	printf("firmware %s f=%d mmcu=%s\n", fname, (int)f.frequency, f.mmcu);
    strcpy(f.tracename, vcd_filename);

    avr_t * avr = NULL;
	avr = avr_make_mcu_by_name(f.mmcu);
	if (!avr) {
		fprintf(stderr, "AVR '%s' not known\n", f.mmcu);
		exit(1);
	}
	avr_init(avr);
	avr_load_firmware(avr, &f);

    if (gdb) {
        avr->gdb_port = gdb_port;
        avr_gdb_init(avr);
    }

    return avr;
}

static void i2c_bus_connect(avr_t** cores, int nb_cores)
{
    avr_t* core_src;
    avr_t* core_dst;

    for (int i = 0; i < nb_cores; i++) {
        core_src = cores[i];
        avr_irq_t* irq_src = avr_io_getirq(core_src, AVR_IOCTL_TWI_GETIRQ(0), TWI_IRQ_OUTPUT);

        for (int j = 0; j < nb_cores; j++) {
            core_dst = cores[j];

            if (core_src == core_dst) {
                continue;
            }

            avr_irq_t* irq_dst = avr_io_getirq(core_dst, AVR_IOCTL_TWI_GETIRQ(0), TWI_IRQ_INPUT);
            avr_connect_irq(irq_src, irq_dst);
        }
    }
}


int main(void)
{
    // set every core
#ifndef DEBUG 
    int gdb = 0;
    avr_t* minut_0 = avr_setup("minut_0.elf", "minut_0.vcd", gdb, 7000);
    avr_t* minut_1 = avr_setup("minut_1.elf", "minut_1.vcd", gdb, 7001);
    avr_t* minut_2 = avr_setup("minut_2.elf", "minut_2.vcd", gdb, 7002);
    avr_t* xbee = avr_setup("xbee.elf", "xbee.vcd", gdb, 7010);
    avr_t* sd_0 = avr_setup("sd_0.elf", "sd_0.vcd", gdb, 7020);
    avr_t* sd_1 = avr_setup("sd_1.elf", "sd_1.vcd", gdb, 7021);

    avr_t* cores[] = { minut_0, minut_1, minut_2, xbee, sd_0, sd_1 };

#else
    avr_t* txer = avr_setup("txer.elf", "txer.vcd", 1, 7020);
    avr_t* rxer = avr_setup("rxer.elf", "rxer.vcd", 1, 7021);

    avr_t* cores[] = { txer, rxer, };
#endif

    i2c_bus_connect(cores, sizeof(cores) / sizeof(cores[0]));

	printf( "\nTRoy_2 simulation launched\n");

    avr_cycle_count_t higher_cycle = 1;
    avr_cycle_count_t higher_cycle_display_trigger = 1e6;
	int state;

	while (1) {
        // avr->cycle fields of all cores shall be kept as close as possible
        for (unsigned int i = 0; i < sizeof(cores) / sizeof(cores[0]); i++) {
            // if the core is in advance, don't run it
            if (cores[i]->cycle > higher_cycle)
                continue;

            // run the core for 1 cycle and check if in error
            state = avr_run(cores[i]);
            if ((state == cpu_Done) || (state == cpu_Crashed)) {
                break;
            }
        }

        // update higher cycle
        for (unsigned int i = 0; i < sizeof(cores) / sizeof(cores[0]); i++) {
            if (cores[i]->cycle > higher_cycle) {
                higher_cycle = cores[i]->cycle;
            }
        }

        // refresh higher cycle display 
        if ( higher_cycle >= higher_cycle_display_trigger) {
            printf("cycle = %10ld (%9ld s)\n", (long)higher_cycle, (long)(higher_cycle / 16e6));
            higher_cycle_display_trigger += 1e6;
        }
    }

    // stop cleanly
#ifndef DEBUG 
    avr_terminate(minut_0);
    avr_terminate(minut_1);
    avr_terminate(minut_2);
    avr_terminate(xbee);
    avr_terminate(sd_0);
    avr_terminate(sd_1);

#else
    avr_terminate(rxer);
    avr_terminate(txer);

#endif
}
