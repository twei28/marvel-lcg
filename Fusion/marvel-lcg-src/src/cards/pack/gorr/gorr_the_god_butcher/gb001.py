from . import *

# * Gorr the God Butcher (I) — VILAIN, stade I. NECROVERSE.
# SCH 1 / ATQ 2 — 13 PV par joueur.
#
# Forced Response: After a player's deck runs out of cards, Gorr the God
#   Butcher activates against them.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After a player deck runs out of cards » : wc019b (The Demiurge, pack
#   wiccan) et 21033 (Soul World). La fabrique `AfterDeckRunOut`
#   (ability/factory/deck.py) n'accepte qu'un deck compare par EGALITE, sans
#   acces au message : elle ne sait pas dire « n'importe quel joueur ».
#   wc019b construit donc l'`Ability` a la main avec pour condition
#   `message.deck.flags.is_player_deck` ; on copie ce montage.
# - « X activates against them » : `Enemy.DoActivate(player, effect)`
#   (card/face/base/enemy.py:203), qui choisit lui-meme attaque ou manigance
#   selon la forme du joueur vise et distribue les cartes de boost.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « A PLAYER's deck » -> n'importe quel joueur, pas seulement le premier :
#   condition sur le drapeau du deck, jamais sur l'initiateur.
# « activates AGAINST THEM » -> la cible est le proprietaire du deck epuise
#   (`message.deck.GetOwner()`), pas le joueur actif.
# « Forced Response » -> apres l'evenement, sans fenetre de choix.


def GetAbilities() -> Sequence['Ability']:

    def est_un_deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return message.deck.flags.is_player_deck

    def gorr_active_contre_lui(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Villain)

        joueur = message.deck.GetOwner()
        if isinstance(joueur, Player):
            this.DoActivate(joueur, effect)

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [est_un_deck_de_joueur],
            gorr_active_contre_lui,
        ).SetName("Deicide"),
    ]
