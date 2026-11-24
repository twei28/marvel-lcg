from . import *

# Fragment Studies : RESSOURCE ([mental][mental]). Classe Hero.
# Response: After you spend this card, shuffle 1 identity-specific card from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - `mt006` Biopathy / `tm007` : `AfterYouSpendThisCard(AbilityType.Response, op)` (la fabrique filtre « THIS card »).
#  - `27030b` : `card_class="IdentitySpecific"` + `Faces.ShuffleAllTo(.., joueur.player_deck, effect)` (ici le choix se fait dans l'operation, voir la note).
#
# TEXTE CONTRE CODE
#  « After you spend THIS card » : quand elle sert de ressource (pas quand elle est defaussee autrement). « 1 identity-specific card » : classe propre a l'identite (les cartes du deck de heros de Destiny), une seule,
#    prise dans SA defausse. « shuffle into your deck » : le deck est melange.
#  Chiffres : 2 ressources [mental] imprimees, 1 carte.


def GetAbilities() -> Sequence['Ability']:

    def fragment_studies(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        joueur = effect.GetInitiator()
        # Les candidates sont cherchees ICI et non par `SetTarget(card_class=..)` : une cible a classe sur une Reponse de ressource rendait la carte
        # impayable pour le moteur quand aucune cible n'existait encore au moment du paiement (cas dy012, la carte n'etait jamais depensee).
        candidates = [f for f in joueur.discard_pile.Get() if ClassCard.IsType(f) and f.IsClass("IdentitySpecific")]
        choisie = joueur.AskChooseFace(candidates, effect, prompt="Fragment Studies : shuffle 1 identity-specific card into your deck", not_move=True) if candidates else None
        if choisie is not None:
            Faces.ShuffleAllTo([choisie], joueur.player_deck, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            fragment_studies,
        ),
    ]
