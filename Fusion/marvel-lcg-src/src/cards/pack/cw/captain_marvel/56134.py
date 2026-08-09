from . import *
def GetAbilities() -> Sequence['Ability']:
    def you_started_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='Captain Marvel', card_type=Leader)
        enemy = Worlds.GetEnemyLeader(effect)
        if leader and enemy and (leader != enemy):
            leader.CastTo(Enemy).BasicAttack([enemy], effect)
        if effect.GetPaidResources().HasColor('Y'):
            if enemy:
                Faces.GiveStatus([enemy], 'Confused', effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, you_started_this).SetPlay().SetLabel()]
