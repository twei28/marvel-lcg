from . import *
def GetAbilities() -> Sequence['Ability']:
    def reluctant_flier(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        message.PreventDamage("All", effect)
        this.DealDamage([message.trigger], 1, effect)
    def check_min_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.property.damage >= 3 and message.would_atk_message is not None
    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt, "You", reluctant_flier, conditions=[check_min_damage]
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
