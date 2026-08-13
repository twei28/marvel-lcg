from . import *

# Overstay Your Welcome

def GetAbilities() -> Sequence['Ability']:

    def overstay_your_welcome(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 5 threat from a scheme",
                lambda targets:
                    this.RemoveThreatFromSchemes(targets, 5, effect)
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from each scheme in play",
                lambda targets:
                    this.RemoveThreatFromSchemes("EachScheme", 2, effect)
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            overstay_your_welcome
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
