from . import *
def GetAbilities() -> Sequence['Ability']:
    def geared_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)
        def action(player: 'Player'):
            CardFactory.GenerateCard('40196', player.player_deck, effect.world)
            player.player_deck.Shuffle(effect)
        Players.ForEachPlayer(effect, action)
    return [AbilityFactory.ThisEnterPlayWithCounters(1, 'pouch'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, geared_up).SetCostFunc(CostFunc.Counter('This', 1, 'pouch')).AnyPlayerCanDoThis()]
