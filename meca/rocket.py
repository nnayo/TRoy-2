import FreeCAD
from FreeCAD import Vector
import Part
from math import cos, sin, pi

import rocket_data as rd
import profiles
import propulsor
import elec
import parachute


def profile_draw(doc, guide):
    # create and position 3 profiles
    for angle in range(0, 360, 120):
        profil = profiles.Profile(doc, name='profile_%d' % angle)
        radius = profil['radius']
        profil.translate(Vector(radius * cos(2 * pi * angle / 360), radius * sin(2 * pi * angle / 360), 0))
        profil.rotate(Vector(0, 0, 1), angle)

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

    return guide


def parachute_draw(doc):
    """every thing related to parachute"""
    # bottom of parachute case
    total_len = propulsor.propulsor_data['len'] + rd.case_equipement['len']
    total_len += 2 * profiles.bague_data['thick'] + 2 * profiles.disque_data['thick']
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'bottom_parachute_case').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("bottom_parachute_case").Visibility = False

    # top of parachute case
    total_len += rd.case_parachute['len']
    total_len += profiles.bague_data['thick'] + profiles.disque_data['thick']
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_parachute_case').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_parachute_case").Visibility = False

    total_len -= parachute.recup_system_data['len']
    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'bottom_recup_system').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("bottom_recup_system").Visibility = False

    rsd = parachute.recup_system_data
    for i in range(3):
        servo = parachute.servo()
        servo.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 90)
        servo.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
        servo.translate(Vector(rsd['servo offset x'], rsd['servo offset y'], total_len + rsd['servo offset z']))
        servo.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120 * i)
        doc.addObject("Part::Feature", 'servo %d' % i).Shape = servo


def elec_draw(doc):
    total_len = propulsor.propulsor_data['len'] + rd.case_equipement['len'] + rd.case_parachute['len']
    total_len += 3 * profiles.bague_data['thick'] + 3 * profiles.disque_data['thick']

    # minut zone
    for i in range(3):
        comp = elec.arduino()
        comp.translate(Vector(45, 20, total_len + 3 * elec.minut_zone_data['offset']))
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120 * i)
        doc.addObject("Part::Feature", 'minuterie %d' % i).Shape = comp

        comp = elec.connect_card()
        comp.translate(Vector(45, 0, total_len + elec.minut_zone_data['offset']))
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120 * i)
        doc.addObject("Part::Feature", 'connection %d' % i).Shape = comp

        comp = elec.mpu()
        comp.translate(Vector(45, -15, total_len + 3 * elec.minut_zone_data['offset']))
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120 * i)
        doc.addObject("Part::Feature", 'mpu %d' % i).Shape = comp

    total_len += elec.minut_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_minut_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_minut_zone").Visibility = False

    # regul zone
    for i in range(3):
        for j in range(3):
            comp = elec.pile_9v()
            comp.translate(Vector(45, 0, total_len + elec.regul_zone_data['offset pile']))
            comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120 * i + 60 + 30 * j - 30)
            doc.addObject("Part::Feature", 'pile 9v %d%d' % (i, j)).Shape = comp

    comp = elec.carte_regul()
    comp.translate(Vector(0, 0, total_len + elec.regul_zone_data['offset carte']))
    doc.addObject("Part::Feature", 'carte regulation').Shape = comp

    total_len += elec.regul_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_regul_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_regul_zone").Visibility = False

    # high storage zone
    comp = elec.arduino()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60)
    doc.addObject("Part::Feature", 'storage hi').Shape = comp

    comp = elec.connect_card()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 240)
    doc.addObject("Part::Feature", 'connection hi').Shape = comp

    comp = elec.sd_card()
    comp.translate(Vector(20, 0, total_len + elec.minut_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120)
    doc.addObject("Part::Feature", 'sd card hi').Shape = comp

    total_len += elec.hi_storage_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_hi_storage_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_hi_storage_zone").Visibility = False

    # HF zone
    comp = elec.arduino()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60)
    doc.addObject("Part::Feature", 'hf').Shape = comp

    comp = elec.connect_card()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 240)
    doc.addObject("Part::Feature", 'connection hf').Shape = comp

    comp = elec.zigbee()
    comp.rotate(Vector(0, 0, 0), Vector(0, 1, 0), 90)
    comp.translate(Vector(20, 0, total_len + elec.minut_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120)
    doc.addObject("Part::Feature", 'zigbee').Shape = comp

    total_len += elec.hf_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_hf_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_hf_zone").Visibility = False

    # back to bottom
    total_len = propulsor.propulsor_data['len']
    total_len += profiles.bague_data['thick'] + profiles.disque_data['thick']

    # low storage zone
    comp = elec.arduino()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60)
    doc.addObject("Part::Feature", 'storage lo').Shape = comp

    comp = elec.connect_card()
    comp.translate(Vector(20, 0, total_len + elec.hf_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 240)
    doc.addObject("Part::Feature", 'connection lo').Shape = comp

    comp = elec.sd_card()
    comp.translate(Vector(20, 0, total_len + elec.minut_zone_data['offset']))
    comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 60 + 120)
    doc.addObject("Part::Feature", 'sd card lo').Shape = comp

    total_len += elec.lo_storage_zone_data['len']

    obj = Part.makeCylinder(200, 1)
    obj.translate(Vector(0, 0, total_len))
    doc.addObject("Part::Feature", 'top_lo_storage_zone').Shape = obj
    FreeCAD.Gui.ActiveDocument.getObject("top_lo_storage_zone").Visibility = False


def skin_draw(doc, profil):
    """draw each skin items"""
    # lower fin skins
    # TODO

    # upper fin skins
    offset = 120 + 10 + 5
    for i in range(3):
        skin_item = profiles.SkinItem(doc, 477 - 120 - 10, profil, 'upper_fin_skins_%d' % i)
        skin_item.translate(Vector(0, 0, offset))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)

    # equipement skins
    offset = 477 + 5 + 5
    for i in range(3):
        skin_item = profiles.SkinItem(doc, 1180 - 477, profil, 'equipment_skins_%d' % i)
        skin_item.translate(Vector(0, 0, offset))
        skin_item.rotate(Vector(0, 0, 1), 120 * i)

    return skin_item

    # parachute skins
    offset += rd.case_equipement['len'] + profiles.bague_data['thick'] + profiles.disque_data['thick']
    for i in range(3):
        comp = parachute.ecope()
        comp.translate(Vector(0, 0, offset))
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120 * i)
        doc.addObject("Part::Feature", 'parachute skin %d' % i).Shape = comp

    # lower cone skins
    offset += rd.case_parachute['len'] + profiles.bague_data['thick'] + profiles.disque_data['thick']
    for i in range(3):
        comp = profiles.skin_item(profiles.profile_data['len'] - offset)
        comp.translate(Vector(0, 0, offset))
        comp.rotate(Vector(0, 0, 0), Vector(0, 0, 1), 120 * i)
        doc.addObject("Part::Feature", 'lower cone skin %d' % i).Shape = comp

    # upper cone skins
    # TODO


def main(doc):
    guide = prop_draw(doc)
    profil = profile_draw(doc, guide)
    skin = skin_draw(doc, profil)
    disque_draw(doc, profil, skin)
    #parachute_draw(doc)
    #elec_draw(doc)

    FreeCAD.Gui.SendMsgToActiveView("ViewFit")


if __name__ == "__main__":
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument('TRoy 2')

    main(doc)
