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
	switch(state) {
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
		TWI_stop();
		break;
	}
}


void main(void)
{
    TWI_init(call_back, NULL);

    TWI_set_sl_addr(0x7e);

    for (u16 i = 0; i < 1000; i++)
        ;

    sei();

#define _RX 2
#define _TX 2
#define _GC 2

	// master rx
#if _RX >= 1
    done = 0;
	while (KO == TWI_ms_rx(0x47, len, data))
		;
	while (!done)
		;
#endif

	// master tx
#if _TX >= 1
    done = 0;
	while (KO == TWI_ms_tx(0x47, len, data))
		;
	while (!done)
		;
#endif

	// gen call
#if _GC >= 1
    done = 0;
	while (KO == TWI_ms_tx(0x00, len, data))
		;
	while (!done)
		;
#endif

	// master rx
#if _RX >= 2
    done = 0;
	while (KO == TWI_ms_rx(0x4e, len, data))
		;
	while (!done)
		;
#endif

	// master tx
#if _TX >= 2
    done = 0;
	while (KO == TWI_ms_tx(0x4e, len, data))
		;
	while (!done)
		;
#endif

	// gen call
#if _GC >= 2
    done = 0;
	while (KO == TWI_ms_tx(0x00, len, data))
		;
	while (!done)
		;
#endif

}

