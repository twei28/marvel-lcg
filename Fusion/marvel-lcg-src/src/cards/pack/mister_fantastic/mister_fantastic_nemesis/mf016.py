from . import *

# Projection — custom « DesignHacker » (attachement némésis de Mister Fantastic)
# Incite 1. Surge. (desc)
# Attach to your identity card.
# [star] Boost: Attach to your identity card.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay('YourIdentity'),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
