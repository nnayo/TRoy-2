import Part
from FreeCAD import Vector

from base_component import ElecComponent


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
    'len': 52.6 + 10., # mm
    'offset pile': 52.6 / 2 + 5., # mm
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

    arduino_data = {
        'x': 33. + 9., # mm (9 = rs connector)
        'y': 18., # mm
        'z': 2., # mm
    }

    ad = arduino_data
    # make arduino
    comp = Part.makeBox(ad['z'], ad['x'], ad['y'])
    comp.translate(Vector(-ad['z'] / 2, -ad['x'] / 2, -ad['y'] / 2))

    return comp


class Arduino(ElecComponent):
    """Arduino Pro mini"""
    def __init__(self, doc, name='arduino'):
        data = {
            'x': 2., # mm
            'y': 33. + 9., # mm (9 = rs connector)
            'z': 18., # mm
        }
        self.data = data
        col_box = {
            'x': 4., # mm
            'y': 31., # mm (9 = rs connector)
            'z': 16., # mm
        }
        self.col_box = col_box

        # make board
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'] + 10, col_box['z'] + 9.)   # 9 mm rs connector
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2, -col_box['z'] / 2 - 9))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


def connect_card():
    """make an connection card"""

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

    # make card
    comp = Part.makeBox(connect_card_data['z'], connect_card_data['x'], connect_card_data['y'])
    comp.translate(Vector(-connect_card_data['z'] / 2, -connect_card_data['x'] / 2, -connect_card_data['y'] / 2))

    # add connector
    connect = Part.makeBox(connector_data['z'], connector_data['x'], connector_data['y'])
    connect.translate(Vector(0, 0, connector_data['y'] / 2))

    comp = comp.fuse(connect)
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180)
    return comp


class ConnectCard(ElecComponent):
    """connection card"""
    def __init__(self, doc, name='connection_card'):
        data = {
            'x': 2., # mm
            'y': 64., # mm
            'z': 21., # mm
        }
        self.data = data
        col_box = {
            'x': 2., # mm
            'y': 62., # mm
            'z': 17., # mm
        }
        self.col_box = col_box

        # connector
        connector_data = {
            'x': 15., # mm
            'y': 20., # mm
            'z': 6., # mm
        }

        # make board
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        comp = comp.fuse(comp)

        # add connector
        connect = Part.makeBox(connector_data['x'], connector_data['y'], connector_data['z'])
        connect.translate(Vector(0, 0, connector_data['z'] / 2))
        comp = comp.fuse(connect)
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'] + 10, col_box['z'])
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


def mpu():
    """make a MPU card"""

    # MPU
    mpu_data = {
        'x': 20., # mm
        'y': 20., # mm
        'z': 2., # mm
    }

    # make card
    comp = Part.makeBox(mpu_data['x'], mpu_data['y'], mpu_data['z'])
    comp.translate(Vector(-mpu_data['x'] / 2, -mpu_data['y'] / 2, -mpu_data['z'] / 2))

    return comp


class Mpu(ElecComponent):
    """MPU board"""
    def __init__(self, doc, name='MPU'):
        data = {
            'x': 20., # mm
            'y': 20., # mm
            'z': 2., # mm
        }
        self.data = data
        col_box = {
            'x': 18., # mm
            'y': 18., # mm
            'z': 4., # mm
        }
        self.col_box = col_box

        # make board
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'])
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2 + 1, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


class Pile9V(ElecComponent):
    """pile 9V"""
    def __init__(self, doc, name='pile9V'):
        data = {
            'x': 25.5, # mm
            'y': 16.5, # mm
            'z': 52.6, # mm
        }
        self.data = data
        col_box = {
            'x': 25.5, # mm
            'y': 16.5, # mm
            'z': 52.6, # mm
        }
        self.col_box = col_box

        # make board
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'] + 2)
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.33, 1.))


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


def carte_regul():
    """carte regulation"""

    # make carte
    comp = Part.makeCylinder(carte_regul_data['r_ext'], carte_regul_data['z'])
    comp = comp.cut(Part.makeCylinder(carte_regul_data['r_int'], carte_regul_data['z']))

    return comp


