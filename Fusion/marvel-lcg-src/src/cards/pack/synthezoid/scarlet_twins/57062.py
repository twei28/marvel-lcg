from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        player = message.GetToPlayer()
        hand = list(player.hand_cards.Get())
        if hand:
            def action(chosen: Sequence['CardFace']):
                Faces.DiscardAll(list(chosen), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 1 card from your hand', action).SetTarget(hand, range=(1, 1), not_move=True))
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        faces = list(player.hand_cards.Get())
        if not faces:
            return
        Rand.Shuffle(faces, effect)
        target = faces[0]
        raw = str(target.paper.desc.get('Cost', '0')).rstrip('*')
        cost = int(raw) if raw.isdigit() else 0
        Faces.DiscardAll([target], effect)
        if (cost > 0):
            player.GetIdentity().TakeIndirectDamage(this, cost, effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
