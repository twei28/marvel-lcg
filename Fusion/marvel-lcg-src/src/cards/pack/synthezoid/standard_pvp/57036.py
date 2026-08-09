from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            prop = None
            if (len(Worlds.GetPlayers(effect)) > 1):
                prop = SchemeProperty(give_additional_boost=1)
            leader.DoSchemes(player, effect, property=prop)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
