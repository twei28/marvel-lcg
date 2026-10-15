from . import *

# * Laura Green (face ALTER EGO) — SKRULL. SPY. REC 3, main 6, 10 PV.
# Playing Along — Action: Search your deck for a TREACHERY card, shuffle your deck
#   and place that card on the top of your deck. (Limit once per round.)
#
# Cartes de reference :
#  - **`an001b`** / **`ok001b`** : `Search.PlayerCard(include_player_deck=True,
#    ...)` (le melange est le comportement par defaut de la recherche).
#  - **`Faces.MoveAllToDeck([face], deck, "Top", effect)`** (modele ag001b, bt011) :
#    la carte trouvee sort du deck pour la zone de traitement, c'est a l'appelant
#    de la consommer.
#  - **`hd001b`** : `LimitOncePerRound()` sur une Action d'alter ego.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « your deck » : le deck du JOUEUR (pas le deck rencontre).
#  - « TREACHERY card » : type Treachery OU trait TREACHERY ; dans un deck joueur
#    ce sont les evenements de Lyja.
#  - Rien a trouver : le deck est melange quand meme (il a ete fouille).
#  - « Limit once per round » : temoin d'epuisement dans les cas.


def GetAbilities() -> Sequence['Ability']:

    def jouer_le_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        trouvee = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            finder=FinderTraitrise(),
        )
        if trouvee is None:
            joueur.player_deck.Shuffle(effect)
            return
        Faces.MoveAllToDeck([trouvee], joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            jouer_le_jeu,
        ).SetName("Playing Along")
        .LimitOncePerRound(),
    ]
