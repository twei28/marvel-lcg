from . import *

# Hammer Swing — custom "Rainy"
# Hero Action (attack): Exhaust Mjolnir and spend 1 resource of any type ->
# deal 4 damage to an enemy.
# Hero Interrupt (defense): When you would take any amount of damage,
# exhaust Mjolnir -> prevent all of that damage.

def GetAbilities() -> Sequence['Ability']:

    def swing_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        this.DealDamage(effect.targets, 4, effect)

    def swing_defense(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swing_attack
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(
            name="Mjolnir",
            card_type=Upgrade,
            from_where=["YouControlCards"]))
        .SetCostFunc(CostFunc.PayPrintCost(Cost("1")))
        .SetTarget(Enemy),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            swing_defense,
        ).SetPlay(hero_form_only=True)
        .SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust(
            name="Mjolnir",
            card_type=Upgrade,
            from_where=["YouControlCards"]))
    ]
