from . import *

# Preparation #2

def GetAbilities() -> Sequence['Ability']:

    def preparation_2(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetHero()], effect)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            preparation_2
        ).SetCostFunc(CostFunc.DealDamage(2, "YourHero"))
        .SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("YourEngagedMinions", range="All"),
    ]
