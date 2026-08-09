from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        player = message.GetToPlayer()
        upgrades = [x for x in Worlds.FindCardsOnField(effect, card_type=Upgrade) if Player.IsType(x.GetControlBy()) and (x.GetControlByPlayer() == player)]
        if upgrades:
            def action(chosen: Sequence['CardFace']):
                Faces.DiscardAll(list(chosen), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard an upgrade you control', action).SetTarget(upgrades, range=(1, 1), not_move=True))
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        faces = ([f for f in player.allies.Get()] + [f for f in player.supports.Get()] + [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if (f.GetControlByPlayer() == player)])
        if not faces:
            this.GainSurge(1, effect)
            return
        best = max(faces, key=lambda f: int(str(f.paper.desc.get('Cost', '0')).rstrip('*') or 0))
        Faces.DiscardAll([best], effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
