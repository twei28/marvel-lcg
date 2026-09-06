from . import *

# In Walks Trouble — OBLIGATION. 2 icones de boost.
# Give to the Peter Parker player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Peter Parker -> remove In Walks Trouble from the game.
#  • Reveal a random card tucked under your identity. If you cannot, this card
#    gains surge. Discard this obligation.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « SPIDER-MAN NOIR », pas
# « ... NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc
# ICI et pas dans `spider_man_noir_nemesis/`. Piege bt019 / nt012 / yd013 /
# dr010 / bk017 / tt020 / br012 / tg011 — NEUVIEME fois, et la cinquieme ou il
# est vu AVANT d'ecrire.
#
# ⚠ « Give to the PETER PARKER player » : QUATRIEME obligation du depot a viser
# ce nom, apres `01165` (Spider-Man officiel), `sr013` (spider_man_rainy) et
# `as014` (armored_spidey). `Worlds.FindPlayerByName` rend le PREMIER joueur
# qui repond au nom : en solo c'est toujours le bon, a plusieurs avec deux
# Peter Parker a la table l'ambiguite existe. Elle est ANTERIEURE et partagee
# par les quatre cartes — on ecrit ce qui est imprime, comme les trois autres.
#
# CARTES DE REFERENCE
#  - `ho013` : le squelette d'une obligation a remise
#    (`WhenThisObligationGiveToYou`).
#  - `YouMayFlipToYourAlterEgoForm` (cards/pack/__init__.py:132) : le helper
#    « may flip », a ne pas confondre avec la bascule forcee.
#  - `ThisCardGainSurge` (cards/pack/__init__.py:100) et `RemoveThisFromGame`
#    (ligne 108) : les deux sorties de la carte.
#  - `Rand.RandomChoice` : « a RANDOM card ». ⚠ Deterministe sous
#    `disable_shuffle` — il rend le PREMIER de la liste, ce dont les cas
#    profitent, mais qu'ils ne doivent pas prendre pour du hasard.
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY flip to alter-ego form » -> facultatif, et AVANT le choix. Le
#    joueur qui refuse reste en heros et doit quand meme choisir une branche —
#    or la premiere exige d'incliner Peter Parker, qui n'est pas en jeu. En
#    forme heros, seule la seconde branche est donc jouable. C'est ce que dit
#    la carte, et c'est ce qui la rend mordante.
#  « Exhaust PETER PARKER » -> la face ALTER-EGO nommement. On passe par
#    l'identite du joueur, qui est cette face-la des lors qu'on a bascule.
#  « Reveal a RANDOM card tucked under your identity » -> au hasard, pas au
#    choix : c'est la punition, le joueur ne trie pas sa pile.
#  ⚠ « If you cannot, this card gains SURGE » -> « you cannot » = la pile est
#    VIDE. Le surge s'ajoute alors a CETTE carte, et une carte de rencontre
#    supplementaire est revelee. Mot-piege « if you cannot » (`wd028`) : le
#    cas doit prouver que la branche est atteignable, donc pile vide.
#  « DISCARD this obligation » -> la seconde branche defausse, la premiere
#    RETIRE DU JEU. Deux sorties differentes, et c'est tout l'arbitrage offert
#    au joueur : payer une inclinaison pour s'en debarrasser definitivement,
#    ou encaisser et la revoir plus tard.


def GetAbilities() -> Sequence['Ability']:

    def des_ennuis_a_la_porte(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)

        joueur = message.GetGaveToPlayer() if hasattr(message, "GetGaveToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return

        # « You may flip to alter-ego form. »
        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def retirer_du_jeu(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def reveler_au_hasard(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            pile = CartesGlissees(effect, joueur)
            if pile:
                Rand.RandomChoice(pile, effect).Reveal(joueur, effect)
            else:
                # « If you cannot, this card gains surge. »
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        # ⚠ La premiere branche exige d'incliner Peter Parker : elle n'est
        # offerte que si l'identite en jeu est bien la face ALTER-EGO et
        # qu'elle est PRETE. En forme heros, le joueur n'a que la seconde.
        identite = joueur.GetIdentity()
        branches = []
        if identite is not None and AlterEgo.IsType(identite) and not identite.IsExhaust():
            branches.append(AbilityFactory.ForChoiceAbility(
                "Exhaust Peter Parker and remove In Walks Trouble from the game",
                retirer_du_jeu))
        branches.append(AbilityFactory.ForChoiceAbility(
            "Reveal a random card tucked under your identity",
            reveler_au_hasard))
        joueur.ChooseAbilities(effect, *branches)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            des_ennuis_a_la_porte,
        ),
    ]
