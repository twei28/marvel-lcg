from . import *


def GetAbilities() -> Sequence['Ability']:

    def end_of_the_line(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        player = message.GetToPlayer()
        discarded = Worlds.DiscardEncounterCards(8, effect)
        RevealDiscardedInvisibleNemesisCards(effect, discarded, player)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            end_of_the_line,
        ).SetName("End of the Line"),
    ]
