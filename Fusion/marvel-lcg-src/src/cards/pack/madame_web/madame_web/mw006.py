from . import *

# Weaving a Web — custom « Kajislav »
# Resource: Exhaust Weaving a Web -> generate a [wild] resource for an ally.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            CardFinder(card_type=Ally)
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
