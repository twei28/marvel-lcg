from . import *

# Secret Agent
# Hero Resource: Exhaust Secret Agent -> generate a wild resource.
# Montage repris de Web-Shooter (01008), sans son cout en compteur 'web'.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G")
        ).SetCostFunc(CostFunc.Exhaust("This"))
    ]
