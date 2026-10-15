from . import *

# * Paibok (I) — MECHANT, stade 1 (Paibok). SKRULL. PV 13[per_hero], SCH 1, ATK 2.
# Toughness.
# While the number of POWER SKRULL cards attached to Paibok is equal to or less
#   than the number of mastery counters on him, POWER SKRULL cards cannot be
#   discarded.
#
# Cartes de reference :
#  - Toughness : natif (`desc.Toughness`, fiche mots-cles/toughness.md), aucun module.
#  - « cannot be discarded » : `WhenCardWouldDiscard` + `SetBeInstead` (modele
#    `ih002` / `wd077b`, fenetre `CanBeInstead`, sender_card.py:334). Fabrique
#    commune `RegleDesPouvoirs()` (paibok/__init__.py), identique sur sk141-143.
#
# ⚠ Mots-pieges : « attached TO PAIBOK » (le sbire nemesis de Lyja s'appelle aussi
# Paibok : on compare l'hote, pas le nom) ; « equal to OR LESS » (<=) ; « cannot be
# discarded » ne vise pas les cartes du DECK que « discard until » defausse.


def GetAbilities() -> Sequence['Ability']:
    return [*RegleDesPouvoirs()]
