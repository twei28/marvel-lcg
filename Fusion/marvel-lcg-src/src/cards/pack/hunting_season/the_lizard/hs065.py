from . import *

# Lizard Tail

def GetAbilities() -> Sequence['Ability']:

    def a_distance(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainRanged(effect)

    return [
        AttacherAuLizard(),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "AttachedVillain", a_distance),
        ActionHeros(Cost("B"), CostFunc.PlaceThreatOn(1, "MainScheme")),
    ]
