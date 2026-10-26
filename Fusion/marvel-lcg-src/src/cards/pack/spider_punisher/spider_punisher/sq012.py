from . import *


def GetAbilities() -> Sequence['Ability']:
    def swing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    def si_aerien(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return EstAerien(effect.GetInitiator())

    def reload(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swing,
            conditions=[si_aerien],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Upgrade, canbe_ready=True, exclude="This"),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            reload,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
