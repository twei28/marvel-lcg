from . import *

# Limitless Strength

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Hulk"),
            attack=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("R")
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
