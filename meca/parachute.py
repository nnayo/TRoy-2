import Part
from FreeCAD import Vector

from base_component import MecaComponent


class Servo(MecaComponent):
    """servo"""
    def __init__(self, doc, name='servo'):
        # servo parallalax
        servo_data = {
            'x': 40.5, # mm
            'y': 20.0, # mm
            'z': 36.1, # mm
            'cylindre r': 10.0, # mm
            'cylindre h': 6.0, # mm
            'cylindre offset x': 30.1, # mm
            'cylindre offset z': 36.1, # mm
            'maintien x': 7.5, # mm
            'maintien y': 20., # mm
            'maintien z': 3.5, # mm
            'maintien offset z': 26.6, # mm
            'taquet x': 30.1, # mm
            'taquet y': 5., # mm
            'taquet z': 2., # mm
        }

        data = servo_data

        # approximate the servo
        body = Part.makeBox(data['x'], data['y'], data['z'])

        maintien1 = Part.makeBox(data['maintien x'], data['maintien y'], data['maintien z'])
        maintien1.translate(Vector(data['x'], 0, data['maintien offset z']))
        maintien2 = Part.makeBox(data['maintien x'], data['maintien y'], data['maintien z'])
        maintien2.translate(Vector(-data['maintien x'], 0, data['maintien offset z']))

        cylindre = Part.makeCylinder(data['cylindre r'], data['cylindre h'])
        cylindre.translate(Vector(data['cylindre offset x'], data['y'] / 2, data['cylindre offset z']))

        taquet = Part.makeBox(data['taquet x'], data['taquet y'], data['taquet z'])
        taquet.translate(Vector(-data['taquet y'] / 2, -data['taquet y'] / 2, 0))
        taquet.rotate(Vector(0, 0, 0), Vector(0, 0, 1), -90)
        taquet.translate(Vector(data['cylindre offset x'], data['y'] / 2, data['z'] + data['cylindre h']))

        servo = body.fuse(maintien1)
        servo = servo.fuse(maintien2)
        servo = servo.fuse(cylindre)
        servo = servo.fuse(taquet)

        servo.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))
        servo.rotate(Vector(0, 0, 0), Vector(1, 0, 0), -90)
        servo.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        #servo.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)

        servo = servo.common(servo)
        MecaComponent.__init__(self, doc, servo, name, (0.95, 1., 1.))


class SkinItem(MecaComponent):
    """make a skin item that fits between 2 profiles with the given length"""
    def __init__(self, doc, length, profil, name='parachue_skin'):
        self.data = {
            'diameter': 123., # mm internal
            'thick': 2., # mm
            'len': length,  # mm
        }

        side = profil['side']
        radius = profil['radius']
        thick = self.data['thick']
        diam_int = self.data['diameter']
        diam_ext = self.data['diameter'] + thick

        # use profile shape to make suppressed parts of the skin
        shape = []
        shape.append(Vector(radius - 20, side / 2, 0))
        shape.append(Vector(radius + diam_ext, side / 2, 0))
        shape.append(Vector(radius + diam_ext, -side / 2, 0))
        shape.append(Vector(radius - 20, -side / 2, 0))
        shape.append(Vector(radius - 20, side / 2, 0))

        wire0 = Part.makePolygon(shape)

        # 1st part
        face0 = Part.Face(wire0)

        # 2nd part
        face1 = Part.Face(wire0)

        # make the volumes
        cut0 = face0.extrude(Vector(0, 0, length))
        cut0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0)

        cut1 = face1.extrude(Vector(0, 0, length))
        cut1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)

        # make the skin
        skin_ext = Part.makeCylinder(diam_ext / 2, length, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        skin_int = Part.makeCylinder(diam_int / 2, length, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        skin = skin_ext.cut(skin_int)

        # create bottom and separation planes
        plane_ext = Part.makeCylinder(diam_int / 2, thick, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        plane_int = Part.makeCylinder(diam_int / 2 - 30, thick, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        plane = plane_ext.cut(plane_int)

        bottom = plane.copy()
        sepa = plane.copy()
        sepa.translate(Vector(0, 0, length - 60))

        skin = skin.fuse(bottom)
        skin = skin.fuse(sepa)

        # add nerves on both sides of the skin
        # 1st part
        shape = []
        shape.append(Vector(radius, side / 2, 0))
        shape.append(Vector(diam_int / 2, side / 2, 0))
        shape.append(Vector(diam_int / 2, side / 2 + thick, 0))
        shape.append(Vector(radius, side / 2 + thick, 0))
        shape.append(Vector(radius, side / 2, 0))

        wire = Part.makePolygon(shape)
        face = Part.Face(wire)

        # make the volume
        nerv0 = face.extrude(Vector(0, 0, length))
        nerv0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0)

        # 2nd part
        shape = []
        shape.append(Vector(radius, -side / 2, 0))
        shape.append(Vector(diam_int / 2, -side / 2, 0))
        shape.append(Vector(diam_int / 2, -side / 2 - thick, 0))
        shape.append(Vector(radius, -side / 2 - thick, 0))
        shape.append(Vector(radius, -side / 2, 0))

        wire = Part.makePolygon(shape)
        face = Part.Face(wire)

        # make the volume
        nerv1 = face.extrude(Vector(0, 0, length))
        nerv1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)

        skin = skin.fuse(nerv0)
        skin = skin.fuse(nerv1)

        # suppress the profiles shape
        skin = skin.cut(cut0)
        skin = skin.cut(cut1)

        MecaComponent.__init__(self, doc, skin, name, (0., 0., 0.))


class Ecope(MecaComponent):
    """make an ecope"""
    def __init__(self, doc, name='ecope'):
        self.data = {
            'diameter': 123., # mm internal
            'x': 30,
            'z': 60,
            'thick': 2., # mm thickness of the door wall
        }

        thick = self.data['thick']
        diam_int = self.data['diameter']
        diam_ext = self.data['diameter'] + thick
        x = self.data['x']
        y = self.data['y']
        z = self.data['z']

        # make the skin
        skin_ext = Part.makeCylinder(diam_ext / 2, z, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        skin_int = Part.makeCylinder(diam_int / 2, z, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        skin = skin_ext.cut(skin_int)

        # make the external box
        box_ext = Part.makeBox(x, y, z)
        box_ext.translate(Vector(-x / 2, -y / 2, -z / 2))

        ecope = skin.cut(box_ext)

        MecaComponent.__init__(self, doc, ecope, name, (0., 0., 0.))
