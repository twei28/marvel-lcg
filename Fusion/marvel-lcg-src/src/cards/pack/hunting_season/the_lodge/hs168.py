from . import *

# hs168 * Gibbon (Experience Cost 1)
# Interrupt : quand il subirait des degats, en prevenir 1. (Limit once per phase.)

def GetAbilities() -> Sequence['Ability']:

    def prevenir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Interrupt, "This", prevenir).LimitOncePerPhase(),
    ]
