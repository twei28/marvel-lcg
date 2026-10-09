from . import *

# hs045 * Hippo

def GetAbilities() -> Sequence['Ability']:
    def boost(effect, message):
        message.would_atk_message.GainOverKill(effect)
    return [AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True)]
