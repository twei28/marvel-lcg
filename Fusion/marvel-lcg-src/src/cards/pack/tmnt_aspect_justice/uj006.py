from . import *

# Dire Straits — EVENEMENT 1* [energy], aspect Justice (TMNT Aspects, Inkwire). FERAL. NYC. THWART.
# [star] Rampage 3. (As an additional cost for this card, take 3 damage and discard 3 cards from the
#   top of your deck.)
# Hero Action (thwart): Remove 3 threat from a scheme. If you control a [[NYC]] support, ready your hero.
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md. Cout additionnel
# `CostFunc.Rampage(3)`. Le « 1* » du cout et le [star] devant Rampage ne sont qu'un RAPPEL (Rules
# Reference v1.8, « Star Icon ») : aucune ligne de code.
#
# CARTES DE REFERENCE
#  - `ua015` Demolish (meme pack d'aspects, meme auteur) : Rampage + « If you control a NYC support »
#    = `joueur.IsControl(CardFinder2("NYC", Support))`, lu a la resolution.
#  - `04049` Clear the Area : evenement de contre `.SetPlay().SetLabel('thwart').SetTarget(Scheme2)` +
#    `RemoveThreatFromSchemes(effect.targets, N, effect)`.
#  - `sk029` Glorious Flight : « ready your hero » = `Faces.ReadyAll([joueur.GetIdentity()], effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « As an additional cost » : un cout impaye (degats empeches, deck ET defausse vides) annule tout.
#  ⚠ « take 3 damage » : l'IDENTITE du joueur ; « YOUR deck » : le deck du joueur.
#  ⚠ « a scheme » : principale OU annexe.
#  ⚠ « If you control a NYC SUPPORT » : un soutien (pas un allie, pas une amelioration) NYC sous TON
#    controle, lu a la resolution, APRES le retrait de menace.
#  ⚠ « ready YOUR hero » : ton identite (la carte est une Hero Action : forme heros).
#  Aucune limite imprimee.


def ControleUnSoutienNYC(effect: 'Effect') -> bool:
    joueur = effect.GetInitiator()
    return joueur is not None and joueur.IsControl(CardFinder2("NYC", Support))


def GetAbilities() -> Sequence['Ability']:

    def dire_straits(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
        if ControleUnSoutienNYC(effect):
            Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dire_straits,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetCostFunc(CostFunc.Rampage(3)),
    ]
