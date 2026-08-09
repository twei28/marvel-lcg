from . import *
def GetAbilities() -> Sequence['Ability']:
    def phase_end(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.PlaceCountersOn([this], 1, 'crash', effect)
        if (this.GetCounters('crash') >= 2):
            def action(player: 'Player'):
                CardFactory.GenerateCard('21185', player.hand_cards, effect.world)
            Players.ForEachPlayer(effect, action)
            Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.WhenPlayerPhaseEnd(AbilityType.ForcedInterrupt, phase_end)]
