from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            Faces.GiveStatus([leader], 'Tough', effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
