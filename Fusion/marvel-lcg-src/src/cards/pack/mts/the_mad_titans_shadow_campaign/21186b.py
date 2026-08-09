from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_odin(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        odin = Worlds.FindCardOnField(effect, name='Odin')
        if odin and (odin.GetControlByPlayer() == Worlds.GetFirstPlayer(effect)):
            return False
        return True
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        odin = Worlds.FindCardOnField(effect, name='Odin')
        if odin:
            odin.CastTo(CanHealth).HealHealth('All', effect)
            odin.FlipTo(effect, trait='KING')
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_odin]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
