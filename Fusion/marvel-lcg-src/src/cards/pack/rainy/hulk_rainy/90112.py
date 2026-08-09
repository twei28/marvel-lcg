from . import *

# Limitless Endurance

def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Bruce Banner"),
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            soigner,
            conditions=[
                lambda effect, message:
                    effect.GetInitiator().GetHero().CanHeath()
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
