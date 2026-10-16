from . import *

# Prepare to Rally — TRAHISON nemesis (5/5). Boost : [star].
# When Revealed: Discard 1 card from your hand.
# [star] Boost: Discard 1 card from your hand.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# MOT-CLE : BOOST — fiche `docs/reference/mots-cles/boost.md` (`desc.Boost =
# "0"` + `WhenCardBecomeBoost`).
#
# CARTES DE REFERENCE
#  - `57062` Superspeed (synthezoid) : « [star] Boost: Discard 1 card from your
#    hand » — `ChooseAbilities(effect, ForChoiceAbility('Discard 1 card from
#    your hand', ...).SetTarget(main, range=(1, 1), not_move=True))`.
#  - `mw020` : `AbilityFactory.WhenThisRevealed(None, op)` + `message.GetToPlayer()`
#    pour une traitrise de rencontre.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard 1 card from your hand » SANS « at random » : le JOUEUR choisit
#    (contrairement a `57062` Superspeed, `rg017`, `07058`, ou la defausse est
#    au hasard a la revelation). Lecture litterale.
#  ⚠ Main vide : rien a defausser, aucun repli imprime (pas de surge).
#  ⚠ Les deux effets (revelation et boost) sont IDENTIQUES : meme helper, mais
#    deux capacites distinctes (`WhenThisRevealed` vs `WhenCardBecomeBoost`).
#  Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def se_preparer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is not None:
            DefausserUneCarteDeLaMain(joueur, effect)

    def se_preparer_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is not None:
            DefausserUneCarteDeLaMain(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            se_preparer,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            se_preparer_boost,
        ),
    ]
