from . import *

# * The Eye of Agamotto — custom « DesignHacker » (Age of Khonshu)
# Linked (Doctor Strange) : mis en jeu par le When Defeated de 76017.
# Resource: Exhaust The Eye of Agamotto and remove 1 mystic counter from it →
#   generate 2 [wild] resources.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("GG"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'mystic')),
    ]
