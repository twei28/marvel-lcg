from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        def if_no_activate():
            leader = Worlds.GetEnemyLeader(effect)
            if leader:
                leader.DoActivate(player, effect, do_not_give_boost=True)
        Enemies.AllMinionActivateAgainstEngagedPlayer(effect, if_no_activate=if_no_activate)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
