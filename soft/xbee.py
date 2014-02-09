"""
generate the eeprom image for TRoy 2 xbee frames
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
		# send application start signal
		appli_start(I2C_SELF_ADDR, I2C_SELF_ADDR, T_ID, CMD),
	],

	#--------------------------------
	# slot #1 : spare
	[
		no_cmde(I2C_SELF_ADDR, I2C_SELF_ADDR, T_ID, CMD),
	],
]

