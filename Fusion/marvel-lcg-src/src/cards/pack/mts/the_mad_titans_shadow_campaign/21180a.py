from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.card.Flip(effect)
        face = this.card.face
        player = Worlds.GetFirstPlayer(effect)
        face.CastTo(Ally).PutIntoPlay(player, effect, under_control=True)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
