from . import *

# Hank's Kimono — soutien signature. ITEM. Cout 1. RES [energy]
# Alter-Ego Action: Exhaust Hank's Kimono -> search your discard pile for a
#   resource card and place it on the top of your deck.
#
# Cartes de reference :
#  - la fouille de la pile de defausse : 04001b * Clint Barton,
#    `Search.PlayerCard(effect, player, include_discard_pile=True, ...)`
#    (recette moteur §2). Comparable parce que la zone fouillee et le filtre
#    par type de carte sont de meme nature ; Clint Barton ajoute a la MAIN la
#    ou le kimono repose sur le DECK.
#  - « Alter-Ego Action » + inclinaison : aa003 * Ebony (pack
#    agatha_harkness), meme couple `AbilityType.AlterEgoAction` +
#    `CostFunc.Exhaust("This")`.
#
# ⚠ « a RESOURCE card » : le TYPE de carte « Resource » (comme bt009 Alien
# Materials), pas « une carte qui porte une icone de ressource » — sinon
# n'importe quelle carte du deck conviendrait et la phrase n'aurait aucun
# sens. D'ou `card_type=Resource`.
#
# ⚠ « on the TOP of your deck », pas dans la main : la carte sera piochee au
# prochain reapprovisionnement. Combinee au passage en forme de heros, c'est
# une pioche differee, pas immediate.
#
# ⚠ Pas de melange : le texte ne dit pas « shuffle », et poser une carte sur
# le dessus n'en demande pas (a la difference de `Search.PlayerCard` sur le
# DECK, ou le « (Shuffle.) » est le comportement par defaut, recette §2).
#
# ⚠ `include_player_deck=False` est OBLIGATOIRE, pas facultatif : le parametre
# n'a AUCUNE valeur par defaut (search.py:133). L'omettre — meme pour dire
# « non » — leve `TypeError: Search.PlayerCard() missing 1 required
# keyword-only argument` a CHAQUE activation de la carte. Trouve par
# l'autoplay le 01/09/2026, dans 4 parties sur 8 ; le cas de test, lui, etait
# passe au VERT (faux vert : le coup d'inclinaison est paye AVANT le plantage,
# et la carte cherchee remontait dans le deck par le remelange de la defausse).

def GetAbilities() -> Sequence['Ability']:

    def hanks_kimono(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            card_type=Resource,
        )
        if face:
            Faces.MoveAllToDeck([face], initiator.player_deck, "Top", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            hanks_kimono
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
