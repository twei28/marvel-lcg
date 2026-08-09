from . import *
def GetAbilities() -> Sequence['Ability']:
    def cho_redirect(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        def action(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
            if (message.GetDefender() == None):
                m2.ChangeDealtToTarget(this, e2)
        this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, None, action, is_from_attack=message), unregister_after_exec=True, until_event_end=message)
    def check_attacks_you(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        return message.HasTarget(player.GetIdentity())
    def draw(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.GetControlByPlayer().DrawUp(1, effect)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Minion, cho_redirect, conditions=[check_attacks_you]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, draw).SetCostFunc(CostFunc.Exhaust('This'))]
