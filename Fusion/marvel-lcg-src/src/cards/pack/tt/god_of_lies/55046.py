from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        PlaceShatterCountersOnTheAvatarOfLokivillain(3, effect)
        for name in ('Unified Front', 'Mounting Resistance', 'Domineering Force', 'Feigned Retreat'):
            face = Worlds.FindCardOnField(effect, name=name, card_type=Environment)
            if face and (face.CastTo(CanPlaceCounter).GetCounters('synergy') < Worlds.GetPlayerNumIcon(effect)):
                PlaceSynergyCounters(name, 1, effect)
                break
    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
