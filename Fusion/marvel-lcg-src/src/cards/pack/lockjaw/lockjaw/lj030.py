from . import *

# * Central Park — custom « Nugget » (carte d'aspect BASIC)
# Alter-Ego Action: Exhaust Central Park → heal 1 damage from a PET AVENGER
#   or GOOD BOY.


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            soigner,
        ).SetName("Central Park")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Friend, traits=["PET AVENGER", "GOOD BOY"], canbe_heal=True),
    ]
