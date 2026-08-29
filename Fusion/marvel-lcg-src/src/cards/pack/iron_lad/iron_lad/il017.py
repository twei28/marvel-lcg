from . import *

# Shadow of the Future — OBLIGATION, give to the Nathaniel Richards player.
# You may flip to alter-ego form. Choose:
# - Remove the top 3 cards of your deck from the game → remove Shadow of
#   the Future from the game.
# - Discard 1 tech card you control. Discard 3 cards from your deck.
#   Discard this obligation.
#
# Modele exact : ok019 Funeral Rites (okoye/okoye/ok019.py), meme structure
# `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
# `player.ChooseAbilities` a 2 branches. Retrait du jeu du dessus du deck :
# `Faces.RemoveAllFromGame(player.player_deck.GetTops(3), effect)` (GetTops
# ne fait que lire, c'est RemoveAllFromGame qui deplace vraiment -- modele
# toafk/kang/11019.py pour la lecture du dessus de deck).

def GetAbilities() -> Sequence['Ability']:

    def shadow_of_the_future(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_du_jeu(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            Faces.RemoveAllFromGame(player.player_deck.GetTops(3), effect)
            Faces.RemoveAllFromGame([this], effect)

        def defausse_partielle(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            tech = CartesTechControlees(player)
            if tech:
                choisie = player.AskChooseFace(tech, effect)
                if choisie:
                    Faces.DiscardAll([choisie], effect)
            player.DiscardDeckTopCards(3, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove the top 3 cards of your deck from the game → remove Shadow of the Future from the game",
                retirer_du_jeu,
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 tech card you control. Discard 3 cards from your deck. Discard this obligation",
                defausse_partielle,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            shadow_of_the_future,
        ),
    ]
