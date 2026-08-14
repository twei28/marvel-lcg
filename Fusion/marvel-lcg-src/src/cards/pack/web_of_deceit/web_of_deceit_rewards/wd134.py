from . import *

# Clairvoyant Sight

def GetAbilities() -> Sequence['Ability']:

    return [
        # « You gain the PSIONIC trait. »
        *AbilityFactory.GiveKeywordToAttached(
            trait="PSIONIC",
        ),
    ]
