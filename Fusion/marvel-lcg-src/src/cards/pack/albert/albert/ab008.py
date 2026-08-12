from . import *

# Adamantium Claws — custom « Kajislav »
# While in hero form, Albert gets +1 ATK and his basic attacks gain piercing.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Albert", card_type=Hero),
            attack=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Albert", card_type=Hero),
            is_basic_attack=True,
            piercing=True,
        ),
    ]
