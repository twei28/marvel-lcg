from . import *
def GetAbilities() -> Sequence['Ability']:
    def fogwells_gym(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        Faces.ReadyAll([message.trigger], effect)
    def check_defender(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> bool:
        return message.trigger.HasTrait('DEFENDER')
    return [
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.Response, None, "Tough", fogwells_gym, conditions=[check_defender])
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
