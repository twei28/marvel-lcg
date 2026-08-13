from . import *

# Last Resort

def GetAbilities() -> Sequence['Ability']:

    def check_guardian_a_vous(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        if player is None:
            return False
        unite = message.trigger
        return unite.GetControlByPlayer() == player and unite.HasTrait("GUARDIAN")

    def last_resort(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.PreventDamage(6, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            last_resort,
            conditions=[check_guardian_a_vous],
        ).SetCostFunc(CostFunc.PlaceThreatOn(2, "MainScheme"))
        .SetCostFunc(CostFunc.Discard("This")),
    ]
