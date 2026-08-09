from . import *

# * Stark Resilient

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        # « for any player » : la ressource generee sert a n'importe qui.
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G")
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
