from . import *

# Dark Lord's Tactics — MANIGANCE ANNEXE. Boost 2, Acceleration, menace de depart 2[per_hero] (natifs, `desc`).
# Each MYSTIC minion gains guard and patrol.
#
# Cartes de reference : skrull_menace/skrull_empire/sk091 (`GiveKeywordToInPlayWhenApplyThis(CardFinder2(trait, Minion), guard=1)`).
# ⚠ Mots-pieges : « EACH MYSTIC minion » : tous les sbires MYSTIC en jeu, y compris ceux qui entrent apres ; guard ET patrol (valeur 1) ; les sbires non MYSTIC n'y gagnent rien.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("MYSTIC", Minion), guard=1, patrol=1),
    ]
