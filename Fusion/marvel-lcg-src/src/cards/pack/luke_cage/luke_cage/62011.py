from . import *
def GetAbilities() -> Sequence['Ability']:
    def power_man(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        effect.GetInitiator().DrawUp(1, effect)
    return [
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.HeroResponse, "This", "Tough", power_man)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
