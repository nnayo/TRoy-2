import FreeCAD
from FreeCAD import Vector, Rotation, Placement
import Part
from math import cos, sin, pi

import profiles
import propulsor
import elec
import parachute

def vector_neg(vect):
    return Vector(-vect.x, -vect.y, -vect.z)


def profile_draw(doc):
    # create and position 3 profiles
    for angle in range(0, 360, 120):
        profil = profiles.Profile(doc, name='profile_%d' % angle)
        radius = profil['radius']
        profil.translate(Vector(radius * cos(2 * pi * angle / 360), radius * sin(2 * pi * angle / 360), 0))
        profil.rotate(Vector(0, 0, 1), angle)

    return profil

    # creation and position of fins
    for angle in range(0, 360, 120):
        fin = profiles.Fin(doc, "fin_%d" % angle)
        radius = profil['radius'] + profil['side']
        fin.translate(Vector(radius * cos(2 * pi * angle / 360), radius * sin(2 * pi * angle / 360), 0))
        fin.rotate(Vector(0, 0, 1), angle)

    return profil

def disque_draw(doc, profil, skin):
    # creation and position of propulsor bague and its disque
    bague = profiles.BaguePropulsor(doc, profil, 'bague_propu')
    bague.translate(Vector(0, 0, bague['offset z']))
    disque = profiles.Disque(doc, profil, skin, "disque_%d" % bague['offset z'])
    disque.translate(Vector(0, 0, bague['offset z'] + bague['thick']))

    return

    # creation and position 3 bagues and 3 disques
    position = 477

    bague = profiles.Bague(doc, profil, "bague_%d" % position)
    bague.translate(Vector(0, 0, position - bague['thick'] / 2))

    position += bague['thick'] / 2
    disque = profiles.Disque(doc, profil, skin, "disque_%d" % position)
    disque.translate(Vector(0, 0, position))

    position = 1180

    bague = profiles.Bague(doc, profil, "bague_%d" % position)
    bague.translate(Vector(0, 0, position - bague['thick'] / 2))

    position += bague['thick'] / 2
    disque = profiles.Disque(doc, profil, skin, "disque_%d" % position)
    disque.translate(Vector(0, 0, position))

    position = 1745

    bague = profiles.Bague(doc, profil, "bague_%d" % position)
    bague.translate(Vector(0, 0, position - bague['thick'] / 2))

    position += bague['thick'] / 2
    disque = profiles.Disque(doc, profil, skin, "disque_%d" % position)
    disque.translate(Vector(0, 0, position))


def prop_draw(doc):
    # create and position

    # propulsor
    propu = propulsor.Propulsor(doc)
    propu.translate(Vector(0, 0, -34.))

    # guide
    guide = propulsor.Guide(doc, propu)
    guide.translate(Vector(0, 0, -34.))


def parachute_draw(doc, profil):
    """every thing related to parachute"""

    position = 1745 - 5 - 20

    for i in range(3):
        name = 'servo_%d' % i

        servo = parachute.Servo(doc, name)
        translation = Vector(-30, 0, position)
        rotation = Rotation(Vector(0, 0, 1), 120 * i - 120)
        placement = Placement(translation, rotation, vector_neg(translation))
        servo.place(placement)

    # parachute skins
    position = 1180 + 5 + 5
    length = 1745 - 1180 - 5

    for i in range(3):
        ecope = parachute.Ecope(doc, 'ecope_%d' % i)
        skin_item = parachute.SkinItem(doc, length, profil, ecope, 'parachute_skin_%d' % i)

        ecope.translate(Vector(0, 0, position + length - ecope['z']))
        ecope.rotate(Vector(0, 0, 1), 120 * i)

        skin_item.translate(Vector(0, 0, position))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)


def elec_draw(doc):
    position = 1745 + 5 + 5

    # minut zone
    offset_radius = 43
    for i in range(0, 3):
        arduino = elec.Arduino(doc, 'minuterie_%d' % i)

        translation = Vector(offset_radius, 20, position + 3 * elec.minut_zone_data['offset'])
        rotation = Rotation(Vector(0, 0, 1), 60 + 120 * i)
        placement = Placement(translation, rotation, vector_neg(translation))
        arduino.place(placement)

        connect = elec.ConnectCard(doc, 'connection_%d' % i)

        translation = Vector(offset_radius, 0, position + elec.minut_zone_data['offset'])
        rotation = Rotation(Vector(0, 0, 1), 60 + 120 * i)
        placement = Placement(translation, rotation, vector_neg(translation))
        connect.place(placement)

        mpu = elec.Mpu(doc, 'mpu_%d' % i)

        translation = Vector(offset_radius, -15, position + 3 * elec.minut_zone_data['offset'])
        rotation = Rotation(Vector(0, 0, 1), 60 + 120 * i)
        placement = Placement(translation, rotation, vector_neg(translation))
        mpu.place(placement)

    # tag top of minut zone
    position += elec.minut_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, position))
    doc.addObject("Part::Feature", 'top_minut_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_minut_zone").Visibility = False

    # regul zone
    offset_radius = 45
    for i in range(3):
        for j in range(3):
            pile = elec.Pile9V(doc, 'pile_9v_%d%d' % (i, j))

            translation = Vector(offset_radius, 0, position + elec.regul_zone_data['offset pile'])
            rotation = Rotation(Vector(0, 0, 1), 120 * i + 60 + 30 * j - 30)
            placement = Placement(translation, rotation, vector_neg(translation))
            pile.place(placement)

    carte = elec.CarteRegul(doc)
    carte.translate(Vector(0, 0, position + elec.regul_zone_data['offset carte']))

    position += elec.regul_zone_data['len']

    # tag top of regul zone
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, position))
    doc.addObject("Part::Feature", 'top_regul_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_regul_zone").Visibility = False

    # high storage zone
    offset_radius = 25
    ardu = elec.Arduino(doc, 'storage_hi')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0)
    placement = Placement(translation, rotation, vector_neg(translation))
    ardu.place(placement)

    connect = elec.ConnectCard(doc, 'connection_hi')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 240)
    placement = Placement(translation, rotation, vector_neg(translation))
    connect.place(placement)

    sd_card = elec.SdCard(doc, 'sd_card_hi')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 120)
    placement = Placement(translation, rotation, vector_neg(translation))
    sd_card.place(placement)

    position += elec.hi_storage_zone_data['len']

    # tag top of high storage zone
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, position))
    doc.addObject("Part::Feature", 'top_hi_storage_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_hi_storage_zone").Visibility = False

    # HF zone
    offset_radius = 25
    ardu = elec.Arduino(doc, 'hf')
    translation = Vector(offset_radius, 0, position + elec.hf_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0)
    placement = Placement(translation, rotation, vector_neg(translation))
    ardu.place(placement)

    connect = elec.ConnectCard(doc, 'connection_hf')
    translation = Vector(offset_radius, 0, position + elec.hf_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 240)
    placement = Placement(translation, rotation, vector_neg(translation))
    connect.place(placement)

    zigbee = elec.ZigBee(doc, 'zigbee')
    translation = Vector(offset_radius, 0, position + elec.hf_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 120)
    placement = Placement(translation, rotation, vector_neg(translation))
    zigbee.place(placement)

    position += elec.hf_zone_data['len']

    # tag top of HF zone
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, position))
    doc.addObject("Part::Feature", 'top_hf_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_hf_zone").Visibility = False

    # back to bottom
    position = 477 + 5 + 5

    # low storage zone
    offset_radius = 25
    ardu = elec.Arduino(doc, 'storage_lo')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0)
    placement = Placement(translation, rotation, vector_neg(translation))
    ardu.place(placement)

    connect = elec.ConnectCard(doc, 'connection_lo')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 240)
    placement = Placement(translation, rotation, vector_neg(translation))
    connect.place(placement)

    sd_card = elec.SdCard(doc, 'sd_card_lo')
    translation = Vector(offset_radius, 0, position + elec.hi_storage_zone_data['offset'])
    rotation = Rotation(Vector(0, 0, 1), 0 + 120)
    placement = Placement(translation, rotation, vector_neg(translation))
    sd_card.place(placement)

    position += elec.lo_storage_zone_data['len']

    # tag top of high storage zone
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, position))
    doc.addObject("Part::Feature", 'top_lo_storage_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_lo_storage_zone").Visibility = False


def skin_draw(doc, profil):
    """draw each skin items"""
    # lower fin skins
    offset = -30
    for i in range(3):
        conic_skin_item = profiles.ConicSkinItem(doc, profil, 'lower_fin_skin_%d' % i)
        conic_skin_item.translate(Vector(0, 0, offset))
        conic_skin_item.rotate(Vector(0, 0, 1), 120 * i)

    conic_skin_item = propulsor.PropHoldItem(doc, profil, 'prop_hold')
    conic_skin_item.translate(Vector(0, 0, offset - 5))

    # upper fin skins
    offset = 120 + 10 + 5
    for i in range(3):
        skin_item = profiles.SkinItem(doc, 477 - 120 - 10, profil, 'upper_fin_skin_%d' % i)
        skin_item.translate(Vector(0, 0, offset))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)

    return skin_item

    # equipement skins
    offset = 477 + 5 + 5
    for i in range(3):
        skin_item = profiles.SkinItem(doc, 1180 - 477 - 5, profil, 'equipment_skin_%d' % i)
        skin_item.translate(Vector(0, 0, offset))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)

    # parachute skins
    # see in parachute_draw()

    # lower cone skins
    offset = 1745 + 5 + 5
    for i in range(3):
        skin_item = profiles.SkinItem(doc, 2000 - 1745 - 5 - 5, profil, 'lower_cone_skin_%d' % i)
        skin_item.translate(Vector(0, 0, offset))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)

    # upper cone skins
    offset = 2000

    cone_top = profiles.Cone(doc, profil, 3)
    cone_top.translate(Vector(0, 0, offset))

    cone_side0 = profiles.Cone(doc, profil, 0)
    cone_side0.translate(Vector(0, 0, offset))
    cone_side0.rotate(Vector(0, 0, 1), 0)

    cone_side1 = profiles.Cone(doc, profil, 1)
    cone_side1.translate(Vector(0, 0, offset))
    cone_side1.rotate(Vector(0, 0, 1), 120)

    cone_side2 = profiles.Cone(doc, profil, 2)
    cone_side2.translate(Vector(0, 0, offset))
    cone_side2.rotate(Vector(0, 0, 1), 240)

    cone_struct = profiles.Cone(doc, profil, 4)
    cone_struct.translate(Vector(0, 0, offset))

    cone_top_thread = profiles.Cone(doc, profil, 5)
    cone_top_thread.translate(Vector(0, 0, offset))
    cone_top_thread.translate(Vector(0, 0, offset + cone_top_thread['len_lo']))

    cone_struct_thread = profiles.Cone(doc, profil, 6)
    cone_struct_thread.translate(Vector(0, 0, offset + cone_struct_thread['len_lo']))
    cone_struct_thread.rotate(Vector(0, 0, 1), 180)

    return skin_item


def main(doc):
    #prop_draw(doc)
    profil = profile_draw(doc)
    skin = skin_draw(doc, profil)
    disque_draw(doc, profil, skin)
    #elec_draw(doc)
    #parachute_draw(doc, profil)

    FreeCAD.Gui.SendMsgToActiveView("ViewFit")


if __name__ == "__main__":
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument('TRoy 2')

    main(doc)
