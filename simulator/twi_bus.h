#ifndef __TWI_BUS_H__
# define __TWI_BUS_H__

#include "sim_avr.h"


// create a TWI bus
struct twi_bus_t* twi_bus_alloc(avr_t** cores, int nb_cores);


// release the TWI bus
void twi_bus_free(struct twi_bus_t* twi_bus);


#endif	// __TWI_BUS_H__
