from . import *

# * Blade

def GetAbilities() -> Sequence['Ability']:

    def blade(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits([this], 2, effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Minion,
            blade,
            has_excess_damage=False,
        ),
    ]
