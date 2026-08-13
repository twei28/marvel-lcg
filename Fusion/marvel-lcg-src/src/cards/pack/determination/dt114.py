from . import *

# * Blink

def GetAbilities() -> Sequence['Ability']:

    def blink(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready a LOCATION card",
                lambda targets: Faces.ReadyAll(targets, effect)
            ).SetTarget(CardFinder(trait="LOCATION"), canbe_ready=True),
            AbilityFactory.ForChoiceAbility(
                "Change your form",
                lambda targets: initiator.GetIdentity().ChangeToOtherForm(effect)
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            blink
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This"))
        .SetCostFunc(CostFunc.DealDamage(1, "YourIdentity")),
    ]
