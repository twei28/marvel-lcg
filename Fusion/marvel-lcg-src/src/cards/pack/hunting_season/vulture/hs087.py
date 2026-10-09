from . import *

# hs087 * Gibbon
# Guard (donnees). Forced Interrupt : quand il subirait des degats, en prevenir 1.

def GetAbilities() -> Sequence['Ability']:

    def prevenir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", prevenir),
    ]
