from . import *

# Truth Revealed — TRAITRISE NEMESIS de Lyja (n° 69, 5/5). 2 icones boost.
# When Revealed: Search your deck for all identity-specific cards, shuffle your deck and place
#   those cards on the bottom of your deck in any order.
#
# Cartes de reference :
#  - **`Search.SearchForCards(..., range="All")`** (search.py:259) : « all cards » ; **`an001b`**
#    pour la recherche dans le deck du joueur ; **`Faces.MoveAllToDeck(faces, deck, "Bottom",
#    effect)`** (modele **`hd001b`**, `05006`) et **`player.PlaceOnBottomInAnyOrder`**
#    (player_cards.py:28) pour « in any order ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOUR deck » : le deck du joueur a qui la carte est revelee.
#  - « IDENTITY-SPECIFIC cards » : les cartes SIGNATURE de l'identite, `desc.Class == "Hero"`
#    (decision de l'auteur : un deck ne contient que les siennes, voir PROCESSUS-HEROS
#    etape 10) ; PAS les cartes d'aspect, ni les basiques, ni l'obligation/nemesis (hors deck).
#  - « ALL » : toutes, pas une seule ; « shuffle your deck » : le deck est melange, PUIS les
#    cartes vont dessous ; « bottom » : sous le deck (donc tirees en dernier).
#  - Aucune carte specifique : le deck est melange quand meme.


def GetAbilities() -> Sequence['Ability']:

    def est_specifique_a_l_identite(face: 'CardFace') -> bool:
        return (getattr(face.paper, "desc", None) or {}).get("Class") == "Hero"

    def verite(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        trouvees = Search.SearchForCards(
            effect, joueur,
            include_player_deck=True,
            finder=CardFinder(check_face_fn=est_specifique_a_l_identite),
            range="All",
        )
        if not trouvees:
            joueur.player_deck.Shuffle(effect)
            return
        trouvees = list(trouvees)
        Faces.MoveAllToDeck(trouvees, joueur.player_deck, "Bottom", effect)
        joueur.PlaceOnBottomInAnyOrder(trouvees, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, verite),
    ]
