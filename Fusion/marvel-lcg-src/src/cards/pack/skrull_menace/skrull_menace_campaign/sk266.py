from . import *

# * Skymax — ALLIE de campagne (Leadership / Campaign, n° 266). Cout 3. THW 2** / ATK 3**, 5 PV.
# SKRULL. SQUADRON SUPREME.
# Response: When Skymax enters play, shuffle all allies from your discard pile into your deck.
#
# Cartes de reference :
#  - **`01083`** Mockingbird : `AfterCardEnterPlay(Response, "This", ...)` (le texte dit « When » mais la
#    capacite est une REPONSE : elle part apres l'entree en jeu).
#  - **`hd012`** He Never Made / **`ok001b`** : « shuffle cards from your discard pile into your deck » =
#    `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)`.
#
# ⚠ Mots-pieges : « ALL allies » (aucune limite, aucun choix) ; « YOUR discard pile » (celle du
# controleur de Skymax, pas celle d'un autre joueur) ; « from your discard pile » : seuls les allies de la
# DEFAUSSE sont touches, jamais ceux en jeu.


def GetAbilities() -> Sequence['Ability']:

    def skymax(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        allies = [f for f in joueur.discard_pile.GetAll() if Ally.IsType(f)]
        if allies:
            Faces.ShuffleAllTo(allies, joueur.player_deck, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            skymax,
        ),
    ]
