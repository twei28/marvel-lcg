from . import *

# The Demiurge — VERSO de wc019a New Vessel, ENVIRONNEMENT permanent
# Permanent.
# Forced Response: After a player deck runs out of cards, place 1 threat on
#   the main scheme.
#
# Face jamais tiree : on ne l'atteint qu'en accomplissant New Vessel (8
# menaces), qui la retourne (voir wc019a). `desc.Permanent = "1"` est lu
# nativement par le moteur (`HasPermanent`) : aucun code pour le mot-cle
# « Permanent ».
#
# « After a player deck runs out of cards » ->
# `AbilityFactory.AfterDeckRunOut(AbilityType.ForcedResponse, <deck>, ...)`
# (game/ability/factory/deck.py:33). Modele : Soul World (`mts/adam_warlock/
# 21033.py`), la seule autre carte du depot sur ce declencheur.
#
# ECART VOULU avec Soul World : celle-ci passe `lambda effect:
# effect.GetInitiator().player_deck` (le deck de SON joueur). Ici le texte dit
# « A player deck », donc N'IMPORTE quel joueur — et un environnement
# n'appartient a aucun joueur, `effect.GetInitiator()` n'aurait pas de sens.
# Or la fabrique `AfterDeckRunOut` n'accepte qu'un `deck(effect)` compare par
# egalite (deck.py:40-41), sans acces au message : elle ne sait pas exprimer
# « n'importe quel deck de joueur ». On construit donc l'`Ability` a la main,
# comme le font deja une dizaine de cartes du depot (cd008, dt077, lj004,
# mk021, 60007...), avec pour seule condition
# `message.deck.flags.is_player_deck` — le drapeau qu'emploie deja
# `AfterDeckReset` pour cette meme distinction (deck.py:67-71). Il accepte
# tous les joueurs et refuse le deck de rencontre.
#
# « place 1 threat on the main scheme » -> `this.PlaceThreatOnSchemes(
# Worlds.GetMainSchemes(effect), 1, effect)`, la brique standard (modele
# mw018). Valeur NUE (1), sans icone par joueur imprimee.

def GetAbilities() -> Sequence['Ability']:

    def est_un_deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return message.deck.flags.is_player_deck

    def the_demiurge(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)

        principaux = Worlds.GetMainSchemes(effect)
        if principaux:
            this.PlaceThreatOnSchemes(principaux, 1, effect)

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [est_un_deck_de_joueur],
            the_demiurge,
        ),
    ]
