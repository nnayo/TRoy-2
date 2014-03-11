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


volatile u8 txed;

void call_back(twi_state_t state, u8 nb_data, void* misc)
{
    TWI_stop();
    txed = 1;
}


void main(void)
{
    TWI_init(call_back, NULL);

    TWI_set_sl_addr(0x7e);

    for (u16 i = 0; i < 1000; i++)
        ;

    u8 data[] = {0x07, 0x17};
    u8 len = sizeof(data);

    sei();

    txed = 0;

    while (1) {
        TWI_ms_tx(0x4e, len, data);
        while (!txed)
            ;
    }
}

