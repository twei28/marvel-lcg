from . import *

# Attuma (II) — MECHANT, stade 2. ATLANTIS. SCH 2, ATK 2, PV 7. Toughness.
# [star] While another ATLANTIS card is in play, Attuma gets +1 SCH and +1 ATK.
#
# Texte identique a gs170 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesAttuma()
