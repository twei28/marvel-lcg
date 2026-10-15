from . import *

# * Searching for Powers — COMPLOT ANNEXE DE JOUEUR (Basic / Campaign, n° 274). Cout 0, menace de depart 3.
# Victory 0.
# When Defeated: The player who defeated this scheme may search their deck and discard pile for a card with
#   the SUPERPOWER trait and play it, ignoring its resource cost. (Shuffle.)
#
# Cartes de reference :
#  - **`hd010`** Trapped : « may search their deck and discard pile for X » = `Search.PlayerCard(effect, joueur,
#    include_player_deck=True, include_discard_pile=True, may=True, ...)` ; « the player who defeated » =
#    `message.GetDefeatingPlayer()`. Le (Shuffle.) est le comportement par defaut de la recherche.
#  - **`bc004`** Big Heist / **`dz031`** : « play it, ignoring its resource cost » = la carte passe par la MAIN
#    (`Faces.AddToHand`) puis `joueur.PlayCardsLikeInTurn([face], effect, ignore_resources_cost=True)` (une
#    carte de la defausse ou du deck n'est pas « jouable » directement : ability.py:235).
#
# ⚠ Mots-pieges :
#  - « SUPERPOWER trait » : le TRAIT, quel que soit le type de carte (amelioration de Lyja, evenement, ...) ;
#  - « ignoring its resource cost » : le cout de ressources n'est pas paye ; les AUTRES conditions de jeu
#    (cible d'une amelioration, Max par joueur) restent ;
#  - « deck AND discard pile » : les deux zones du JOUEUR qui a vaincu le complot ; « may » : facultatif ;
#  - une carte trouvee mais injouable reste en main (la recherche l'a deja sortie du deck).


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return
        face = Search.PlayerCard(
            effect,
            vainqueur,
            include_player_deck=True,
            include_discard_pile=True,
            trait="SUPERPOWER",
            may=True,
        )
        if face is None:
            return
        Faces.AddToHand([face], vainqueur, effect)
        vainqueur.PlayCardsLikeInTurn([face], effect, ignore_resources_cost=True)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
