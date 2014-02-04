import Part
from FreeCAD import Vector

from base_component import MecaComponent, debug, debug_shape

recup_system_data = {
    'len': 60.0, # mm
    'servo offset x': 30., # mm
    'servo offset y': -10., # mm
    'servo offset z': 33., # mm
}

ecope_data = {
    'thick': 1., # mm thickness of the door wall
}


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
        servo.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)

        servo = servo.common(servo)
        MecaComponent.__init__(self, doc, servo, name, (0.95, 1., 1.))


def ecope():
    """ecope"""
    data = ecope_data

    # modify a skin to add nervures and ecope
    # TODO
    skin = profiles.skin_item(rd.case_parachute['len'] + profiles.bague_data['thick'])

    return skin

