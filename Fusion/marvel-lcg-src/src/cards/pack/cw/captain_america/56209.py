from . import *
def GetAbilities() -> Sequence['Ability']:
    def recruited_by_cap(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        for minion in effect.targets:
            for player in Worlds.GetPlayers(effect):
                if (player != initiator):
                    Faces.MoveAllTo([minion], player.engaged_minions, effect)
                    return
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, recruited_by_cap).SetPlay().SetLabel().SetTarget('YourEngagedMinions')]
