from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        def action(player: 'Player'):
            faces = list(player.hand_cards.Get())
            if not faces:
                return
            Rand.Shuffle(faces, effect)
            this.TuckCardUnderHere(faces[0], effect)
        Players.ForEachPlayer(effect, action)
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        faces = list(this.GetPlacedCardArea().Get())
        if faces:
            Faces.ReturnToHand(faces, 'Owner', effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
