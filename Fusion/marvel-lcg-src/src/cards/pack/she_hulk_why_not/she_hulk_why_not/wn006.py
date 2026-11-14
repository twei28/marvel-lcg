from . import *

# Superhuman Law Division (variante Why Not) : 3 menaces au lieu de 2, et
# « (thwart) » barre par l'auteur (le modele 01026 n'avait deja aucun libelle).


def GetAbilities() -> Sequence['Ability']:

    def superhuman_law_division(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            superhuman_law_division
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("B"))
        .SetTarget(Scheme2),
    ]
