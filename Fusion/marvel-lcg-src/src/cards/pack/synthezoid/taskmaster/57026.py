from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        leader = Worlds.GetEnemyLeader(effect)
        if leader:
            Faces.GiveStatus([leader], 'Tough', effect)
            Faces.GiveFacedownBoostCards([leader], 1, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
