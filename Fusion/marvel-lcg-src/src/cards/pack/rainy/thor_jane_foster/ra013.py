from . import *

# Mighty — custom "Rainy"
# You get +2 hit points. Thor gets +1 DEF and gains retaliate 1.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(card_type=Identity),
            health=2,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Thor"),
            defense=1,
            retaliate=1,
        ),
    ]
