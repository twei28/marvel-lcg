from . import *

# * Mjolnir — custom "Rainy" (Jane Foster)
# Restricted. Thor gets +1 ATK and gains the AERIAL trait.
# Hero Action (attack): Discard Mjolnir -> deal 2 damage to an enemy.
# This attack gains ranged.

def GetAbilities() -> Sequence['Ability']:

    def hammer_throw(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        this.DealDamage(
            effect.targets, 2, effect,
            property=AttackProperty(ranged=True))

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Thor"),
            attack=1,
            trait="AERIAL",
        ),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hammer_throw
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Enemy),
    ]
