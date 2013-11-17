import Part
from FreeCAD import Vector

# propulseur Pro 54 3G
propulsor_data = {
    'len': 326., # mm
    'diameter': 54., # mm
    'butee diameter': 58., # mm
    'butee thick': 9.5, # mm
    'tuyere diameter': 32., # mm
    'tuyere len': 13., # mm
}

guide_data = {
    'thick': 2., # mm thickness of the guide wall
}


def propulsor():
    """propulsor"""
    prop = propulsor_data

    # approximate the prop
    body = Part.makeCylinder(prop['diameter'] / 2, prop['len'])
    hold = Part.makeCylinder(prop['butee diameter'] / 2, prop['butee thick'])
    hold.translate(Vector(0, 0, -prop['butee thick']))
    tuyere = Part.makeCylinder(prop['tuyere diameter'] / 2, prop['tuyere len'])
    tuyere.translate(Vector(0, 0, -prop['butee thick'] - prop['tuyere len']))

    obj = body.fuse(hold)
    obj = obj.fuse(tuyere)

    return obj


def guide():
    """guide"""
    prop = propulsor_data

    # make the guide
    propu = Part.makeCylinder(prop['diameter'] / 2, prop['len'])

    obj = Part.makeCylinder(prop['diameter'] / 2 + guide_data['thick'], prop['len'])
    obj = obj.cut(propu)

    return obj

