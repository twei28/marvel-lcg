from . import *

# Unyielding — custom "Rainy"
# Hero Response (thwart): After you are attacked and take no damage, exhaust
# Unyielding -> remove 2 threat from a scheme. You may spend 1 resource of
# any type to ready your hero.

def GetAbilities() -> Sequence['Ability']:

    def unyielding(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        def ready_hero(targets: Sequence['CardFace']) -> None:
            identity = initiator.GetIdentity()
            Faces.ReadyAll([identity], effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Spend 1 resource to ready your hero",
                ready_hero
            ).SetCostFunc(CostFunc.PayPrintCost(Cost("1")))
            .SetTarget("This")
        )

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            unyielding,
            take_no_damage=True,
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2)
    ]
