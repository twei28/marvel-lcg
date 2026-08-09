from . import *

# * Wolverine — custom « Kajislav » (sbire némésis d'Albert)
# Forced Response: After you attack Wolverine, heal 1 damage from him.
# [star] Boost: Put this minion into play engaged with the Albert player.

def GetAbilities() -> Sequence['Ability']:

    def healing_factor(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        this.HealthUnits([this], 1, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "You",
            healing_factor,
            against_who="This",
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
