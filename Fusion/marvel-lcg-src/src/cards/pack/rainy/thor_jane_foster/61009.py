from . import *

# Congress of Worlds — custom "Rainy"
# Alter-Ego Action: Exhaust Congress of Worlds and spend 1 resource of any
# type -> remove 2 threat from the main scheme or 3 threat from a side scheme.

def GetAbilities() -> Sequence['Ability']:

    def congress_of_worlds(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        for scheme in effect.targets:
            if MainScheme.IsType(scheme):
                this.RemoveThreatFromSchemes([scheme], 2, effect)
            else:
                this.RemoveThreatFromSchemes([scheme], 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            congress_of_worlds
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Spend(Cost("1")))
        .SetTarget(Scheme2)
    ]
