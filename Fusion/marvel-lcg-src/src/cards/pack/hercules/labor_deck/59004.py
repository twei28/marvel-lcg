from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = message.GetToPlayer()
        face = Search.PlayerCard(effect, player, include_player_deck=True, include_discard_pile=True, include_player_hand_cards=True, name='Amadeus Cho', card_type=Ally)
        if face:
            face.PutIntoPlay(player, effect, under_control=True)
    def protect_humanity(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        identity = player.GetIdentity()
        allies = list(player.allies.Get())
        if not allies:
            return
        def redirect(targets: Sequence['CardFace']):
            target = targets[0]
            def action(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
                if (message.GetDefender() == None):
                    m2.ChangeDealtToTarget(target, e2)
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, None, action, is_from_attack=message), unregister_after_exec=True, until_event_end=message)
            def after_attack():
                if (message.GetDefender() == identity):
                    this.RemoveCountersInternal(1, 'all-purpose', effect)
            RunAt.AfterEventEnd(effect, message, after_attack)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('The villain attacks that ally instead', redirect).SetTarget(allies, range=(1, 1), not_move=True))
    def check_attacks_hercules(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        if not player:
            return False
        identity = player.GetIdentity()
        if not Hero.IsType(identity):
            return False
        return message.HasTarget(identity)
    def after_leave(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetControlByOrOwner()
        if Player.IsType(player):
            Atonement(effect, player)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, protect_humanity, conditions=[check_attacks_hercules]),
            AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, 'This', after_leave).LimitOncePerPhase()]
