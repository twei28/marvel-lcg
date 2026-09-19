from . import *

# Endgame (2B) — 0[per_hero] depart, 7[per_hero] cible, +1[per_hero].
# Each minion gains guard.
# If this stage is completed, the players lose the game.
# Modele : 60097 Purple Man (GiveKeywordToInPlayWhenApplyThis, liste).

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Minion), guard=1),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
