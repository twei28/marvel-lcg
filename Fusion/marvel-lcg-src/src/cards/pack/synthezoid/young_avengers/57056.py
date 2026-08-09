from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        upgrades = [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if (f.GetControlByPlayer() == player)]
        if upgrades:
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard an upgrade you control', action).SetTarget(upgrades, range=(1, 1), not_move=True))
    return [AbilityFactory.UnitAttackGainKeyword('This', piercing=True, ranged=True),
            AbilityFactory.WhenThisRevealed(None, when_revealed)]
