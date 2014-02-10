#include "drivers/twi.h"
#include "avr/io.h"

#include "avr_mcu_section.h"

AVR_MCU(16000000, "atmega328p");

const struct avr_mmcu_vcd_trace_t simavr_conf[]  _MMCU_ = {
    { AVR_MCU_VCD_SYMBOL("TWDR"), .what = (void*)&TWDR, },
    { AVR_MCU_VCD_SYMBOL("TWSR"), .what = (void*)&TWSR, },
    { AVR_MCU_VCD_SYMBOL("TWCR"), .what = (void*)&TWCR, },
    { AVR_MCU_VCD_SYMBOL("TWAR"), .what = (void*)&TWAR, },
};


u8 len;
u8 data[10];

void call_back(twi_state_t state, u8 nb_data, void* misc)
{
}


void main(void)
{
    TWI_init(call_back, NULL);

    TWI_set_sl_addr(0x4e);

    while (1) {
    }
}

