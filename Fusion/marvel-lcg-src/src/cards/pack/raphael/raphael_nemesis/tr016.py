from . import *

# Insurrection — TRAHISON nemesis (x2 dans le set, 3/5 et 4/5). Boost : [star].
# When Revealed: Discard 1 ally you control. If you cannot, discard 1 card from
#   your hand.
# [star] Boost: Discard 1 ready ally you control.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# MOT-CLE : BOOST — fiche `docs/reference/mots-cles/boost.md`. `desc.Boost = "0"`
# (aucune icone chiffree, une etoile) + `WhenCardBecomeBoost("This", op)`.
#
# CARTES DE REFERENCE
#  - `mw020` One Spyder Down : « Discard an ally you control. If you cannot ... »
#    = `player.AskDiscardFaces(player.GetControlAllies(), (1, 1), effect)`, dont
#    le RETOUR vide signifie « you cannot ». Les deux cartes ont la meme forme,
#    seule la branche de repli change (surge la-bas, defausse de main ici).
#  - `57062` Superspeed : « Discard 1 card from your hand » en boost, le joueur
#    choisit (`ForChoiceAbility(...).SetTarget(main, range=(1, 1))`) —
#    `DefausserUneCarteDeLaMain` du __init__.
#  - `mw015` Power Absorption : meme montage pour « Discard an ally you control ».
#
# TEXTE CONTRE CODE
#  ⚠ « Discard 1 ally YOU CONTROL » : parmi les allies du joueur revele
#    (`message.GetToPlayer()`), pas ceux d'un autre joueur ; le joueur CHOISIT.
#  ⚠ « If you CANNOT, discard 1 card FROM YOUR HAND » : le repli ne part que
#    s'il n'y avait AUCUN allie a defausser, jamais en plus. Un joueur sans
#    allie ET sans main ne defausse rien (aucun surge imprime).
#  ⚠ Boost : « 1 READY ally you control » : seulement les allies REDRESSES
#    (`IsReady()`), pas les epuises ; aucun repli imprime, donc rien si aucun
#    allie redresse.
#  ⚠ Le joueur du boost est `message.GetToPlayer()` (celui qui subit
#    l'activation).
#  Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def insurrection(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        # « Discard 1 ally you control. » Un retour vide = « you cannot ».
        if joueur.AskDiscardFaces(joueur.GetControlAllies(), (1, 1), effect):
            return
        # « If you cannot, discard 1 card from your hand. »
        DefausserUneCarteDeLaMain(joueur, effect)

    def insurrection_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        pretes = [a for a in joueur.GetControlAllies() if a.IsReady()]
        if pretes:
            joueur.AskDiscardFaces(pretes, (1, 1), effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            insurrection,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            insurrection_boost,
        ),
    ]
