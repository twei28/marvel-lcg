from . import *

# Civil Genius : EVENEMENT (THWART), cout 2, [mental]. x2.
# Hero Action (thwart): Remove 3 threat from a scheme. You may exhaust Beast's Lab and discard a card tucked under it to change to alter-ego form.
#
# CARTES DE REFERENCE
#  - `mf009` : `this.RemoveThreatFromSchemes(effect.targets, n, effect)` + `.SetPlay().SetLabel('thwart')` + `.SetTarget(Scheme2)`.
#  - `YouMayFlipToYourAlterEgoForm` (cards/pack/__init__.py) : `player.GetIdentity().ChangeToForm(AlterEgo, effect)` ; `bs010` : `MayChooseOneAbility` + cout d'inclinaison du Lab.
#
# TEXTE CONTRE CODE
#  « Remove 3 threat from A scheme » : une manigance, 3 menaces. « YOU MAY exhaust Beast's Lab AND discard a card tucked under it TO change to alter-ego form » : option refusable a deux couts, APRES le retrait ;
#    elle n'est offerte qu'en forme heros (sinon il n'y a rien a changer), avec le Lab pret et une carte glissee.
#  Chiffres : cout 2, 3 menaces.


def GetAbilities() -> Sequence['Ability']:

    def genie_civil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
        glissees = GlisseesSousLab(joueur)
        if not (joueur.IsHero() and glissees and LabPret(joueur)):
            return

        def defausser_et_changer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            carte = joueur.AskChooseFace(glissees, effect, prompt="Discard a card tucked under Beast's Lab", peek=True, not_move=True)
            if carte is not None:
                Faces.DiscardAll([carte], effect)
            joueur.GetIdentity().ChangeToForm(AlterEgo, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Beast's Lab and discard a card tucked under it: change to alter-ego form",
                defausser_et_changer,
            ).SetHasNoTargetEffect()
            .SetCostFunc(CostFunc.Exhaust("YouControlCards", name=NOM_LAB)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            genie_civil,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
