
LIBS = $(TROLL_PROJECTS)/simavr/simavr/obj-x86_64-redhat-linux/libsimavr.so.1

CFLAGS = -g -I$(TROLL_PROJECTS)/simavr/simavr/sim -std=c99 -Wall -Wextra
LDFLAGS = $(TROLL_PROJECTS)/simavr/simavr/obj-x86_64-linux-gnu/libsimavr.a -lelf

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


clean:
	rm -f TRoy_2_sim TRoy_2_sim.o *.elf *.vcd
