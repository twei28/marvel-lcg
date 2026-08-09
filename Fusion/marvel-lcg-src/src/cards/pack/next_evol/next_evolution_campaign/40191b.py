from . import *
def GetAbilities() -> Sequence['Ability']:
    def safehouse_established(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)
        player = Worlds.GetFirstPlayer(effect)
        card = CardFactory.GenerateCard('40197', player.additional_discard_pile, effect.world)
        card.face.CastTo(Support).PutIntoPlay(player, effect, under_control=True)
    return [AbilityFactory.ThisEnterPlayWithCounters(1, 'safehouse'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, safehouse_established).SetCostFunc(CostFunc.Counter('This', 1, 'safehouse')).AnyPlayerCanDoThis()]
