from . import *

# Legal Practice (variante Why Not) : 2 menaces par carte defaussee au lieu
# de 1 ; l'auteur a BARRE « Thwart » et « (thwart) » : plus de trait THWART,
# plus de libelle thwart. Modele 01023.


def GetAbilities() -> Sequence['Ability']:

    def legal_practice(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        defaussees = len(effect.cost_func.Get(CostFunc.Discard).return_discarded_cards)
        this.RemoveThreatFromSchemes(effect.targets, 2 * defaussees, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            legal_practice
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 5)))
        .SetTarget(Scheme2),
    ]
