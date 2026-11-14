from . import *

# * Deathbird (III) — MECHANT, stade 3, expert (Majestrix's Verdict). SHI'AR. PV 21[per_hero], MNG 2, ATQ 3[star].
# Deathbird cannot be defeated, if players do not control Lilandra and the Shi'ar Throne support.
# [star] Forced interrupt: When Deathbird initiates an attack against you, if you control a STARJAMMER
#   ally, she attacks that ally instead. Give her 1 additional boost card for that activation.
#
# Cartes de reference :
#  - « cannot be defeated » : `DeathbirdInvaincue()` (modele 50129a), comme gs115.
#  - Forced interrupt : `AttaqueDetourneeVersStarjammer(boost_sup=1)` (modele 50089b) ; « 1 additional boost
#    card for that activation » : `GiveAdditionalBoostCardForThisActivation(1)` (modele sk100 Emperor's Throne).
#
# ⚠ Mots-pieges : PAS de « +1 ATK » sur ce stade (texte different de I et II) ; la carte de boost
# supplementaire ne vaut que si l'attaque est detournee.


def GetAbilities() -> Sequence['Ability']:
    return [*DeathbirdInvaincue(), AttaqueDetourneeVersStarjammer(boost_sup=1)]
