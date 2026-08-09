from . import *
def GetAbilities() -> Sequence['Ability']:
    def team_assembled(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)
        def action(player: 'Player'):
            face = Search.PlayerCard(effect, player, include_player_deck=True, include_discard_pile=True, may=True, finder=CardFinder(card_type=Ally, cost_equal_or_less=3))
            if face:
                face.CastTo(Ally).PutIntoPlay(player, effect, under_control=True)
        Players.ForEachPlayer(effect, action)
    return [AbilityFactory.ThisEnterPlayWithCounters(1, 'assembly'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, team_assembled).SetCostFunc(CostFunc.Counter('This', 1, 'assembly')).AnyPlayerCanDoThis()]
