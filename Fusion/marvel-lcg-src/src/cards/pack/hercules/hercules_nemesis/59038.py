from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        value = len(Worlds.FindCardsOnField(effect, trait='OLYMPUS'))
        if (value > 0):
            this.PlaceThreatOnSchemes([this], value, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
