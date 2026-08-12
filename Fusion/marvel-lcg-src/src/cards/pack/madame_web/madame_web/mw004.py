from . import *

# Clairvoyance — custom « Kajislav »
# Hero Interrupt: When you would take any amount of damage, exhaust
#   Clairvoyance -> prevent 1 of that damage.

def GetAbilities() -> Sequence['Ability']:

    def clairvoyance(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.PreventDamage(1, effect)

    return [
        # Pas de CanPlayThisUpgradeCard : amelioration signature posee devant
        # soi, pas attachee a une carte choisie (lecon du pack totally_awesome_hulk).
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            clairvoyance
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
