import Part
from FreeCAD import Vector

import rocket_data as rd


# profiles alu en U
profile_data = {
    'side': 20., # mm
    'len': 2000., # mm
    'thick': 1.5, # mm
    'radius': 60.5 + 1.5 - 20., # mm // bague['len'] + thick - side
}

# bague de maintien
bague_data = {
    'thick': 10., # mm
    'hole radius': 4., # mm
    'side': profile_data['side'] - 2 * profile_data['thick'], # mm
    'len': 60.5, # mm
}

# bague propulseur
bague_propu_data = {
    'ring radius': 39., # mm
    'hole radius': 29., # mm
    'offset z': 120. # mm
}

# disque de separation
disque_data = {
    'thick': 5., # mm
    'hole radius': 30., # mm
    'diameter': rd.skin['diameter'] + rd.skin['thick'], # mm
}

# ailerons
fins_data = {
    'len': 300., # mm
    'e': 200., # mm
    'p': 50., # mm
    'm': 200., # mm
    'thick': 3., # mm
}


def profile():
    """make a profile by extrusion"""
    # retreive configuration
    side = profile_data['side']
    thick = profile_data['thick']
    length = profile_data['len']
    radius = profile_data['radius']

    # make profile shape
    shape = []
    shape.append(Part.makeLine((0, 0, 0), (side, 0, 0)))
    shape.append(Part.makeLine((side, 0, 0), (side, side, 0)))
    shape.append(Part.makeLine((side, side, 0), (0, side, 0)))
    shape.append(Part.makeLine((0, side, 0), (0, side - thick, 0)))
    shape.append(Part.makeLine((0, side - thick, 0), (side - thick, side - thick, 0)))
    shape.append(Part.makeLine((side - thick, side - thick, 0), (side - thick, thick, 0)))
    shape.append(Part.makeLine((side - thick, thick, 0), (0, thick, 0)))
    shape.append(Part.makeLine((0, thick, 0), (0, 0, 0)))

    wire = Part.Wire(shape)
    face = Part.Face(wire)
    profil = face.extrude(Vector(0, 0, length))
    profil.translate(Vector(0, -side / 2, 0))

    return profil


def bague():
    """make a bague by extrusion"""
    # retreive configuration
    side = bague_data['side']
    thick = bague_data['thick']
    length = bague_data['len']

    # make bague shape
    shape = []

    # first branch
    shape.append(Vector(side, -side / 2, 0))
    shape.append(Vector(length, -side / 2, 0))
    shape.append(Vector(length, side / 2, 0))
    shape.append(Vector(side, side / 2, 0))

    wire0 = Part.makePolygon(shape)

    # 2nd and 3rd branches
    wire1 = wire0.copy()
    wire1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)
    wire2 = wire0.copy()
    wire2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 240)

    # union of all branches
    wire = wire0.fuse(wire1)
    wire = wire.fuse(wire2)
    vertexes = []
    for edg in wire.Edges:
        vertexes += edg.Vertexes
    points = []
    for vrt in vertexes:
        points.append(vrt.Point)
    points.append(points[0])    # close the wire

    wire = Part.makePolygon(points)
    face = Part.Face(wire)

    # make the volume
    bagu = face.extrude(Vector(0, 0, thick))

    # dig the hole
    hole = Part.makeCylinder(bague_data['hole radius'], thick)
    bagu = bagu.cut(hole)

    return bagu


def bague_propu():
    """most complicated bague"""
    # TODO
    # retreive configuration
    side = bague_data['side']
    thick = bague_data['thick']
    length = bague_data['len']

    # make bague shape
    shape = []

    # first branch
    shape.append(Vector(side, -side / 2, 0))
    shape.append(Vector(length, -side / 2, 0))
    shape.append(Vector(length, side / 2, 0))
    shape.append(Vector(side, side / 2, 0))

    wire0 = Part.makePolygon(shape)

    # 2nd and 3rd branches
    wire1 = wire0.copy()
    wire1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)
    wire2 = wire0.copy()
    wire2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 240)

    # union of all branches
    wire = wire0.fuse(wire1)
    wire = wire.fuse(wire2)
    vertexes = []
    for edg in wire.Edges:
        vertexes += edg.Vertexes
    points = []
    for vrt in vertexes:
        points.append(vrt.Point)
    points.append(points[0])    # close the wire

    wire = Part.makePolygon(points)
    face = Part.Face(wire)

    # make the volume
    bagu = face.extrude(Vector(0, 0, thick))

    # ring part
    ring = Part.makeCylinder(bague_propu_data['ring radius'], thick)
    bagu = bagu.fuse(ring)

    # dig the hole
    hole = Part.makeCylinder(bague_propu_data['hole radius'], thick)
    bagu = bagu.cut(hole)

    return bagu




def disque():
    """make a disque by extrusion"""
    # retreive configuration
    side = profile_data['side']
    radius = profile_data['radius']
    thick = disque_data['thick']
    diam = disque_data['diameter']

    # use profile shape to make suppressed parts of the disque
    shape = []

    # 1st part
    shape.append(Vector(radius, side / 2, 0))
    shape.append(Vector(radius + diam, side / 2, 0))
    shape.append(Vector(radius + diam, -side / 2, 0))
    shape.append(Vector(radius, -side / 2, 0))
    shape.append(Vector(radius, side / 2, 0))

    wire0 = Part.makePolygon(shape)
    face0 = Part.Face(wire0)

    # 2nd and 3rd parts
    face1 = Part.Face(wire0)
    face2 = Part.Face(wire0)

    # make the volumes
    cut0 = face0.extrude(Vector(0, 0, thick))
    cut0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0)

    cut1 = face1.extrude(Vector(0, 0, thick))
    cut1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)

    cut2 = face2.extrude(Vector(0, 0, thick))
    cut2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 240)

    # make the disque
    disqu = Part.makeCylinder(diam / 2, thick)
    disqu = disqu.cut(cut0)
    disqu = disqu.cut(cut1)
    disqu = disqu.cut(cut2)

    # dig the hole
    hole = Part.makeCylinder(disque_data['hole radius'], thick)
    disqu = disqu.cut(hole)

    return disqu


def skin_item(length):
    """make a skin item that fits between 2 profiles with the given length"""
    # retreive configuration
    side = profile_data['side']
    radius = profile_data['radius']
    diam_int = rd.skin['diameter']
    diam_ext = rd.skin['diameter'] + rd.skin['thick']

    # use profile shape to make suppressed parts of the skin
    shape = []

    # 1st part
    shape.append(Vector(radius, side / 2, 0))
    shape.append(Vector(radius + diam_ext, side / 2, 0))
    shape.append(Vector(radius + diam_ext, -side / 2, 0))
    shape.append(Vector(radius, -side / 2, 0))
    shape.append(Vector(radius, side / 2, 0))

    wire0 = Part.makePolygon(shape)
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

    # suppress the profiles shape
    skin = skin.cut(cut0)
    skin = skin.cut(cut1)

    return skin


def fin():
    """make a fin"""
    # use profile shape to make suppressed parts of the skin
    shape = []

    # 1st part
    shape.append(Vector(0, 0, 0))
    shape.append(Vector(0, 0, fins_data['len']))
    shape.append(Vector(fins_data['e'], 0, fins_data['len'] - fins_data['p']))
    shape.append(Vector(fins_data['e'], 0, fins_data['len'] - fins_data['p'] - fins_data['m']))
    shape.append(Vector(0, 0, 0))

    wire = Part.makePolygon(shape)
    face = Part.Face(wire)

    # make the volume
    _fin = face.extrude(Vector(0, fins_data['thick'], 0))

    # center it
    _fin.translate(Vector(0, - fins_data['thick'] / 2, 0))

    return _fin
