from . import *
def GetAbilities() -> Sequence['Ability']:
    def double_agent(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes('MainScheme', 2, effect)
        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            this.PlaceThreatOnSchemes('MainScheme', 2, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, double_agent).SetPlay().SetLabel()]
