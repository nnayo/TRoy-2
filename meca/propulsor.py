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

