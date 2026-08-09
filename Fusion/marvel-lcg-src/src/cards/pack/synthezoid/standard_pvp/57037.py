from . import *
def GetAbilities() -> Sequence['Ability']:
    def hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            leader.DoAttackYou(player, effect)
    def ae(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        your_leader = Worlds.GetYourTeamLeader(effect)
        enemy = Worlds.GetEnemyLeader(effect)
        if enemy and your_leader:
            enemy.CastTo(Enemy).BasicAttack([your_leader], effect)
    return [AbilityFactory.WhenThisRevealed('Hero', hero),
            AbilityFactory.WhenThisRevealed('Alter-Ego', ae)]
