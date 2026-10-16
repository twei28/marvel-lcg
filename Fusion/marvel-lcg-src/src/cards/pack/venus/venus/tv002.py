from . import *

# * Bludgeon — ALLIE, cout 3, [wild]. NINJA. SHARK. TEMPORAL. PV 3, ATQ 2*, CTR 2*. x1.
# Response: After Bludgeon enters play, put 1 card from your discard pile on top of
#   your deck.
#
# CARTES DE REFERENCE
#  - `tl002` Splinter (pack leonardo) : `AfterCardEnterPlay(Response, "This", op)` +
#    `SetTarget(..., from_where=["YourDiscardPile"])` + `Faces.MoveAllToDeck([...],
#    player_deck, "Top", effect)` ; ici la carte est LIBRE (toute carte de la defausse).
#
# TEXTE CONTRE CODE
#  ⚠ « put 1 card from YOUR discard pile » -> la defausse du joueur, jamais celle des autres.
#  ⚠ « on TOP of your deck » -> argument positionnel "Top".
#  ⚠ Reponse (pas « Hero Response ») : jouable aussi en alter-ego, sans condition de forme.
#  ATQ/CTR « 2* » = 1 degat consecutif chacun, lu dans `desc` par le moteur.


def GetAbilities() -> Sequence['Ability']:

    def remonter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        cibles = [t for t in effect.targets if t is not None]
        if joueur is None or not cibles:
            return
        Faces.MoveAllToDeck(cibles, joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            remonter,
        ).SetTarget(card_type=CardFace, from_where=["YourDiscardPile"]),
    ]
