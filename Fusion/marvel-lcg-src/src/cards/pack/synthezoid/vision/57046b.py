from . import *
def GetAbilities() -> Sequence['Ability']:
    def reduce_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)
    def check_vision(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return (message.trigger == effect.this.bind_face)
    return [AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, None, reduce_damage, conditions=[check_vision])]
