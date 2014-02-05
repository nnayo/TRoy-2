import Part
from FreeCAD import Vector

from base_component import MecaComponent


class Propulsor(MecaComponent):
    """propulsor"""

    def __init__(self, doc, name='Pro_54_5G'):
        # propulseur Pro 54 5G
        self.data = {
            'len': 488. + 16., # mm
            'diameter': 54., # mm
            'hold diameter': 58., # mm
            'hold thick': 9.5, # mm
            'tuyere diameter': 32., # mm
            'tuyere len': 13., # mm
        }

        # approximate the prop
        prop = self.data
        body = Part.makeCylinder(prop['diameter'] / 2, prop['len'])
        hold = Part.makeCylinder(prop['hold diameter'] / 2, prop['hold thick'])
        hold.translate(Vector(0, 0, -prop['hold thick']))
        tuyere = Part.makeCylinder(prop['tuyere diameter'] / 2, prop['tuyere len'])
        tuyere.translate(Vector(0, 0, -prop['hold thick'] - prop['tuyere len']))

        comp = body.fuse(hold)
        comp = comp.fuse(tuyere)

        MecaComponent.__init__(self, doc, comp, name, (0.95, 1., 1.))


class Guide(MecaComponent):
    """guide"""

    def __init__(self, doc, prop, name='guide'):
        self.data = {
            'thick': 2.,                # mm thickness of the guide wall
            'len' : prop['len'] + 2.    # mm thickness of the guide wall
        }

        # make the guide
        propu = Part.makeCylinder(prop['diameter'] / 2, prop['len'])

        comp = Part.makeCylinder(prop['diameter'] / 2 + self.data['thick'], self.data['len'])
        comp = comp.cut(propu)

        MecaComponent.__init__(self, doc, comp, name, (0., 0., 0.))


class PropHoldItem(MecaComponent):
    """make a propulsor hold item that fits in line with a profile"""
    def __init__(self, doc, profil, name='prop_hold'):
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
        shape.append(Vector(radius - 20, side / 2, 0))
        shape.append(Vector(radius + diam_hi_ext, side / 2, 0))
        shape.append(Vector(radius + diam_hi_ext, -side / 2, 0))
        shape.append(Vector(radius - 20, -side / 2, 0))
        shape.append(Vector(radius - 20, side / 2, 0))

        wire0 = Part.makePolygon(shape)
        face0 = Part.Face(wire0)

        # make the cut
        cut0 = face0.extrude(Vector(0, 0, length))
        cut0.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 0)

        # make the volume
        shape_int = Part.makeCone(diam_lo_ext / 2, diam_hi_ext / 2, length)
        lower = Part.makeCone(diam_lo_ext / 2, diam_hi_ext / 2, 30)
        upper = Part.makeCylinder(diam_hi_ext / 2, 30)
        upper.translate(Vector(0, 0, 30))
        shape_ext = upper.fuse(lower)
        shape = shape_ext.cut(shape_int)

        # suppress the profiles shape
        shape = shape.common(cut0)
        prof_cut = profil.comp.Shape.copy()
        shape = shape.cut(prof_cut)

        MecaComponent.__init__(self, doc, shape, name, (0., 0., 0.))


