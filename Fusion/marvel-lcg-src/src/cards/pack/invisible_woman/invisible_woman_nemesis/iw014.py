from . import *


def GetAbilities() -> Sequence['Ability']:

    def psycho_man(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        player = message.GetToPlayer()
        discarded = Worlds.DiscardEncounterCards(4, effect)
        RevealDiscardedInvisibleNemesisCards(effect, discarded, player)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            psycho_man,
        ).SetName("Emotional Manipulation"),
    ]
