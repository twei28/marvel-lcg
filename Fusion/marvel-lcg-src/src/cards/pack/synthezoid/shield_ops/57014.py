from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], 'Tough', effect)
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        targets = []
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            targets.append(leader)
        targets += Worlds.FindCardsOnField(effect, card_type=Minion)
        if targets:
            Faces.GiveStatus(targets, 'Tough', effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
