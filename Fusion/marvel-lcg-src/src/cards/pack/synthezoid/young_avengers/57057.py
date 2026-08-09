from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        supports = list(player.supports.Get())
        if supports:
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a support you control', action).SetTarget(supports, range=(1, 1), not_move=True))
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
