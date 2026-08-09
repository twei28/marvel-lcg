from . import *

# Kevlar Shell — custom « Kajislav »
# While in hero form, Albert gets +1 DEF and gains retaliate 1.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Albert", card_type=Hero),
            defense=1,
            retaliate=1,
        ),
    ]
