
LIBS = $(TROLL_PROJECTS)/simavr/simavr/obj-x86_64-redhat-linux/libsimavr.so.1

CFLAGS = -g -I$(TROLL_PROJECTS)/simavr/simavr/sim -std=c99 -Wall -Wextra
LDFLAGS = $(TROLL_PROJECTS)/simavr/libsimavr.a -lelf


all:	TRoy_2_sim minut_0.elf minut_1.elf minut_2.elf xbee.elf sd_0.elf sd_1.elf


TRoy_2_sim: TRoy_2_sim.o
	$(CC) TRoy_2_sim.o $(LDFLAGS) -o TRoy_2_sim


TRoy_2_sim.o: TRoy_2_sim.c


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


test: TRoy_2_sim rxer.elf txer.elf
	$(CC) $(CFLAGS) -DDEBUG -c TRoy_2_sim.c -o TRoy_2_sim.o
	$(CC) TRoy_2_sim.o $(LDFLAGS) -o TRoy_2_sim

rxer.elf: rxer.o
	avr-gcc rxer.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o rxer.elf

rxer.o: rxer.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -g -std=c99 -mmcu=atmega328p -c rxer.c -o rxer.o

txer.elf: txer.o
	avr-gcc txer.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o txer.elf

txer.o: txer.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -std=c99 -mmcu=atmega328p -c txer.c -o txer.o


clean:
	rm -f TRoy_2_sim *.o *.elf *.vcd
