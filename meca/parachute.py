import Part
from FreeCAD import Vector

import profiles


recup_system_data = {
    'len': 60.0, # mm
    'servo offset x': 30., # mm
    'servo offset y': -10., # mm
    'servo offset z': 33., # mm
}

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

ecope_data = {
    'thick': 1., # mm thickness of the door wall
}


def servo():
    """servo"""
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

    obj = body.fuse(maintien1)
    obj = obj.fuse(maintien2)
    obj = obj.fuse(cylindre)
    obj = obj.fuse(taquet)
    obj.translate(Vector(-data['x'] / 2, -data['y'] / 2, -data['z'] / 2))

    return obj


def ecope():
    """ecope"""
    data = ecope_data

    # modify a skin to add nervures and ecope
    # TODO
    skin = profiles.skin_item(rd.case_parachute['len'] + profiles.bague_data['thick'])

    return skin

