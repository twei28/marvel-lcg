from . import *

# Scavenged Bulwark — Surge (base).
# When Revealed: Give the villain a tough status card.
# [star] Boost: If Bloody Mary is activating, give her a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Bloody Mary"):
            Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
