from . import *
def GetAbilities() -> Sequence['Ability']:
    def iron_fist(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        amount = this.attack
        def prevent(inner_effect: 'Effect', damage_message: 'Message.WhenUnitWouldTakeDamage') -> None:
            damage_message.PreventDamage(amount, effect)
        effect.this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                None,
                prevent,
                is_from_attack=message.would_atk_message,
            ),
            unregister_after_exec=False,
            until_event_end=message.would_atk_message,
        )
    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(AbilityType.Interrupt, "This", iron_fist),
    ]
