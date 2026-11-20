from . import *

# * Corsair (Christopher Summers) — ALLIE (BASIC / Majestrix's Verdict), cout 3 [energy]. STARJAMMER.
# PV 4, CTR 2 (1 degat consecutif), ATQ 2[star] (1 degat consecutif).
# [star] Corsair's attacks gain ranged.
#
# Cartes de reference :
#  - « X's attacks gain ranged » : `UnitAttackGainKeyword("This", ranged=True)` (RECETTES §3, modele 27078 /
#    ho016 pour la fabrique ; `attacker="This"` pour ne pas toucher un homonyme).
#  - icone [energy] : carre jaune « eclair », verifie par decoupe contre sk008 (RES=Y, meme auteur).
#
# ⚠ Mots-pieges : « attacks » = toutes ses attaques (pas seulement l'attaque de base).


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", ranged=True)]
