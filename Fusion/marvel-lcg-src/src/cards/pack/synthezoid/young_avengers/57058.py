from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        faces = Worlds.GetOnFieldMinions(effect)
        if not (Faces.ResolveAbility(faces, player, AbilityType.WhenRevealed, effect)):
            this.GainSurge(1, effect)
            return
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
