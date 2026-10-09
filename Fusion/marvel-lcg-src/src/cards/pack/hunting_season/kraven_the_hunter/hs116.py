from . import *

# hs116 Toxic Gas
# When Revealed : 1[per_hero] menace supplementaire ici. Chaque personnage ami gagne -1 ATK.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenThisRevealed(None, MenaceSupplementaire),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero, attack=-1),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Ally, attack=-1),
    ]
