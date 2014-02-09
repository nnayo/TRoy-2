#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "sim_avr.h"
#include "avr_twi.h"
#include "sim_elf.h"
#include "sim_gdb.h"


static avr_t* avr_setup(const char* fname, char* vcd_filename, int gdb_port)
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

    avr->gdb_port = gdb_port;
    //avr_gdb_init(avr);

    return avr;
}

int main(void)
{
    // I2C bus
    avr_irq_t * i2c_irq;

    // set every core
    avr_t* minut_0 = avr_setup("minut_0.elf", "minut_0.vcd", 7000);
    avr_t* minut_1 = avr_setup("minut_1.elf", "minut_1.vcd", 7001);
    avr_t* minut_2 = avr_setup("minut_2.elf", "minut_2.vcd", 7002);
    avr_t* xbee = avr_setup("xbee.elf", "xbee.vcd", 7010);
    avr_t* sd_0 = avr_setup("sd_0.elf", "sd_0.vcd", 7020);
    avr_t* sd_1 = avr_setup("sd_1.elf", "sd_1.vcd", 7021);

    avr_t* cores[] = { minut_0, minut_1, minut_2, xbee, sd_0, sd_1 };

	printf( "\nTRoy_2 simulation launched\n");

    avr_cycle_count_t higher_cycle = 1;
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
    }

    // stop cleanly
    avr_terminate(minut_0);
    avr_terminate(minut_1);
    avr_terminate(minut_2);
    avr_terminate(xbee);
    avr_terminate(sd_0);
    avr_terminate(sd_1);
}
