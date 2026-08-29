from . import *

# Caged Bird — obligation d'Alexei Shostakov
# Give to the Alexei Shostakov player.
# When Revealed: Find Red Guardian's Shield and tuck it under here.
# Alter-Ego Action: Exhaust Alexei Shostakov -> remove this card from the game.
#
# L'obligation prend le bouclier en otage : tant qu'elle est en jeu, tout le
# pack est mort (rg004, rg005, rg006, rg007, rg009 dependent du bouclier).
#
# Gabarit : Lost Visor (cyclops/cyclops/33027), la seule obligation officielle
# qui fait exactement cela — retrouver une carte nommee OU QU'ELLE SOIT et la
# glisser sous elle. Meme structure, meme couple de capacites.
#
# « Find » sans zone precisee : `Search.SearchForCard` couvre les quatre zones
# ou le bouclier peut se trouver. Lost Visor n'en ouvre que trois (main, deck,
# defausse, zone du joueur) parce que le viseur de Cyclope est toujours
# attache a l'identite ; le bouclier de Red Guardian, lui, s'attache a un
# ENNEMI ou a une MANIGANCE (rg001a), qui ne sont pas dans la zone du joueur.
# D'ou `include_in_play=True` en plus : `Worlds.GetOnFieldCards` descend
# recursivement dans les `GetInventoryDeck()` des cartes en jeu, donc y compris
# une amelioration attachee a un ennemi. Les zones se recoupent, mais
# `SearchForCardsInternal` regroupe par (nom, zone) : le bouclier n'etant qu'a
# un seul endroit a la fois, aucune double proposition n'est possible.
#
# Face cachee (`False`) comme Lost Visor : « tuck » = glisser dessous, la carte
# n'est plus consultable ni jouable.


def GetAbilities() -> Sequence['Ability']:

    def caged_bird(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetToPlayer()

        bouclier = Search.SearchForCard(
            effect,
            joueur,
            include_player_hand_cards=True,
            include_player_deck=True,
            include_player_discard_pile=True,
            include_player_area=True,
            include_in_play=True,
            name=NOM_BOUCLIER,
        )
        if bouclier:
            this.PlaceCardHere(bouclier, False, effect)

    def caged_bird_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)

        # Le texte ne dit rien du bouclier glisse dessous : il ne dit que
        # « remove this card from the game ». Le laisser tel quel le suivrait
        # dans la zone retiree du jeu — `Faces.MoveAllTo` ne vide pas le
        # `GetPlacedCardArea()` de la carte deplacee, et `GameArea.AddCard`
        # entraine les cartes placees avec leur hote. Red Guardian perdrait son
        # bouclier definitivement, donc tout son deck.
        # On applique la regle generale des cartes placees sous une carte qui
        # quitte le jeu : elles vont a la defausse de leur proprietaire. C'est
        # deja ce que fait le moteur lui-meme dans le meme cas
        # (`player_action.py:525`, `GainCard` vide `GetPlacedCardArea()` a la
        # defausse quand son hote quitte le jeu).
        # Le bouclier est alors recuperable par « Rescue the Shield » (rg001b)
        # ou par Shield Harness (rg010) : c'est manifestement l'intention.
        Faces.DiscardAll(this.GetPlacedCardArea().Get(), effect)

        Faces.RemoveAllFromGame([this], effect)

    return [
        # CORRECTIF (29/08/2026, trouve par `tools/audit_cartes.py`) :
        # la carte IMPRIME « When Revealed », mais le module utilisait
        # `WhenThisObligationGiveToYou`, qui ne produit AUCUNE capacite de type
        # `AbilityType.WhenRevealed`. L'effet partait bien — l'audit du pack
        # l'avait prouve — mais le marqueur imprime n'avait pas sa contrepartie
        # dans le moteur, et rien de ce qui cible une capacite « When Revealed »
        # ne voyait celle-ci.
        # Convention officielle verifiee : sur les 13 obligations du jeu qui
        # impriment ce marqueur, 11 passent par `WhenThisObligationRevealed` ou
        # `WhenThisRevealed` (40031, 40160, 40161, 41025, 42024, 50059...).
        # Seule `ab011`, d'un pack custom, faisait comme nous.
        AbilityFactory.WhenThisObligationRevealed(
            caged_bird
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            caged_bird_action,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
