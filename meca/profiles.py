import Part
from FreeCAD import Vector

import rocket_data as rd

from base_component import MecaComponent


class Profile(MecaComponent):
    def __init__(self, doc, name='profile'):
        # profiles alu en U
        self.data = {
            'side': 20., # mm
            'len': 2000., # mm
            'thick': 1.5, # mm
            'radius': 60.5 + 1.5 - 20., # mm // bague['len'] + thick - side
        }

        """make a profile by extrusion"""
        # retreive configuration
        side = self.data['side']
        thick = self.data['thick']
        length = self.data['len']

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
        wire.translate(Vector(0, -side / 2, 0))
        face = Part.Face(wire)
        profil = face.extrude(Vector(0, 0, length))

        MecaComponent.__init__(self, doc, profil, name, (0.95, 1., 1.))


class Bague(MecaComponent):
    """make a bague by extrusion"""

    def __init__(self, doc, profil, name='bague'):
        self.data = {
            'thick': 10., # mm
            'hole radius': 4., # mm
            'side': profil['side'] - 2 * profil['thick'], # mm
            'len': 60.5, # mm
        }

        side = self.data['side']
        thick = self.data['thick']
        length = self.data['len']

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
        bague = face.extrude(Vector(0, 0, thick))

        # dig the hole
        hole = Part.makeCylinder(self.data['hole radius'], thick)
        bague = bague.cut(hole)

        MecaComponent.__init__(self, doc, bague, name, (0.95, 1., 1.))


class BaguePropulsor(MecaComponent):
    """most complicated bague"""
    # TODO
    def __init__(self, doc, profil, name='bague propulsor'):
        self.data = {
            'thick': 10., # mm
            'side': profil['side'] - 2 * profil['thick'], # mm
            'len': 60.5, # mm
            'ring radius': 39., # mm
            'hole radius': 29., # mm
            'offset z': 120. # mm
        }

        base = self.data['ring radius'] - self.data['side']
        side = self.data['side']
        thick = self.data['thick']
        length = self.data['len']
        
        # make bague shape
        shape = []

        # first branch
        shape.append(Vector(base, -side / 2, 0))
        shape.append(Vector(length, -side / 2, 0))
        shape.append(Vector(length, side / 2, 0))
        shape.append(Vector(base, side / 2, 0))

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
        branches = face.extrude(Vector(0, 0, thick))

        # make the ring
        bague = Part.makeCylinder(self.data['ring radius'], thick)
        hole = Part.makeCylinder(self.data['hole radius'], thick)
        bague = bague.fuse(branches)
        bague = bague.cut(hole)

        MecaComponent.__init__(self, doc, bague, name, (0.95, 1., 1.))


class Disque(MecaComponent):
    def __init__(self, doc, profil, skin, name='disque'):
        """make a disque by extrusion"""

        self.data = {
            'thick': 5., # mm
            'hole radius': 30., # mm
            'diameter': skin['diameter'] + skin['thick'], # mm
        }

        side = profil['side']
        radius = profil['radius']
        thick = self.data['thick']
        diam = self.data['diameter']

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
        disque = Part.makeCylinder(diam / 2, thick)
        disque = disque.cut(cut0)
        disque = disque.cut(cut1)
        disque = disque.cut(cut2)

        # dig the hole
        hole = Part.makeCylinder(self.data['hole radius'], thick)
        disque = disque.cut(hole)

        MecaComponent.__init__(self, doc, disque, name, (0.95, 1., 1.))


class SkinItem(MecaComponent):
    """make a skin item that fits between 2 profiles with the given length"""
    def __init__(self, doc, length, profil, name='skin_item'):
        self.data = {
            'diameter': 123., # mm internal
            'thick': 2., # mm
            'len': length,  # mm
        }

        side = profil['side']
        radius = profil['radius']
        diam_int = self.data['diameter']
        diam_ext = self.data['diameter'] + self.data['thick']

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

        MecaComponent.__init__(self, doc, skin, name, (0., 0., 0.))


class Fin(MecaComponent):
    """make a fin"""
    def __init__(self, doc, name='fin'):
        # ailerons
        self.data = {
            'len': 300., # mm
            'e': 200., # mm
            'p': 50., # mm
            'm': 200., # mm
            'thick': 3., # mm
        }

        # use profile shape to make suppressed parts of the skin
        shape = []

        # 1st part
        shape.append(Vector(0, 0, 0))
        shape.append(Vector(0, 0, self.data['len']))
        shape.append(Vector(self.data['e'], 0, self.data['len'] - self.data['p']))
        shape.append(Vector(self.data['e'], 0, self.data['len'] - self.data['p'] - self.data['m']))
        shape.append(Vector(0, 0, 0))

        wire = Part.makePolygon(shape)
        # center it
        wire.translate(Vector(0, - self.data['thick'] / 2, 0))
        face = Part.Face(wire)

        # make the volume
        comp = face.extrude(Vector(0, self.data['thick'], 0))

        # center it
        #comp.translate(Vector(0, - self.data['thick'] / 2, 0))

        MecaComponent.__init__(self, doc, comp, name, (0.95, 1., 1.))
