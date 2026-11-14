from . import *

# Doctor Minerva (II) — MECHANT, stade 2. KREE. SCIENTIST. SCH 1, ATK 2, PV 7. Toughness.
# [star] Forces Response: After Doctor Minerva schemes against you, deal yourself a facedown encounter
#   card.
#
# Texte identique a gs181 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDoctorMinerva()
