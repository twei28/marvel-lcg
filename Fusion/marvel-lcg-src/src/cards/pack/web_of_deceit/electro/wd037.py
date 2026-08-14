from . import *

# * Electro (III)

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        # « Forced Response: After Electro activates against you, discard cards
        # from the top of the encounter deck until a treachery with 1 or more
        # boost icons is discarded. Then, discard an equal number of cards from
        # the top of your deck. »
        #
        # « an equal number » se lit sur la traitrise trouvee : autant de cartes
        # que d'icones de boost qu'elle porte. C'est le seul nombre que la
        # phrase vient de nommer.
        traitrise = DefausserJusquAUneTraitrise(effect, avec_boost=True)
        if traitrise is None:
            return
        joueur = message.GetToPlayer()
        joueur.DiscardDeckTopCards(traitrise.CastTo(HasBoostIcon).printed_boost, effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            decharge
        ),
    ]
