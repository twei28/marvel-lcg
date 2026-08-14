from . import *

# * Madame Web

def GetAbilities() -> Sequence['Ability']:

    def toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Alter-Ego Action (thwart): Exhaust Madame Web → for each WEB-WARRIOR
        # card you control, choose a scheme and remove 1 threat from it. »
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        combien = len(joueur.GetControlCards(CardFinder(trait="WEB-WARRIOR")))
        for _ in range(combien):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 threat from a scheme",
                    lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect)
                ).SetTarget(Scheme2),
            )

    return [
        # « Each PSIONIC character you control gains the WEB-WARRIOR trait. »
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="PSIONIC", card_type=Friend),
            control_by="You",
            trait=["WEB-WARRIOR"],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            toile
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetLabel('thwart'),
    ]
