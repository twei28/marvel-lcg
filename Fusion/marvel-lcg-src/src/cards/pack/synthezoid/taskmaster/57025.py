from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GiveActivatingEnemyAdditionalBoostCard(1, effect)
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        task = Worlds.FindCardOnField(effect, name='Taskmaster', card_type=Minion)
        if task:
            leader = Worlds.GetYourTeamLeader(effect)
            if leader:
                task.DoAttackYou('YourLeader', effect)
            return
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            Faces.GiveStatus([leader], 'Tough', effect)
            Faces.GiveFacedownBoostCards([leader], 1, effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
