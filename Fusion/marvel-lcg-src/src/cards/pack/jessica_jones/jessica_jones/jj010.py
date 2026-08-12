from . import *

# * Jessica's Jacket — custom « ekAugust »
# You get +2 hit points.
# Interrupt: When you would take any amount of damage, exhaust Jessica's Jacket
#   -> prevent 1 of that damage and remove 1 threat from a scheme.

def GetAbilities() -> Sequence['Ability']:

    def jessicas_jacket(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        message.PreventDamage(1, effect)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
        ),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            jessicas_jacket,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
    ]
