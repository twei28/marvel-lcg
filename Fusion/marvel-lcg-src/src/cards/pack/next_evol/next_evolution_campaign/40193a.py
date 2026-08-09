from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        this.card.Flip(effect)
        face = this.card.face
        face.CastTo(Environment).Reveal(Worlds.GetFirstPlayer(effect), effect)
    return [AbilityFactory.CanPlayThisSchemeCard(),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
