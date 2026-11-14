from . import *

# Mole Man (II) — MECHANT, stade 2. GENIUS. SUBTERRANEAN. SCH 2, ATK 2, PV 7. Toughness.
# [star] Forced Response: After Mole Man attacks you, shuffle a SUBTERRANEAN minion from the encounter
#   discard pile into the encounter deck.
#
# Texte identique a gs186 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesMoleMan()
