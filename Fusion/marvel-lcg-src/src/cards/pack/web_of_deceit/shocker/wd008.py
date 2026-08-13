from . import *

# * Vulture

def GetAbilities() -> Sequence['Ability']:

    def vautour(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        # « discard 1 random card from your hand unless your identity has the
        # AERIAL trait. »
        joueur = message.GetToPlayer()
        if joueur.GetIdentity().HasTrait("AERIAL"):
            return
        joueur.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            vautour
        ),
    ]
