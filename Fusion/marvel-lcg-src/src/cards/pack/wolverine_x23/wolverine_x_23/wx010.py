from . import *

# Grim Resolve
# Resource: Exhaust this card and take 1 damage -> generate a [wild] resource.
#
# Copie de Grim Resolve (43010), sans adaptation : aucune reference a un nom.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G")
        ).SetCostFunc(CostFunc.TakeDamage(1, "Initiator"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
