from . import *

# * Wolverine

def GetAbilities() -> Sequence['Ability']:

    def wolverine(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits([this], 2, effect)

    return [
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.ForcedResponse,
            "This",
            wolverine
        ),
    ]
