from . import *
def GetAbilities() -> Sequence['Ability']:
    def miscreant(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Villain)
        this.PlaceThreatOnSchemes('MainScheme', 1, effect)
        scheme = Worlds.FindCardOnField(effect, card_type=EncounterSideScheme)
        if scheme:
            this.PlaceThreatOnSchemes([scheme], 1, effect)
    return [AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, 'This', AvatarWouldBeDefeated),
            AbilityFactory.WhenPlayerRevealCard(AbilityType.ForcedResponse, 'AnyPlayer', Treachery, 'WhenRevealed', miscreant, from_encounter=True)]
