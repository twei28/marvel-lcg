from . import *


def GetAbilities() -> Sequence['Ability']:
    def armor_piercing_rounds(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        cible = list(effect.targets)
        degats = 5 if cible and cible[0].IsTough() else 2      # « If that enemy has a tough status card, deal 5 damage instead »
        this.DealDamage(cible, degats, effect)

    return [
        RessourceEnhancedCombatSense(CostFunc.Exhaust("This")),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            piercing=True,
            conditions=[AttaqueDeCetteCarte],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            armor_piercing_rounds,
            conditions=[ActionPayable("B")],
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("B"))
        .SetTarget(Enemy),
    ]
