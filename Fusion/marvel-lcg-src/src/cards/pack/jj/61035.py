from . import *
def GetAbilities() -> Sequence['Ability']:
    def shakedown(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        minion = message.target
        n = minion.printed_scheme or 0
        this.RemoveThreatFromSchemes(effect.targets, n, effect)
    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.Response, "You", Minion, shakedown, is_from_attack=True, has_excess_damage=False)
        .SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Scheme2, range=(1, 1)),
    ]
