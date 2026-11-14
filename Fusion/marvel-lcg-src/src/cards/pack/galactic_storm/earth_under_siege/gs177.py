from . import *

# Destroyer (II) — MECHANT, stade 2. ASGARD. SCH 1, ATK 3, PV 7. Toughness.
# [star] Excess damage dealt by Destroyer's attacks is placed as threat on the main scheme.
#
# Texte identique a gs176 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDestroyer()
