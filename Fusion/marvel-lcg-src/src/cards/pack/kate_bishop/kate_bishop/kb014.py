from . import *

# Family = Trouble — OBLIGATION, give to the Kate Bishop player.
# You may flip to alter-ego form. Choose:
# - Find the hero-specific Hawkeye ally and remove it from the game -> remove
#   Family = Trouble from the game.
# - Remove all arrow counters from Kate's Bow. You cannot place arrow
#   counters on Kate's Bow until the end of the next round. Discard this
#   obligation.
#
# TODO connu (limite moteur) : la deuxieme option retire bien tous les
# compteurs et defausse l'obligation, mais la clause « you cannot place
# arrow counters on Kate's Bow until the end of the next round » N'EST PAS
# implementee -- aucun equivalent a "AbilityFactory.PlayersCannotPlaceCounter"
# n'existe dans ce depot (grep infructueux sur CannotPlace/PlayersCannotPlace
# dans game/ability/factory/). L'ajouter proprement demanderait d'intercepter
# TOUTES les cartes qui posent des compteurs 'arrow' sur Kate's Bow (Quick
# Draw, Lucky, Kate's Quiver, Tandem Archery, l'ally Hawkeye, Kate's Bow
# lui-meme), pas seulement celle-ci -- hors budget de cette session. Seul le
# texte de la carte porte cette clause pour l'instant.
#
# Modele : Criminal Past (trors/hawkeye/04026.py), meme structure de choix
# (YouMayFlipToYourAlterEgoForm + player.ChooseAbilities avec 2 options).


def GetAbilities() -> Sequence['Ability']:

    def family_is_trouble(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_lallie(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                include_discard_pile=True,
                card_type=Ally,
                name="Hawkeye",
            )
            if face:
                Faces.RemoveAllFromGame([face], effect)
            Faces.RemoveAllFromGame([this], effect)

        def verrouiller_les_fleches(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            arc = TrouverArcEnJeu(effect)
            if arc:
                Faces.RemoveCountersOn([arc], "All", 'arrow', effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Find the hero-specific Hawkeye ally and remove it from the game → remove Family = Trouble from the game",
                retirer_lallie,
            ),
            AbilityFactory.ForChoiceAbility(
                "Remove all arrow counters from Kate's Bow. You cannot place arrow counters on Kate's Bow until the end of the next round. Discard this obligation",
                verrouiller_les_fleches,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            family_is_trouble,
        ),
    ]
