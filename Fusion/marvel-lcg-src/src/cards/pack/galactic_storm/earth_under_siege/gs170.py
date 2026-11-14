from . import *

# Attuma (I) — MECHANT, stade 1. ATLANTIS. SCH 1, ATK 2, PV 6.
# [star] While another ATLANTIS card is in play, Attuma gets +1 SCH and +1 ATK.
#
# Cartes de reference :
#  - « While another ATLANTIS card is in play, gets +1 X » : `AbilityFactory.ThisGainKeyword(check_fn,
#    attack=1, scheme=1)` (modele nebu/22013.py, `check_fn` conditionnel qui rend 0 ou 1).
#
# ⚠ Mots-pieges : « ANOTHER Atlantis card » exclut Attuma lui-meme (il porte le trait ATLANTIS) : le
# check_fn doit chercher une carte ATLANTIS AUTRE que This, pas juste « une carte ATLANTIS existe ».


def GetAbilities() -> Sequence['Ability']:
    return CapacitesAttuma()
