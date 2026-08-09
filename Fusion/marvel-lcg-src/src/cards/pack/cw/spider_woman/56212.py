from . import *
def GetAbilities() -> Sequence['Ability']:
    def spider_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='Spider-Woman', card_type=Leader)
        enemy = Worlds.GetEnemyLeader(effect)
        if leader and enemy and (leader != enemy):
            leader.CastTo(Enemy).BasicAttack([enemy], effect)
        if effect.GetPaidResources().HasColor('B'):
            if enemy:
                Faces.GiveStatus([enemy], 'Confused', effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, spider_blast).SetPlay().SetLabel()]
