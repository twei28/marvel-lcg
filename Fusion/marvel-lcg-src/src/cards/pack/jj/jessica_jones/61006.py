from . import *
def GetAbilities() -> Sequence['Ability']:
    def snooping_around(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        if alias:
            alias.PlaceCountersInternal(2, 'evidence', effect)
        faces = Worlds.DiscardEncounterCards(1, effect)
        for face in faces:
            if Minion.IsType(face) or EncounterSideScheme.IsType(face):
                face.Reveal(effect.GetInitiator(), effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, snooping_around)
        .SetPlay().SetLabel('thwart').SetTarget(Scheme2, range=(1, 1)),
    ]
