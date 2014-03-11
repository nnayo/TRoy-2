
CFLAGS = -g -I$(TROLL_PROJECTS)/simavr/simavr/sim -I. -std=c99 -Wall -Wextra
LDFLAGS = $(TROLL_PROJECTS)/simavr/libsimavr.a -lelf


all:	sim_TRoy_2 minut_0.elf minut_1.elf minut_2.elf xbee.elf sd_0.elf sd_1.elf



sim_TRoy_2: sim_TRoy_2.o twi_bus.o mpu6050.o sc18is600.o $(TROLL_PROJECTS)/simavr/libsimavr.a
	$(CC) sim_TRoy_2.o twi_bus.o mpu6050.o sc18is600.o $(LDFLAGS) -o sim_TRoy_2

sim_TRoy_2.o: sim_TRoy_2.c
	$(CC) $(CFLAGS) -c sim_TRoy_2.c -o sim_TRoy_2.o

mpu6050.o: mpu6050.c mpu6050.h sc18is600.h
sc18is600.o: sc18is600.c sc18is600.h


minut_0.elf:
	ln -s ../soft/minut_0.elf minut_0.elf

minut_1.elf:
	ln -s ../soft/minut_1.elf minut_1.elf

minut_2.elf:
	ln -s ../soft/minut_2.elf minut_2.elf

xbee.elf:
	ln -s ../soft/xbee.elf xbee.elf

sd_0.elf:
	ln -s ../soft/sd_0.elf sd_0.elf

sd_1.elf:
	ln -s ../soft/sd_1.elf sd_1.elf


test: sim_TRoy_2 slv_11.elf slv_2e.elf slv_47.elf
	$(CC) $(CFLAGS) -DTEST -c sim_TRoy_2.c -o sim_TRoy_2.o

slv_47.elf: slv_47.o $(TROLL_PROJECTS)/nanoK/libnanoK.a
	avr-gcc slv_47.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o slv_47.elf

slv_47.o: slv.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -g -o0 -std=c99 -mmcu=atmega328p -fshort-enums -mcall-prologues -c slv.c -o slv_47.o -DSLV_ADDR=0x47

slv_2e.elf: slv_2e.o $(TROLL_PROJECTS)/nanoK/libnanoK.a
	avr-gcc slv_2e.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o slv_2e.elf

slv_2e.o: slv.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -g -o0 -std=c99 -mmcu=atmega328p -fshort-enums -mcall-prologues -c slv.c -o slv_2e.o -DSLV_ADDR=0x2e

slv_11.elf: slv_11.o $(TROLL_PROJECTS)/nanoK/libnanoK.a
	avr-gcc slv_11.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o slv_11.elf

slv_11.o: slv.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -g -o0 -std=c99 -mmcu=atmega328p -fshort-enums -mcall-prologues -c slv.c -o slv_11.o -DSLV_ADDR=0x11


clean:
	rm -f sim_TRoy_2 *.o *.elf *.vcd *~ *.lix
