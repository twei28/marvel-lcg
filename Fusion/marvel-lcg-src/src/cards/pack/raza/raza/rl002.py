from . import *
def GetAbilities() -> Sequence['Ability']:
    def tolo_hawk(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        message.SetBeInstead(effect)
        identite = IdentiteDe(effect)
        if identite is not None:
            this.DealDamage([identite], 1, effect)
        if this.sustained > 0:
            this.HealHealth(this.sustained, effect)
    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            tolo_hawk,
            by_consequential_damage=True,
        ),
    ]
