from . import *

# Lizardmen

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Give the villain a tough status card. »
        villain = Worlds.FindVillain(effect)
        if villain:
            Faces.GiveStatus([villain], "Tough", effect)

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
