from . import *
def GetAbilities() -> Sequence['Ability']:
    def mission_prepped(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)
        def action(player: 'Player'):
            face = Search.PlayerCard(effect, player, include_player_deck=True, include_discard_pile=True, may=True, finder=CardFinder(card_type=Upgrade, cost_equal_or_less=2))
            if face:
                face.CastTo(Upgrade).PutIntoPlay(player, effect, under_control=True)
        Players.ForEachPlayer(effect, action)
    return [AbilityFactory.ThisEnterPlayWithCounters(1, 'prep'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, mission_prepped).SetCostFunc(CostFunc.Counter('This', 1, 'prep')).AnyPlayerCanDoThis()]
