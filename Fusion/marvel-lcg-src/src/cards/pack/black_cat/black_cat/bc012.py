from . import *

# Luck's Ran Out — OBLIGATION. 3 icones de boost.
# Give to the Felicia Hardy player.
# Reveal a random card tucked under your identity. If you cannot, this card
#   gains surge. Discard this card.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « BLACK CAT », pas
# « ... NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc
# ICI. Piege bt019 / nt012 / yd013 / dr010 / bk017 / tt020 / br012 / tg011 /
# sn011 — DIXIEME fois, et la sixieme ou il est vu AVANT d'ecrire.
#
# ⚠ « Felicia Hardy » N'A AUCUN HOMONYME AU DEPOT (verifie sur les 5914
# cartes) : contrairement a « Peter Parker », pris quatre fois, le
# `desc.GiveTo` est ici sans ambiguite.
#
# CARTE DE REFERENCE
#  - `sn011` In Walks Trouble (pack spider_man_noir, meme auteur) : la SECONDE
#    branche y est MOT POUR MOT ce texte-ci. La difference imprimee est qu'ici
#    il n'y a AUCUN choix et AUCUNE bascule de forme : l'obligation tombe, on
#    revele, on defausse. Plus courte, plus mordante.
#  - `Rand.RandomChoice` : « a RANDOM card ». ⚠ Deterministe sous
#    `disable_shuffle` — il rend le PREMIER de la liste, ce dont les cas
#    profitent, mais qu'ils ne doivent pas prendre pour du hasard.
#  - `ThisCardGainSurge` (cards/pack/__init__.py:100).
#
# TEXTE CONTRE CODE
#  ⚠ « If you cannot, this card gains SURGE » -> « you cannot » = la pile est
#    VIDE. Mot-piege « if you cannot » (`wd028`) : le cas doit prouver que la
#    branche est ATTEIGNABLE, donc pile vide.
#  ⚠ « REVEAL a random card » et non « discard » : la carte est REVELEE, donc
#    resolue comme une carte de rencontre. Une traitrise glissee fait son
#    « When Revealed », un sbire entre en jeu. C'est la punition d'avoir range
#    n'importe quoi sous son identite.
#  « DISCARD this card » -> la derniere phrase tombe dans les DEUX cas, avec
#    ou sans surge.


def GetAbilities() -> Sequence['Ability']:

    def la_chance_a_tourne(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)

        joueur = message.GetGaveToPlayer() if hasattr(message, "GetGaveToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return

        pile = CartesGlissees(effect, joueur)
        if pile:
            Rand.RandomChoice(pile, effect).Reveal(joueur, effect)
        else:
            # « If you cannot, this card gains surge. »
            ThisCardGainSurge(effect)

        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            la_chance_a_tourne,
        ),
    ]
