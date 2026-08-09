from . import *
def GetAbilities() -> Sequence['Ability']:
    def sensory_overload(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        player.GetIdentity().TakeIndirectDamage(this, 1, effect)
    def after_recover(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.DiscardAll([this], effect)
    def check_sense(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> bool:
        return message.trigger.HasTrait('SENSE')
    return [AbilityFactory.WhenCardEnterPlay(AbilityType.ForcedResponse, Upgrade, sensory_overload, conditions=[check_sense]),
            AbilityFactory.AfterUnitRecovery(AbilityType.Response, 'YourIdentity', after_recover)]
