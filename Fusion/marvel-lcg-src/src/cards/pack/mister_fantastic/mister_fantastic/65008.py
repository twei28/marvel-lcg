from . import *

# Neutralizer — custom « DesignHacker »
# Play under any player's control. Restricted. Uses (2 charge counters).
# Hero Interrupt: When you make a basic attack, exhaust Neutralizer and remove
# one charge counter from it -> you get +3 ATK for that attack. That attack
# gains overkill.

def GetAbilities() -> Sequence['Ability']:

    def neutralizer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainATKForThisAttack(3, effect)
        message.GainOverkill(effect)

    return [
        # « Play under any player's control » : la cible "Players" laisse
        # choisir l'identité à laquelle Neutralizer s'attache.
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            neutralizer,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
    ]
