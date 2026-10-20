from . import *

# * Korvus (Korvus Rook'shir) — ALLIE (BASIC / Majestrix's Verdict), cout 3 [energy]. SHI'AR. STARJAMMER.
# PV 5, CTR 1 (1 degat consecutif), ATQ 3[star] (2 degats consecutifs).
# [star] Korvus's attacks gain overkill.
#
# Cartes de reference :
#  - « X's attacks gain overkill » : `UnitAttackGainKeyword("This", overkill=True)` (RECETTES §3, 27078/ho016).
#  - icone [energy] : carre jaune « eclair », verifie par decoupe contre sk008 (RES=Y, meme auteur).
#
# ⚠ Mots-pieges : deux etoiles a contour sous l'ATQ = 2 degats consecutifs (`ATK` = "3**").


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", overkill=True)]
