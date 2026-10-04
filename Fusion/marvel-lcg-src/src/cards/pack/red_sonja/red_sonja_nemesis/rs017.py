from . import *

# Yeti Warrior — MINION, RED SONJA NEMESIS (3/5). SCH 0, ATK 3* (degat
# consequent), HP 6, Boost 0. CREATURE.
# Guard. Toughness. (bases automatiques, lues dans `desc` -- voir `01120`
# Armored Guard, PROCESSUS-CARTE etape 5.)
# [star] Yeti Warrior's attacks gain overkill.
#
# ⚠ L'asterisque sur ATK (« 3★ ») encode `printed_attack_consequential_damage`
# (can_attack.py:48, degat consequent, regle officielle) -- PAS un ajout de
# la valeur de Boost (Boost = 0, aucun badge numerique visible sur le scan).
# Le second « ★ » (dans « [star] Yeti Warrior's attacks gain overkill ») est
# un puce de mise en page du gabarit fan, pas un lien avec le premier :
# capacite PASSIVE et INCONDITIONNELLE (pas de « Boost: » en tete de ligne,
# contrairement a `rs016` Ice Queen).
#
# CARTE DE REFERENCE : `AbilityFactory.UnitAttackGainKeyword("This",
# overkill=True)` (do_attack.py:828), sans condition -- permanent.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            overkill=True,
        ),
    ]
