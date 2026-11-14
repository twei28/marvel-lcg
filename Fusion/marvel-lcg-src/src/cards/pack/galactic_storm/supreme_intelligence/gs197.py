from . import *

# * Supreme Intelligence (III) — MECHANT (Supreme Intelligence, expert). KREE. SCH 3, ATK 2, 15[per_hero] PV.
# Toughness.
# Forced Response: After a KREE minion is defeated, heal 1 damage from the villain and give it a facedown
#   boost card.
#
# Cartes de reference : **`gs195`** (helper `ReponseSbireKreeVaincu`, ici SANS condition ELITE) ; Toughness =
# base automatique.
#
# ⚠ Mots-pieges : « give IT a facedown boost card » = le mechant (le sbire est vaincu) ; AUCUNE condition de
# trait au stade III, chaque sbire KREE vaincu donne la carte de boost.


def GetAbilities() -> Sequence['Ability']:
    return [ReponseSbireKreeVaincu(boost_si_elite_seulement=False)]
