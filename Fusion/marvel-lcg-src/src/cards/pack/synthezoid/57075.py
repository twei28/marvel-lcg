from . import *
def GetAbilities() -> Sequence['Ability']:
    def synthezoid_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='Vision', card_type=Leader)
        enemy = Worlds.GetEnemyLeader(effect)
        if leader and enemy and (leader != enemy):
            leader.CastTo(Enemy).BasicAttack([enemy], effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, synthezoid_strike).SetPlay().SetLabel()]
