"""
generate the eeprom image for TRoy 2 minuterie frames
"""


from frame import *


I2C_SELF_ADDR = Frame.I2C_SELF_ADDR
T_ID = Frame.T_ID
CMD = Frame.CMD


# slots number
slots_nb = 2

slots = [
	#--------------------------------
	# slot #0 : reset
	[
		# wait to allow DNA master to start 0x07d0 = 2000 ms
		wait(I2C_SELF_ADDR, I2C_SELF_ADDR, T_ID, CMD, 0x07, 0xd0),

		# send application start signal
		appli_start(I2C_SELF_ADDR, I2C_SELF_ADDR, T_ID, CMD),
	],

	#--------------------------------
	# slot #1 : spare
	[
		no_cmde(I2C_SELF_ADDR, I2C_SELF_ADDR, T_ID, CMD),
	],
]

