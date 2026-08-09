from . import *

# Genius-Level Intellect — custom « Kajislav »
# You gain the GENIUS trait.
# While in hero form, Albert gets +1 THW.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            trait="GENIUS",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Albert", card_type=Hero),
            thwart=1,
        ),
    ]
