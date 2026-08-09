from . import *

# * Prehensile Tail
# Resource: Exhaust Prehensile Tail → generate 1 [wild] resource.
#   Spend it only to pay for a Squirrel Girl card.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            for_card=FinderCarteSquirrelGirl(),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
