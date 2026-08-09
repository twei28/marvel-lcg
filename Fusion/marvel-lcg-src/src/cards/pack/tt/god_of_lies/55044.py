from . import *
def GetAbilities() -> Sequence['Ability']:
    def defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        PlaceSynergyCounters('Unified Front', 1, effect)
    def after_attacked(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        attacker = message.attacker
        faces = Worlds.DiscardEncounterCards(1, effect)
        if Filter.ByType(faces, Treachery):
            Faces.GiveStatus([attacker], 'Stunned', effect)
    return [WhenDefeatedPlaceShatterCountersOnTheAvatarOfLokivillain(3, defeated),
            AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, (CardFinder(card_type=Hero) | CardFinder(card_type=Ally)), 'This', after_attacked)]
