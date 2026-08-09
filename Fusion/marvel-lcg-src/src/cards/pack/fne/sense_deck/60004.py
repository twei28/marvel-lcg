from . import *
def GetAbilities() -> Sequence['Ability']:
    def reduce_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        attacker = message.trigger
        SenseDiscard(this, effect)
        attacker.CastTo(Unit2).GainForThisActive(effect, message, attack=-3)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity() if player else None
        if identity:
            def redirect(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
                if (message.GetDefender() == None) and (m2.trigger != identity):
                    m2.ChangeDealtToTarget(identity, e2)
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, None, redirect, is_from_attack=message), unregister_after_exec=True, until_event_end=message)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy)),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, None, reduce_attack, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)])]
