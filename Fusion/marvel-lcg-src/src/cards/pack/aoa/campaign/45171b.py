from . import *
def GetAbilities() -> Sequence['Ability']:
    def mission_team(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        def action(player: 'Player'):
            def draw(targets: Sequence['CardFace']):
                player.DrawUp(1, effect)
            return draw
        choices = [AbilityFactory.ForChoiceAbility(f'Player {player.player_id} draws 1 card', action(player)) for player in Worlds.GetPlayers(effect)]
        initiator.ChooseAbilities(effect, *choices)
    return [AbilityFactory.FirstPlayerControlThis(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, mission_team).SetCostFunc(CostFunc.Exhaust('This'))]
