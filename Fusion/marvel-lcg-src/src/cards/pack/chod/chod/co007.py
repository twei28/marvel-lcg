from . import *

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Ch'od"),
            hand_size=1,
        ),
    ]
