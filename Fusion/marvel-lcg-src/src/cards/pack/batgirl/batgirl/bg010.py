from . import *

# Armored Suit — amelioration, cout 2, [physical]. « You get +3 hit points. Hero Interrupt: When you would take any amount of damage,
# exhaust Armored Suit → prevent 1 of that damage. »
# Cartes de reference : `01081` Armored Vest (`CanPlayThisUpgradeCard` + `GiveKeywordToAttached`), `03005` Shield Block
# (`WhenUnitWouldTakeDamage(.., "You", ..)` + `message.PreventDamage`).


def GetAbilities() -> Sequence['Ability']:

    def armored_suit(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Identity, health=3),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            armored_suit,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
