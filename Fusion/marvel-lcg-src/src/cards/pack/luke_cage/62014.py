from . import *
def GetAbilities() -> Sequence['Ability']:
    def valkyrie(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        target = message.trigger
        message.SetBeInstead(effect)
        target.SetHealth(1, effect)
        Faces.DiscardAll([this], effect)
    def check_another_ally(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        return Ally.IsType(message.trigger) and message.trigger != effect.this
    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.Interrupt, None, valkyrie, conditions=[check_another_ally])
        .SetCostFunc(CostFunc.Discard("This")),
    ]
