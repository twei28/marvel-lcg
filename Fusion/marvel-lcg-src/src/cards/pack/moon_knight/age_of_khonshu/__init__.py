from cards.pack import *

# Set modulaire custom « Age of Khonshu » (DesignHacker, pack Moon Knight).
#
# Quatre héros corrompus en sbires ELITE ; chacun, vaincu, donne son artefact
# au joueur qui l'a terrassé (« Linked (X) »). Les quatre artefacts (mk021 à
# mk024) ne sont dans AUCUN deck : ils sont créés à la volée au moment du
# When Defeated (CardFactory.GenerateCard, modèle de la campagne trors), puis
# mis en jeu sous le contrôle du joueur.


def DonnerArtefact(effect: 'Effect', message: 'Message.WhenUnitBeDefeated',
                   card_id: str) -> None:
    from game.card.factory import CardFactory

    player = message.defeating_player
    if player is None:
        # Vaincu sans joueur attribuable (retrait direct...) : pas d'artefact.
        return

    card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
    card.face.PutIntoPlay(player, effect)


def CapaciteArtefactLie(card_id: str) -> 'Ability':
    """When Defeated : le joueur qui a vaincu met l'artefact lié en jeu."""
    def when_defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        DonnerArtefact(effect, message, card_id)

    return AbilityFactory.WhenUnitBeDefeated(
        AbilityType.WhenDefeated,
        "This",
        when_defeated,
        has_defeating_player=True,
    )
