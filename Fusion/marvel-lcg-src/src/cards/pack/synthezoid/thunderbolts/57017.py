from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            Faces.GiveStatus([leader], 'Stunned', effect)
            return
        player = message.GetToPlayer()
        Faces.GiveStatus([player.GetIdentity()], 'Stunned', effect)
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.GetYourTeamLeader(effect)
        if leader:
            Faces.GiveStatus([leader], 'Stunned', effect)
        else:
            Faces.GiveStatus([player.GetIdentity()], 'Stunned', effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
