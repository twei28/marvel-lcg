from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        faces = Worlds.DiscardEncounterCards(3, effect)
        if Filter.ByType(faces, Treachery):
            player.GetIdentity().TakeIndirectDamage(this, 2, effect)
    def defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        PlaceSynergyCounters('Domineering Force', 1, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            WhenDefeatedPlaceShatterCountersOnTheAvatarOfLokivillain(3, defeated)]
