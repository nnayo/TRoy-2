EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:sc18is600
LIBS:tlv1117
LIBS:tps2110
LIBS:TRoy 2-cache
EELAYER 24 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 6 14
Title ""
Date "28 oct 2013"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
NoConn ~ 4400 4750
Connection ~ 6850 4950
Wire Wire Line
	6850 4000 7800 4000
Wire Wire Line
	6850 4000 6850 5250
Wire Wire Line
	6850 4950 6700 4950
Wire Wire Line
	7800 3700 6700 3700
Wire Wire Line
	7800 3500 6700 3500
Wire Wire Line
	4400 3300 4600 3300
Wire Wire Line
	4600 3300 4600 2700
Wire Wire Line
	6700 3050 6850 3050
Wire Wire Line
	6850 3050 6850 2700
Wire Wire Line
	6850 2700 4600 2700
Wire Wire Line
	4600 4950 4600 5250
Wire Wire Line
	4600 4950 4400 4950
Wire Wire Line
	4400 4250 5600 4250
Wire Wire Line
	4400 3800 5600 3800
Wire Wire Line
	5600 3600 4400 3600
Wire Bus Line
	5600 3000 5500 3000
Wire Bus Line
	5500 3000 5500 1850
Wire Bus Line
	5500 1850 5300 1850
Wire Wire Line
	4400 3500 5600 3500
Wire Wire Line
	4400 3700 5600 3700
Wire Wire Line
	5600 4150 4400 4150
Wire Wire Line
	4400 4750 5600 4750
Wire Wire Line
	4600 5250 6850 5250
Wire Wire Line
	6700 3600 7800 3600
Wire Wire Line
	6700 3800 7800 3800
Wire Wire Line
	6750 3200 6850 3200
Wire Wire Line
	6850 3200 6850 3300
Wire Wire Line
	6850 3300 7800 3300
Text Label 7800 4000 0    60   ~ 0
Xbee gnd
Text Label 7800 3800 0    60   ~ 0
Xbee cs/
Text Label 7800 3700 0    60   ~ 0
Xbee sclk
Text Label 7800 3600 0    60   ~ 0
Xbee miso
Text Label 7800 3500 0    60   ~ 0
Xbee mosi
Text Label 7800 3300 0    60   ~ 0
Xbee +3.3V
Text Label 4400 4950 2    60   ~ 0
Arduino gnd
Text Label 4400 4250 2    60   ~ 0
Arduino sda A4
Text Label 4400 4150 2    60   ~ 0
Arduino scl A5
Text Label 4400 3800 2    60   ~ 0
Arduino cs/ D10
Text Label 4400 3700 2    60   ~ 0
Arduino sclk
Text Label 4400 3600 2    60   ~ 0
Arduino miso
Text Label 4400 3500 2    60   ~ 0
Arduino mosi
Text Label 4400 3300 2    60   ~ 0
Arduino Vcc
Text HLabel 5300 1850 0    60   BiDi ~ 0
bus
$Sheet
S 5600 2900 1100 2150
U 52333F2E
F0 "interface" 60
F1 "interface.sch" 60
F2 "bus" B L 5600 3000 60 
F3 "cmd servo" I L 5600 4750 60 
F4 "sda" B L 5600 4250 60 
F5 "scl" B L 5600 4150 60 
F6 "scl ext" B R 6700 4150 60 
F7 "sda ext" B R 6700 4250 60 
F8 "miso" O L 5600 3600 60 
F9 "sclk 3.3V" O R 6700 3700 60 
F10 "cs/ 3.3V" O R 6700 3800 60 
F11 "mosi 3.3V" O R 6700 3500 60 
F12 "cs/" I L 5600 3800 60 
F13 "sclk" I L 5600 3700 60 
F14 "mosi" I L 5600 3500 60 
F15 "miso 3.3V" I R 6700 3600 60 
F16 "GND" U R 6700 4950 60 
F17 "+5V" U R 6700 3050 60 
F18 "+3.3V" U R 6700 3200 60 
$EndSheet
$EndSCHEMATC
