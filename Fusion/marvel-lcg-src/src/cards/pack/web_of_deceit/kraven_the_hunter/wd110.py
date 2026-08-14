from . import *

# Tiger

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: If this activation is an attack, it gains piercing. »
        message.would_atk_message.GainPiercing(effect)

    return [
        # « [star] Tiger's attacks gain piercing. »
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
            during_attack=True,
        ),
    ]
