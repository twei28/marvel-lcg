from . import *

# * Webb's Apartment — custom « Kajislav »
# Alter-Ego Action: Exhaust Webb's Apartment -> heal 1 damage from a character
#   you control.

def GetAbilities() -> Sequence['Ability']:

    def appartement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            appartement
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YouControlUnit", canbe_heal=True),
    ]
