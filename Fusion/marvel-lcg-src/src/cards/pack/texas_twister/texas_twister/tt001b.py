from . import *

# * Drew Daniels (face alter-ego) — CIVILIAN. PV 10, REC 3, main 6.
# Slowdown — Response: After you change to this form, shuffle up to 2
#   [[SUPERPOWER]] cards from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - `01042` Ancestral Knowledge : `SetTarget(range=..., from_where=
#    ["YourDiscardPile"])` puis `Faces.ShuffleAllTo(effect.targets, ...)`.
#  - `bk001b` Clarice Ferguson : meme structure de Reponse au changement de
#    face.
#
# TEXTE CONTRE CODE
#  « UP TO 2 » -> `range=(0, 2)` : zero est un choix legal, le joueur peut
#    renoncer. Ecrire `(1, 2)` forcerait la main quand la defausse ne contient
#    rien d'utile.
#  « [[SUPERPOWER]] cards » -> filtre par TRAIT, pas par type : sept des
#    quinze cartes signature portent SUPERPOWER, evenements comme
#    ameliorations.
#  « INTO YOUR DECK » -> remelange, pas un retour en main : c'est tt005 Pine
#    Ridge Reservation qui rend une carte a la main, et la difference est le
#    tempo de tout le pack.
#  « Response » et non « Forced Response » : le joueur choisit de le faire.


def GetAbilities() -> Sequence['Ability']:

    def ralentissement(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not effect.targets:
            return
        Faces.ShuffleAllTo(list(effect.targets), joueur.player_deck, effect)

    return [
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.Response,
            ralentissement,
        ).SetTarget(
            CardFinder(trait="SUPERPOWER"),
            range=(0, 2),
            from_where=["YourDiscardPile"],
        ).SetName("Slowdown"),
    ]
