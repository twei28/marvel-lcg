from . import *

# * Tuning Fork — custom « Nugget »
# You may play LOCATION supports from your discard pile during your turn
#   (paying their resource costs).
# Resource: Exhaust Tuning Fork → generate a [wild] resource.
#
# La première capacité reprend celle de l'allié officiel Lockjaw (05018), à une
# nuance près : `during="YourTurn"` est refusé par le moteur dès que la carte
# visée n'est pas « This » (assert dans `YouMayPlayCardLikeInHand`). La clause
# est donc omise — sans effet pratique, le moteur n'autorisant à jouer un
# soutien que pendant son propre tour. La seconde capacité est la source de la
# ressource « os » du pack.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.NonKeyword,
            CardFinder2("LOCATION", Support),
            from_where="YourDiscardPile",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
