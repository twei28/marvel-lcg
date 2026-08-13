from . import *

# Determined Conditioning

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            defense=-1,
            retaliate=1,
        ),
    ]
