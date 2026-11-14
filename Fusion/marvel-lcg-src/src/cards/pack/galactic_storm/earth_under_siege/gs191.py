from . import *

# Veranke (II) — MECHANT, stade 2. SKRULL. SCH 3, ATK 1, PV 7. Toughness.
# [star] Players cannot defend against Veranke's attacks.
#
# Texte identique a gs190 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesVeranke()
