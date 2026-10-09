from . import *

# hs115 The Calypso Serum
# When Revealed : 1[per_hero] menace supplementaire ici. Chaque ennemi gagne +1 SCH et +1 ATK.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenThisRevealed(None, MenaceSupplementaire),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Enemy, attack=1, scheme=1),
    ]
