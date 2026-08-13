from . import *

# In Harm's Way

def GetAbilities() -> Sequence['Ability']:

    def check_ami(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        initiator = effect.GetInitiator()
        return message.trigger.GetControlByPlayer() == initiator

    def in_harms_way(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        message.PreventDamage(initiator.DeclareNumber(0, 5), effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            in_harms_way,
            conditions=[check_ami],
        ).SetPlay().SetLabel('defense')
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
