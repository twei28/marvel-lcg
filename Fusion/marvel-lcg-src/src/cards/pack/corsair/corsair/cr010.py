from . import *
# Trick up my Sleeve. Evenement TACTIC THWART, cout 2, x3.
#
# Hero Action (thwart): Remove 4 threat from a scheme. You may discard a card tucked under Corsair to confuse an enemy.
#
# Cartes de reference : 01023 Legal Practice (`SetLabel('thwart')` + `SetTarget(Scheme2)` + `RemoveThreatFromSchemes`),
# 08013 / 16155 (choix secondaire facultatif), 05015 Tackle (`Faces.GiveStatus(..., "Confused")`).
# ⚠ « You MAY discard... to confuse » : facultatif ; la defausse est le cout du statut (pas de defausse sans cible).
def GetAbilities() -> Sequence['Ability']:
    def trick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
        glissees = Glissees(IdentiteDe(effect))
        ennemis = Ennemis(effect)
        if joueur is None or not glissees or not ennemis:
            return
        def action(chosen: Sequence['CardFace']):
            if not chosen:
                return
            Faces.DiscardAll(list(chosen), effect)
            cible = ennemis[0] if len(ennemis) == 1 else joueur.AskChooseFace(
                ennemis, effect, prompt="Confuse an enemy", forced=True)
            if cible is not None:
                Faces.GiveStatus([cible], "Confused", effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a card tucked under Corsair to confuse an enemy",
                action,
            ).SetTarget(glissees, range=(0, 1), not_move=True),
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            trick,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
