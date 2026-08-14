from . import *

# Proportionate Strength and Speed

def GetAbilities() -> Sequence['Ability']:

    return [
        # « You get +3 hit points and your hero gets +1 DEF and +1 ATK. »
        *AbilityFactory.GiveKeywordToAttached(
            health=3,
            defense=1,
            attack=1,
        ),
    ]
