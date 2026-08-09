from . import *

# * Amadeus Cho (face alter-ego) — custom « Rainy »
# Mastermind Excello — Action: Look at the top 2 cards of your deck. Place one
#   of those in your reserve and the other on the top or bottom of your deck.
#   (Limit once per round.)
#
# `LookAtDeck` rend les cartes du dessus SANS les sortir du deck : c'est bien
# « regarder ». Le choix passe ensuite par `MayChooseFace` et non par un
# selecteur de cibles — leçon du pack squirrel_girl : un selecteur ne restreint
# pas les cartes hors jeu, et le joueur pourrait designer n'importe quoi.

def GetAbilities() -> Sequence['Ability']:

    def mastermind_excello(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        joueur = effect.GetInitiator()
        vues = joueur.LookAtDeck(joueur.player_deck, 2, effect)
        if not vues:
            return

        pour_la_reserve = joueur.AskChooseFace(
            vues,
            effect,
            prompt="Reserve",
            not_move=True,
        )
        if pour_la_reserve is None:
            pour_la_reserve = vues[0]

        MettreEnReserve([pour_la_reserve], joueur, effect)

        # Une seule carte a ete regardee (deck presque vide) : rien a replacer.
        restantes = [face for face in vues if face is not pour_la_reserve]
        if not restantes:
            return

        # Deux options nommees plutot qu'un oui/non : « dessus » et « dessous »
        # sont deux choix egaux, aucun n'est le refus de l'autre.
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place the other card on top of your deck",
                lambda targets: Faces.MoveAllToDeck(
                    restantes, joueur.player_deck, "Top", effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Place the other card on the bottom of your deck",
                lambda targets: Faces.MoveAllToDeck(
                    restantes, joueur.player_deck, "Bottom", effect),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            mastermind_excello,
        ).SetName("Mastermind Excello").LimitOncePerRound(),
    ]
