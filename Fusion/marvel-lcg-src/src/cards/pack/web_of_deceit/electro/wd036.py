from . import *

# * Electro (II)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Discard cards from the top of the encounter deck
        # until a copy of A.I.M. Scientist is discarded. Put it into play
        # engaged with the first player. »
        #
        # ⚠ DEUX cartes portent ce nom quand le modulaire A.I.M. Science est de
        # la partie : celle du set Electro et l'officielle 50083. C'est voulu —
        # le texte dit « a copy of », et sur la table les deux en sont une.
        savant = Worlds.DiscardEncounterCardsUntil(
            effect,
            name="A.I.M. Scientist",
            card_type=Minion,
        )
        if savant:
            savant.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)

    def decharge(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        # « Forced Response: After Electro activates against you, discard cards
        # from the top of the encounter deck until a treachery is discarded. »
        DefausserJusquAUneTraitrise(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            decharge
        ),
    ]
