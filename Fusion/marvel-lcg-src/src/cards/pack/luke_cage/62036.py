from . import *
def GetAbilities() -> Sequence['Ability']:
    def toughen_up(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        identity = effect.GetInitiator().GetIdentity()
        if identity:
            Faces.GiveStatus([identity], "Tough", effect)
    def check_full_hp(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> bool:
        identity = effect.GetInitiator().GetIdentity()
        return bool(identity and identity.health >= identity.printed_health)
    return [
        AbilityFactory.AfterUnitRecovery(AbilityType.Response, "You", toughen_up, conditions=[check_full_hp])
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
