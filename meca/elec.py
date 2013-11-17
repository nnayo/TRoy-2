import Part
from FreeCAD import Vector

# arduino
arduino_data = {
    'x': 33. + 9., # mm (9 = rs connector)
    'y': 18., # mm
    'z': 2., # mm
}

# connection card
connect_card_data = {
    'x': 64., # mm
    'y': 21., # mm
    'z': 3., # mm
}

# connector
connector_data = {
    'x': 20., # mm
    'y': 6., # mm
    'z': 15., # mm
}

# MPU
mpu_data = {
    'x': 20., # mm
    'y': 20., # mm
    'z': 2., # mm
}

# ZigBee
zbee_data = {
    'x': 34., # mm
    'y': 22., # mm
    'z': 3., # mm
}

# carte SD
sd_card_data = {
    'x': 32., # mm
    'y': 24., # mm
    'z': 2., # mm
}

# pile 9V
pile_9v_data = {
    'x': 25.5, # mm
    'y': 16.5, # mm
    'z': 52.6, # mm
}

# carte puissance
carte_regul_data = {
    'r_ext': 30., # mm
    'r_int': 15., # mm
    'z': 5., # mm
}

# zones
minut_zone_data = {
    'len': 60., # mm
    'offset': 15., # mm
}

regul_zone_data = {
    'len': pile_9v_data['z'] + 10., # mm
    'offset pile': pile_9v_data['z'] / 2 + 5., # mm
    'offset carte': 45., # mm
}

hi_storage_zone_data = {
    'len': 40., # mm
    'offset': 10., # mm
}

hf_zone_data = {
    'len': 40., # mm
    'offset': 20., # mm
}

lo_storage_zone_data = {
    'len': 40., # mm
    'offset': 10., # mm
}


def arduino():
    """make an Arduino Pro mini"""

    ad = arduino_data
    # make arduino
    comp = Part.makeBox(ad['z'], ad['x'], ad['y'])
    comp.translate(Vector(-ad['z'] / 2, -ad['x'] / 2, -ad['y'] / 2))

    return comp


def connect_card():
    """make an connection card"""

    # make card
    comp = Part.makeBox(connect_card_data['z'], connect_card_data['x'], connect_card_data['y'])
    comp.translate(Vector(-connect_card_data['z'] / 2, -connect_card_data['x'] / 2, -connect_card_data['y'] / 2))

    # add connector
    connect = Part.makeBox(connector_data['z'], connector_data['x'], connector_data['y'])
    connect.translate(Vector(0, 0, connector_data['y'] / 2))

    comp = comp.fuse(connect)
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180)
    return comp


def mpu():
    """make a MPU card"""

    # make card
    comp = Part.makeBox(mpu_data['x'], mpu_data['y'], mpu_data['z'])
    comp.translate(Vector(-mpu_data['x'] / 2, -mpu_data['y'] / 2, -mpu_data['z'] / 2))

    return comp


def zigbee():
    """make a ZigBee card"""

    # make card
    comp = Part.makeBox(zbee_data['x'], zbee_data['y'], zbee_data['z'])
    comp.translate(Vector(-zbee_data['x'] / 2, -zbee_data['y'] / 2, -zbee_data['z'] / 2))

    return comp


def sd_card():
    """make a SD card"""

    # make card
    comp = Part.makeBox(sd_card_data['z'], sd_card_data['x'], sd_card_data['y'])
    comp.translate(Vector(-sd_card_data['z'] / 2, -sd_card_data['x'] / 2, -sd_card_data['y'] / 2))

    return comp


def pile_9v():
    """make a 9V pile"""

    # make pile
    comp = Part.makeBox(pile_9v_data['x'], pile_9v_data['y'], pile_9v_data['z'])
    comp.translate(Vector(-pile_9v_data['x'] / 2, -pile_9v_data['y'] / 2, -pile_9v_data['z'] / 2))

    return comp


def carte_regul():
    """carte regulation"""

    # make carte
    comp = Part.makeCylinder(carte_regul_data['r_ext'], carte_regul_data['z'])
    comp = comp.cut(Part.makeCylinder(carte_regul_data['r_int'], carte_regul_data['z']))

    return comp


