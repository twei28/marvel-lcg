from . import *
def GetAbilities() -> Sequence['Ability']:
    def she_hulk_smash(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        leader = Worlds.FindCardOnField(effect, name='She-Hulk', card_type=Leader)
        enemy = Worlds.GetEnemyLeader(effect)
        if leader and enemy and (leader != enemy):
            leader.CastTo(Enemy).BasicAttack([enemy], effect)
        if effect.GetPaidResources().HasColor('R'):
            if enemy:
                Faces.GiveStatus([enemy], 'Stunned', effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, she_hulk_smash).SetPlay().SetLabel()]
