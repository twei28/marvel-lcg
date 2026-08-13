from . import *

# * X-23

def GetAbilities() -> Sequence['Ability']:

    def x_23(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits([this], 2, effect)

    return [
        Reckless(),
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.ForcedResponse,
            "This",
            x_23
        ),
    ]
