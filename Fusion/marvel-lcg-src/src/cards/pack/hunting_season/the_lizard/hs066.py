from . import *

# Alligator Jaws

def GetAbilities() -> Sequence['Ability']:

    def perforant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)

    return [
        AttacherAuLizard(),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "AttachedVillain", perforant),
        ActionHeros(Cost("R"), CostFunc.Exhaust("YourHero")),
    ]
