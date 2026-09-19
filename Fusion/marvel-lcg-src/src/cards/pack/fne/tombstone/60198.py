from . import *

# * Tombstone (CRIMINAL) — Quickstrike : base desc.
# [star] Boost: Give the villain a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
