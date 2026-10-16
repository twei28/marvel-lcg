from . import *

# Feral Cunning — EVENEMENT 2* [mental], aspect Justice (TMNT Aspects, Inkwire). ATTACK. FERAL.
# [star] Rampage 2. (As an additional cost for this card, take 2 damage and discard 2 cards from the
#   top of your deck.)
# Hero Action (attack): Deal 1 damage to an enemy and confuse it.
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md. Cout additionnel
# `CostFunc.Rampage(2)`. Le « 2* » du cout et le [star] devant Rampage ne sont qu'un RAPPEL.
#
# CARTES DE REFERENCE
#  - `ua015` Demolish : Rampage sur une Hero Action d'attaque
#    (`.SetPlay().SetLabel('attack').SetTarget(Enemy).SetCostFunc(CostFunc.Rampage(X))`).
#  - `58016` Battlefield Benevolence : « confuse that enemy » = `Faces.GiveStatus(cibles, "Confused", effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « Deal 1 damage to an enemy AND confuse IT » : la MEME cible (vilain ou sbire) recoit les deux ;
#    la desorientation ne depend pas des degats (un Tenace qui absorbe le degat n'empeche pas le statut).
#  ⚠ Rampage : cout impaye -> ni degat ni statut.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def feral_cunning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 1, effect)
        cibles = [cible for cible in effect.targets if cible.IsInPlay()]
        Faces.GiveStatus(cibles, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            feral_cunning,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetCostFunc(CostFunc.Rampage(2)),
    ]
