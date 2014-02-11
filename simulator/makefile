
LIBS = $(TROLL_PROJECTS)/simavr/simavr/obj-x86_64-redhat-linux/libsimavr.so.1

CFLAGS = -g -I$(TROLL_PROJECTS)/simavr/simavr/sim -std=c99 -Wall -Wextra
LDFLAGS = $(TROLL_PROJECTS)/simavr/libsimavr.a -lelf


all:	sim_TRoy_2 minut_0.elf minut_1.elf minut_2.elf xbee.elf sd_0.elf sd_1.elf


sim_TRoy_2: sim_TRoy_2.o
	$(CC) sim_TRoy_2.o $(LDFLAGS) -o sim_TRoy_2


sim_TRoy_2.o: sim_TRoy_2.c


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


test: sim_TRoy_2 rxer.elf txer.elf
	$(CC) $(CFLAGS) -DDEBUG -c sim_TRoy_2.c -o sim_TRoy_2.o
	$(CC) sim_TRoy_2.o $(LDFLAGS) -o sim_TRoy_2

rxer.elf: rxer.o
	avr-gcc rxer.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o rxer.elf

rxer.o: rxer.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -g -std=c99 -mmcu=atmega328p -c rxer.c -o rxer.o

txer.elf: txer.o
	avr-gcc txer.o -L$(TROLL_PROJECTS)/nanoK -lnanoK -g -mmcu=atmega328p -Wl,--undefined=_mmcu,--section-start=.mmcu=0x8000 -o txer.elf

txer.o: txer.c
	avr-gcc -I$(TROLL_PROJECTS)/simavr/simavr/sim/avr -I$(TROLL_PROJECTS)/nanoK -std=c99 -mmcu=atmega328p -c txer.c -o txer.o


clean:
	rm -f sim_TRoy_2 *.o *.elf *.vcd
