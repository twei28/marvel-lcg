from . import *
def GetAbilities() -> Sequence['Ability']:
    def character_defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 2, effect)
    def check_character(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        trigger = message.trigger
        return Unit2.IsType(trigger)
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.MoveAllTo([this], effect.world.aside_deck, effect)
    return [AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, None, character_defeated, conditions=[check_character]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
