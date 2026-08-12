from . import *


def GetAbilities() -> Sequence['Ability']:

    def invisible_barrier(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        attacker = message.trigger.CastTo(Unit2)
        effect.this.DealDamage([attacker], 1, effect)

    def attacker_has_2_atk(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return message.trigger.CastTo(Unit2).attack >= 2

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.Interrupt,
            Enemy,
            invisible_barrier,
            conditions=[attacker_has_2_atk],
        ).SetName("Invisible Barrier"),
    ]
