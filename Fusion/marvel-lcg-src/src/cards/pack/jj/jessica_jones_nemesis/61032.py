from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        for card in Worlds.FindCardsOnField(effect, name='Suggestion'):
            card.PlaceCountersInternal(2, 'pheromone', effect)
    def check_suggestion(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        return bool(message.trigger.name and 'Suggestion' in message.trigger.name)
    def forced_response(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        message.trigger.PlaceCountersInternal(2, 'pheromone', effect)
    return [
        AbilityFactory.WhenThisRevealed(None, when_revealed),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, None, forced_response, conditions=[check_suggestion]),
    ]
