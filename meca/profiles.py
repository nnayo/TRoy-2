import FreeCADGui
import FreeCAD
import Part
from FreeCAD import Vector, Matrix

from base_component import MecaComponent, debug, debug_shape


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


def cone_top(cone, box, data):
    """cone top part"""
    name = 'cone_top'
    box.translate(Vector(0, 0, data['len_lo']))
    part = cone.common(box)

    return name, part


def cone_side(cone, box, data, index, cut, cylinder):
    """cone side part"""
    name = 'cone_side%d' % index

    cone_side_n = FreeCAD.activeDocument().getObject(name)
    if cone_side_n:
        return name, cone_side_n.Shape

    box = box.copy()
    box.translate(Vector(0, 0, -data['len_hi']))
    cone = cone.common(box)

    # suppress the profiles shape
    cut0 = cut.copy()
    cut1 = cut.copy()
    cylinder = cylinder.copy()
    cut0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0 + 120 * index)
    cut1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120 + 120 * index)
    cylinder.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0 + 120 * index)

    part = cone.copy()
    part = part.common(cylinder)
    part = part.cut(cut0)
    part = part.cut(cut1)

    return name, part


def cone_setup(doc, profil, data):
    """create all the shapes needed for the cone parts"""

class Cone(MecaComponent):
    """make a cone in 5 parts: 3 sides, 1 top and 1 holding structure"""
    def __init__(self, doc, profil, index=None, name='cone'):
        self.data = {
            'diameter': 123., # mm internal
            'thick': 2., # mm
            'len_lo': 150,  # mm
            'len_hi': 100,  # mm
            'struct_thick': 20., # mm
        }

        if index == None:
            return

        side = profil['side']
        radius = profil['radius']
        diam_int = self.data['diameter']
        diam_ext = self.data['diameter'] + self.data['thick']
        length = self.data['len_lo'] + self.data['len_hi']
        struct_thick = self.data['struct_thick']

        # to modify the sphere to make it a ellipsoid
        matrix = Matrix()
        matrix.scale(1., 1., length / (diam_ext / 2))

        # to suppress the lower half of the sphere/ellipsoid
        lower = Part.makeBox(diam_ext, diam_ext, length)
        lower.translate(Vector(-diam_ext / 2, -diam_ext / 2, 0))

        # make the external shape base of the cone
        cone_base_ext_obj = doc.getObject('cone_base_ext')

        if not cone_base_ext_obj:
            sphere = Part.makeSphere(diam_ext / 2)
            sphere = sphere.transformGeometry(matrix)
            cone_base_ext = sphere.common(lower)
            cone_base_ext_obj = doc.addObject("Part::Feature", 'cone_base_ext')
            cone_base_ext_obj.Shape = cone_base_ext
            FreeCADGui.ActiveDocument.getObject('cone_base_ext').Visibility = False

        cone_base_ext = cone_base_ext_obj.Shape

        # make the internal shape base of the cone
        cone_base_int_obj = doc.getObject('cone_base_int')

        if not cone_base_int_obj:
            sphere = Part.makeSphere(diam_int / 2)
            sphere = sphere.transformGeometry(matrix)
            cone_base_int = sphere.common(lower)
            cone_base_int_obj = doc.addObject("Part::Feature", 'cone_base_int')
            cone_base_int_obj.Shape = cone_base_int
            FreeCADGui.ActiveDocument.getObject('cone_base_int').Visibility = False

        cone_base_int = cone_base_int_obj.Shape

        # make the skin
        skin_obj = doc.getObject('skin')

        if not skin_obj:
            skin = cone_base_ext.cut(cone_base_int)
            skin_obj = doc.addObject("Part::Feature", 'skin')
            skin_obj.Shape = skin
            FreeCADGui.ActiveDocument.getObject('skin').Visibility = False

        skin = skin_obj.Shape

        cone = skin.copy()

        # top part
        if index == 3:
            name, cone = cone_top(cone, lower, self.data)

            MecaComponent.__init__(self, doc, cone, name, (0., 0., 0.))
            return

        # use profile shape to make suppressed parts of the skin
        shape = []

        # full profil part
        shape.append(Vector(radius, side / 2, 0))
        shape.append(Vector(radius + diam_ext, side / 2, 0))
        shape.append(Vector(radius + diam_ext, -side / 2, 0))
        shape.append(Vector(radius, -side / 2, 0))
        shape.append(Vector(radius, side / 2, 0))

        wire = Part.makePolygon(shape)

        face = Part.Face(wire)

        # make the volume
        cut = face.extrude(Vector(0, 0, self.data['len_lo']))

        # create 1/3 cylinder
        cylinder = Part.makeCylinder(diam_ext / 2, length, Vector(0, 0, 0), Vector(0, 0, 1), 120)

        # one of the 3 sides
        if index == 0:
            name, part = cone_side(cone, lower, self.data, index, cut, cylinder)

            MecaComponent.__init__(self, doc, part, name, (0., 0., 0.))
            return

        elif index == 1:
            name, part = cone_side(cone, lower, self.data, index, cut, cylinder)

            MecaComponent.__init__(self, doc, part, name, (0., 0., 0.))
            return

        elif index == 2:
            name, part = cone_side(cone, lower, self.data, index, cut, cylinder)

            MecaComponent.__init__(self, doc, part, name, (0., 0., 0.))
            return

        elif index == 4:
            name = 'cone_struct'

            struct = Part.makeSphere(diam_ext / 2)

            # modify the sphere to make it a ellipsoid
            struct = struct.transformGeometry(matrix)

            # suppress the lower half of the sphere
            struct = struct.common(lower)

            # dig a hole in the structure
            hole = Part.makeCylinder(diam_ext / 2 - struct_thick, self.data['len_lo'])
            struct = struct.cut(hole)

            hole = Part.makeCylinder(diam_ext / 2 - 2 * struct_thick, self.data['len_lo'] + struct_thick)
            struct = struct.cut(hole)

            # keep the top and the feet
            foot0 = cut.copy()
            foot0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0)
            foot1 = cut.copy()
            foot1.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120)
            foot2 = cut.copy()
            foot2.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 240)
            top = Part.makeBox(diam_ext, diam_ext, 2 * struct_thick)
            top.translate(Vector(-diam_ext / 2, -diam_ext / 2, self.data['len_lo'] - struct_thick))

            keep = top.fuse(foot0)
            keep = keep.fuse(foot1)
            keep = keep.fuse(foot2)

            struct = struct.common(keep)

            # suppress sides and top part prints
            _, top = cone_top(cone, lower, self.data)
            _, side0 = cone_side(cone, lower, self.data, 0, cut, cylinder)
#            _, side1 = cone_side(cone, lower, self.data, 1, cut, cylinder)
#            _, side2 = cone_side(cone, lower, self.data, 2, cut, cylinder)
#
            struct = struct.cut(top)
            struct = struct.cut(side0)
#            struct = struct.cut(side1)
#            struct = struct.cut(side2)

            MecaComponent.__init__(self, doc, struct, name, (1., 1., 0.))
            return


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


class ConicSkinItem(MecaComponent):
    """make a conic skin item that fits between 2 profiles"""
    def __init__(self, doc, profil, name='skin_item'):
        self.data = {
            'diameter_hi': 123., # mm internal
            'diameter_lo': 62., # mm internal
            'thick': 2., # mm
            'len': 160,  # mm
        }

        side = profil['side']
        radius = profil['radius']
        diam_hi_int = self.data['diameter_hi']
        diam_hi_ext = self.data['diameter_hi'] + self.data['thick']
        diam_lo_int = self.data['diameter_lo']
        diam_lo_ext = self.data['diameter_lo'] + self.data['thick']
        length = self.data['len']

        # use profile shape to make suppressed parts of the skin
        shape = []

        # 1st part
        shape.append(Vector(radius, side / 2, 0))
        shape.append(Vector(radius + diam_hi_ext, side / 2, 0))
        shape.append(Vector(radius + diam_hi_ext, -side / 2, 0))
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
        skin_ext = Part.makeCone(diam_lo_ext / 2, diam_hi_ext / 2, length, Vector(0, 0, 0), Vector(0, 0, 1), 120)
        skin_int = Part.makeCone(diam_lo_int / 2, diam_hi_int / 2, length, Vector(0, 0, 0), Vector(0, 0, 1), 120)
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
