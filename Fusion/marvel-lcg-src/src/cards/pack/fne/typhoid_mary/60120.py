from . import *

# Hand Lookout (HAND, NINJA) — Guard, Toughness : bases.
# [star] Boost: Give the activating enemy an additional boost card. (11041)

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GiveBoostCardForThisActivation(Enemy, 1, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
