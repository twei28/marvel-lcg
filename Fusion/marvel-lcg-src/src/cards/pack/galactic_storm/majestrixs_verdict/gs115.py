from . import *

# * Deathbird (II) — MECHANT, stade 2 (Majestrix's Verdict). SHI'AR. PV 19[per_hero], MNG 2, ATQ 3[star].
# Deathbird cannot be defeated, if players do not control Lilandra and the Shi'ar Throne support.
# [star] Forced interrupt: When Deathbird initiates an attack against you, if you control a STARJAMMER
#   ally, she attacks that ally instead with +1 ATK.
#
# Cartes de reference :
#  - « cannot be defeated, if ... » : `UnitCannotBeDefeatedWhile` (modele 50129a Citizen V, 35029 Omega Red),
#    helper `DeathbirdInvaincue()` ; `change_on_event` relance la defaite quand Lilandra ou le Trone change de
#    zone (Deathbird restee a 0 PV tombe des que la condition est remplie).
#  - Forced interrupt : identique a gs114 (`AttaqueDetourneeVersStarjammer(bonus_atq=1)`, modele 50089b).
#
# ⚠ Mots-pieges : « players do not control Lilandra AND the Shi'ar Throne SUPPORT » : les DEUX, en jeu sous
# le controle de joueurs ; la face manigance du Trone ne compte pas.


def GetAbilities() -> Sequence['Ability']:
    return [*DeathbirdInvaincue(), AttaqueDetourneeVersStarjammer(bonus_atq=1)]
