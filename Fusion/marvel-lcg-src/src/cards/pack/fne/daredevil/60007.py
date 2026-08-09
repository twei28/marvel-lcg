from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_this(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        return (effect.this == message.trigger)
    def check_hero_form(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        this = effect.this.CastTo(Ally)
        return this.GetControlByPlayer().IsInHeroForm()
    def elektra(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        message.SetBeInstead(effect)
        identity = this.GetControlByPlayer().GetIdentity()
        identity.CastTo(Unit2).TakeDamage(this, message.will_take_damage, effect)
    return [Ability(AbilityType.ForcedInterrupt, Message.WhenAllyWouldTakeConsequentialDamage, [check_this, check_hero_form], elektra, is_local=True)]
