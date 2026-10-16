from . import *

# Curse of Nine Tales — TRAHISON nemesis, x3 (3/5, 4/5, 5/5 : meme card_id, les
# trois scans ne different que par le numero de collection). SPELL. Boost 1.
# When Revealed: Choose one:
#  - Discard the top 3 cards of your deck and place 1 threat on the main scheme
#    for each different card type discarded this way.
#  - Discard 2 allies you control.
#
# Cartes de reference :
#  - premiere option : `06030` Trickster, mot pour mot :
#    `joueur.DiscardDeckTopCards(3, effect)` +
#    `FacesCounter.GetDifferentTypesCount(faces)` +
#    `this.PlaceThreatOnSchemes("MainScheme", n, effect)` ;
#  - « Choose one » : `joueur.ChooseAbilities(effect, ForChoiceAbility(...), ...)`
#    (`tl013`, `cn006`) ;
#  - deuxieme option : `joueur.AskDiscardFaces(allies, (2, 2), effect)`
#    (`raphael_nemesis/tr016`, `mw020`).
#
# Mots-pieges :
#  - « Choose ONE » : une seule option, au choix du joueur revele ;
#  - « YOUR deck » / « allies YOU CONTROL » : le joueur a qui la carte est
#    revelee (`message.GetToPlayer()`) ;
#  - « FOR EACH DIFFERENT card TYPE » : types distincts parmi les cartes
#    defaussees, pas leur nombre ;
#  - « Discard 2 allies » : exactement DEUX ; avec moins de deux allies
#    l'option n'est pas offerte (ForChoiceAbility avec cibles (2, 2)) ;
#  - la carte ne coute pas de menace si aucune carte n'est defaussee (deck vide).


def GetAbilities() -> Sequence['Ability']:

    def curse_of_nine_tales(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        def defausser_trois_cartes(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            faces = joueur.DiscardDeckTopCards(3, effect)
            valeur = FacesCounter.GetDifferentTypesCount(faces)
            this.PlaceThreatOnSchemes("MainScheme", valeur, effect)

        def defausser_deux_allies(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll([f for f in cibles if f is not None], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard the top 3 cards of your deck and place 1 threat on the main scheme "
                "for each different card type discarded this way",
                defausser_trois_cartes,
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard 2 allies you control",
                defausser_deux_allies,
            ).SetTarget(Ally, from_where=["YouControlCards"], range=(2, 2)),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            curse_of_nine_tales,
        ),
    ]
