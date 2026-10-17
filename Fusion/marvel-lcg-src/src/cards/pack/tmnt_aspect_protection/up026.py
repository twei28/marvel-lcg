from . import *

# Primal Provisions — EVENEMENT 0* [energy], aspect Protection (TMNT Aspects, Inkwire). FERAL.
# Max 1 per phase.
# [star] Rampage 2. (As an additional cost for this card, take 2 damage and discard 2 cards from the top
#   of your deck.)
# Hero Action: Draw 2 cards.
#
# NOUVELLE. MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md.
#
# CARTES DE REFERENCE
#  - `ua015` Demolish : `.SetCostFunc(CostFunc.Rampage(X))` sur la capacite `WhenInYourPlayTurn(...).SetPlay()`.
#  - `tr006` Unbridled Fury / `19030` Bring It! : « Max 1 per phase » = `.MaxOnePerPhase()`.
#  - `27016`/`56048` : `initiator.DrawUp(N, effect)` pour « Draw N cards ».
#
# TEXTE CONTRE CODE
#  ⚠ « Max 1 per PHASE » (pas per round) : `MaxOnePerPhase`.
#  ⚠ Rampage 2 : 2 degats a l'identite + 2 cartes du dessus de VOTRE deck, payes avant l'effet ; le deck
#    paye (2 cartes en moins) PUIS la pioche de 2.
#  ⚠ « Hero Action » : forme heros.


def GetAbilities() -> Sequence['Ability']:

    def primal_provisions(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            primal_provisions,
        ).SetPlay().SetLabel()
        .MaxOnePerPhase()
        .SetCostFunc(CostFunc.Rampage(2)),
    ]
