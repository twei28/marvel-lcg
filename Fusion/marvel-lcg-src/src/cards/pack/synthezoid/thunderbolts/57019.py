from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            leader.CastTo(Unit2).TakeDamage(this, 2, effect)
            return
        player = message.GetToPlayer()
        characters = [player.GetIdentity()] + list(player.allies.Get())
        def action(chosen: Sequence['CardFace']):
            for face in chosen:
                face.CastTo(Unit2).TakeDamage(this, 1, effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal 1 damage to a character you control', action).SetTarget(characters, range=(1, 1), not_move=True))
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            this.DealDamage([leader], 2, effect)
            return
        faces = player.GetControlCharacters()
        if faces:
            def action(targets: Sequence['CardFace']):
                this.DealDamage(list(targets), 2, effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal 2 damage to a character you control', action).SetTarget(list(faces), range=(1, 1), not_move=True))
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
