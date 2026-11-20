from . import *

# * Hepzibah — ALLIE (BASIC / Majestrix's Verdict), cout 3 [physical]. STARJAMMER.
# PV 3, CTR 2 (1 degat consecutif), ATQ 3[star] (1 degat consecutif).
# [star] Hepzibah's attacks gain piercing.
#
# Cartes de reference :
#  - « X's attacks gain piercing » : `UnitAttackGainKeyword("This", piercing=True)` (RECETTES §3, 27078/ho016).
#  - icone [physical] : carre rouge « poing », verifie par decoupe contre sk004 (RES=R, meme auteur).
#
# ⚠ Mots-pieges : « attacks » = toutes ses attaques.


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", piercing=True)]
