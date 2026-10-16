from . import *

# Unbridled Fury — EVENEMENT, cout 1, [physical]. x2.
# Max 1 per phase.
# Hero Action: Raphael gets +2 ATK until the end of the round. If you paid for
#   this card using a [physical] resource, draw 1 card.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `bk014` (pack blink) / `14005` : « Max 1 per phase » -> `.MaxOnePerPhase()`
#    (ability.py:1028), modele officiel `19030` Bring It!.
#  - `bw008` Heavy Lifting : `hero.GainUntilRoundEnd(effect, attack=N)` pour
#    « gets +N ATK until the end of the round », et
#    `effect.GetPaidResources().GetColor("R")` pour lire la couleur payee.
#  - `10006` Unstoppable Force / `01053` : « If you paid for this card using a
#    [physical] resource » -> `effect.GetPaidResources().HasColor("R")`.
#
# TEXTE CONTRE CODE
#  ⚠ « Max 1 per PHASE » et non « per round » : `MaxOnePerPhase` (Double Life
#    27032 est la version « per round »).
#  ⚠ « using A [physical] resource » (UN suffit : `HasColor`) et non « ONLY
#    [physical] » (`OnlyHasColor`, famille Hulk). Les compteurs de rage
#    depenses comme ressource [physical] (`tr001a`) COMPTENT : c'est le sens de
#    « as if it were a [physical] resource ». A VERIFIER en phase C que
#    `GetPaidResources` voit bien une ressource generee par un compteur.
#  ⚠ « RAPHAEL gets +2 ATK » : le HEROS (face heros), jamais l'identite civile.
#    `Hero Action` impose de toute facon la forme heros.
#  ⚠ Le +2 ATK est pose AVANT/independamment de la pioche : les deux
#    consequences sont separees par un point, sans fleche.


def GetAbilities() -> Sequence['Ability']:

    def fureur(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is not None:
            heros.GainUntilRoundEnd(effect, attack=2)

        if effect.GetPaidResources().HasColor("R"):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fureur,
        ).SetPlay().SetLabel()
        .MaxOnePerPhase(),
    ]
