from . import *

# * The Owl (AERIAL, CRIMINAL) — Quickstrike : base automatique.
# [star] The Owl's attacks gain piercing.
# [star] Boost: If this activation is an attack, it gains piercing.
#
# Modele exact : 04027 Crossfire.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainPiercing(effect)

    return [
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
