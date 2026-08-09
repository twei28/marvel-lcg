from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetToPlayer()
        faces = Worlds.DiscardEncounterCards((3 if Worlds.IsExpert(effect) else 2), effect)
        if Filter.ByType(faces, Treachery):
            Faces.ExhaustAll([player.GetIdentity()], effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
