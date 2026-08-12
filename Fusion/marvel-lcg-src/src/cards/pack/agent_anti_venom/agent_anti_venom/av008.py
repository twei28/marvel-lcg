from . import *

# Anti-Maniac Booster — custom « DesignHacker »
# Agent Anti-Venom gains retaliate 1.
# Response: After Agent Anti-Venom takes damage from an attack, exhaust
#   Anti-Maniac Booster -> heal 1 damage from Agent Anti-Venom.

def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        identity = GetAgentAntiVenom(effect)
        if identity is not None:
            this.HealthUnits([identity], 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            retaliate=1,
        ),

        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            booster,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
