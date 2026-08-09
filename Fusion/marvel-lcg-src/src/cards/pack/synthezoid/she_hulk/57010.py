from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        player = message.GetToPlayer()
        characters = [player.GetIdentity()] + list(player.allies.Get())
        targets = [x for x in characters if x.card.IsReady()]
        if targets:
            def action(chosen: Sequence['CardFace']):
                Faces.ExhaustAll(list(chosen), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Exhaust a character you control', action).SetTarget(targets, range=(1, 1), not_move=True))
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        faces = [f for f in player.GetControlCharacters() if f.card.state.is_ready]
        if not faces:
            this.GainSurge(1, effect)
            return
        Faces.ExhaustAll(faces, effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
