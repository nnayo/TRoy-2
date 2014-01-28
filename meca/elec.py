import Part
from FreeCAD import Vector

from base_component import ElecComponent


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
    'offset': 20., # mm
}

hf_zone_data = {
    'len': 40., # mm
    'offset': 20., # mm
}

lo_storage_zone_data = {
    'len': 40., # mm
    'offset': 20., # mm
}


class Arduino(ElecComponent):
    """Arduino Pro mini"""
    def __init__(self, doc, name='arduino'):
        data = {
            'x': 2., # mm
            'y': 33, # mm
            'z': 18, # mm
        }
        self.data = data
        col_box = {
            'x': 6., # mm
            'y': 31. + 9, # mm (9 = rs connector)
            'z': 16., # mm
        }
        self.col_box = col_box

        # make board
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'])   # 9 mm rs connector
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2 + 9, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


class ConnectCard(ElecComponent):
    """connection card"""
    def __init__(self, doc, name='connection_card'):
        data = {
            'x': 2., # mm
            'y': 80., # mm
            'z': 21., # mm
        }
        self.data = data
        col_box = {
            'x': 6., # mm
            'y': 78., # mm
            'z': 19., # mm
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

        # add connector
        connect = Part.makeBox(connector_data['x'], connector_data['y'], connector_data['z'])
        connect.translate(Vector(data['x'] / 2, -data['y'] / 2 + 2, data['z'] / 2 - connector_data['z'] - 2))
        comp = comp.fuse(connect)

        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 180)
        comp = comp.fuse(comp)  # else rotate is not taken into account

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'])
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


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
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'] + 1)
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


class ZigBee(ElecComponent):
    """make a ZigBee card"""

    def __init__(self, doc, name='zigbee'):
        data = {
            'x': 3., # mm
            'y': 22., # mm
            'z': 34., # mm
        }
        self.data = data

        col_box = {
            'x': 3., # mm
            'y': 20., # mm
            'z': 32., # mm
        }
        self.col_box = col_box

        # make card
        comp = Part.makeBox(data['x'], data['y'], data['z'])
        comp.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))

        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['x'], col_box['y'], col_box['z'] + 2)
        box.translate(Vector(-col_box['x'] / 2, -col_box['y'] / 2, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


class SdCard(ElecComponent):
    """a SD card"""

    def __init__(self, doc, name='SD_card'):
        # carte SD
        data = {
            'x': 32., # mm
            'y': 24., # mm
            'z': 2., # mm
        }
        self.data = data

        col_box = {
            'x': 34., # mm
            'y': 24., # mm
            'z': 2., # mm
        }
        self.col_box = col_box

        # make card
        comp = Part.makeBox(data['z'], data['x'], data['y'])

        comp.translate(Vector(-data['z'] / 2, -data['x'] / 2, -data['y'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeBox(col_box['z'], col_box['x'], col_box['y'])

        box.translate(Vector(-col_box['x'] / 2 + 1, -col_box['y'] / 2, -col_box['z'] / 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


class CarteRegul(ElecComponent):
    """carte regulation"""

    def __init__(self, doc, name='regul'):
        # carte puissance
        data = {
            'r_ext': 30., # mm
            'r_int': 15., # mm
            'z': 2., # mm
        }
        self.data = data

        col_box = {
            'r_ext': 29., # mm
            'r_int': 16., # mm
            'z': 8., # mm
        }
        self.col_box = col_box

        # make board
        comp = Part.makeCylinder(data['r_ext'], data['z'])
        comp = comp.cut(Part.makeCylinder(data['r_int'], data['z']))

        comp.translate(Vector(0, 0, -data['z'] / 2))
        comp = comp.fuse(comp)

        # make its collision box
        box = Part.makeCylinder(col_box['r_ext'], col_box['z'])
        box = box.cut(Part.makeCylinder(col_box['r_int'], col_box['z']))

        box.translate(Vector(0, 0, -col_box['z'] / 2 + 2))
        box = box.fuse(comp)

        ElecComponent.__init__(self, doc, comp, box, name, (0., 0.67, 0.))


