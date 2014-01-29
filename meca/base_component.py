import FreeCAD, FreeCADGui
from FreeCAD import Rotation
Gui = FreeCADGui


def debug(obj):
    FreeCAD.Console.PrintError('%r :"%s" %r\n' % (obj, obj.__doc__, dir(obj)))

def debug_shape(obj):
    FreeCAD.activeDocument().addObject("Part::Feature", 'debug').Shape = obj


class MecaComponent:
    """base for all mechanical component"""

    def __init__(self, doc, comp, name='unknown', color=(1., 0., 0.)):
        """generic meca init"""
        # must be called at the end of the specific init

        self.name = name

        self.pl = FreeCAD.Placement()

        self.comp = doc.addObject("Part::Feature", name)
        self.comp.Shape = comp
        Gui.ActiveDocument.getObject(name).ShapeColor = color

    def translate(self, vect):
        """translate component"""
        self.pl.Base = vect

        self.comp.Placement = self.pl

    def rotate(self, vect, angle):
        """rotate component"""
        self.pl.Rotation = Rotation(vect, angle)

        self.comp.Placement = self.pl

    def place(self, pl):
        """set the placement"""
        self.pl = pl

        self.comp.Placement = self.pl

    def __getitem__(self, item):
        """return dimension"""
        return self.data[item]

    def cut(self, shape):
        """overload the cut method"""
        self.comp.Shape = self.comp.Shape.cut(shape)

    def envelop(self):
        return self.comp


class ElecComponent:
    """base for all electronic component"""

    def __init__(self, doc, comp, box, name='unknown', color=(1., 0., 0.)):
        """generic elec init"""
        # must be called at the end of the specific init

        self.name = name

        self.comp = doc.addObject("Part::Feature", name)
        self.comp.Shape = comp
        Gui.ActiveDocument.getObject(name).ShapeColor = color

        self.box = doc.addObject("Part::Feature", name + '_box')
        self.box.Shape = box
        Gui.ActiveDocument.getObject(name + "_box").Visibility = False

        self.pl = FreeCAD.Placement()

    def translate(self, vect):
        """translate component and box"""
        self.pl.Base = vect

        self.comp.Placement = self.pl
        self.box.Placement = self.pl

    def rotate(self, vect, angle):
        """rotate component and box"""
        self.pl.Rotation = Rotation(vect, angle)

        self.comp.Placement = self.pl
        self.box.Placement = self.pl

    def place(self, pl):
        """set the placement"""
        self.pl = pl

        self.comp.Placement = self.pl
        self.box.Placement = self.pl

    def __getitem__(self, item):
        """return dimension of the board"""
        return self.data[item]

    def envelop(self):
        """return full collision box"""
        return self.box


