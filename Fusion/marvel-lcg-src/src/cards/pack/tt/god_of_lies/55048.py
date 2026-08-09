from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        PlaceShatterCountersOnTheAvatarOfLokivillain(3, effect)
        PlaceSynergyCounters('Feigned Retreat', 1, effect)
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
