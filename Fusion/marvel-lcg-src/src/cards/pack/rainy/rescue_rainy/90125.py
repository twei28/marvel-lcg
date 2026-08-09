from . import *

# Repulsor Gauntlets

def GetAbilities() -> Sequence['Ability']:

    def portee(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.property.ranged = True

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Rescue"),
            attack=1,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            CardFinder(name="Rescue"),
            portee,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
