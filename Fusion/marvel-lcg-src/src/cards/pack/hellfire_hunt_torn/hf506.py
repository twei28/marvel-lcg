from . import *

# Uncover The Truth (obligation, Boost 2, icone Hazard). « Alter-Ego Action : Exhaust your identity -> heal 5 damage from the villain and remove 5 threat from a
# side scheme. Discard this obligation. »
# Cartes de reference : 27131 / 04045 (`WhenInYourPlayTurn(...).SetTarget(SchemeSide2)`, cible = « a side scheme »), 04166 (action d'alter ego d'obligation),
# 40160 (`CostFunc.Exhaust("YourIdentity")`). Hazard : natif (`desc.Hazard`, fiche mots-cles/hazard.md ; l'icone « carte penchee + croix » = Hazard, comparee a 01180).
# ⚠ Le texte SOIGNE le vilain (5 degats) ET retire 5 menaces d'une manigance annexe : les deux parties sont jouees, puis l'obligation est defaussee.


def GetAbilities() -> Sequence['Ability']:
    def agir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            this.HealthUnits([vilain], 5, effect)
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, agir)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetTarget(SchemeSide2),
    ]
