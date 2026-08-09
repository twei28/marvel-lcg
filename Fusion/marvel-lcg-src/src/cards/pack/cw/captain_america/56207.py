from . import *
def GetAbilities() -> Sequence['Ability']:
    def no_you_move(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        leader = Worlds.FindCardOnField(effect, name='Captain America', card_type=Leader)
        if leader:
            shield = Worlds.FindCardOnField(effect, name="Cap's Shield")
            if shield and (shield.GetBindFace() != leader):
                shield.CastTo(Attachment).AttachTo2(leader, effect)
            def action(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
                if (message.GetDefender() == None):
                    m2.ChangeDealtToTarget(leader, e2)
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, None, action, is_from_attack=message), unregister_after_exec=True, until_event_end=message)
        Faces.DiscardAll([this], effect)
    def check_attacks_you(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        return message.HasTarget(player.GetIdentity())
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Leader, no_you_move, conditions=[check_attacks_you])]
