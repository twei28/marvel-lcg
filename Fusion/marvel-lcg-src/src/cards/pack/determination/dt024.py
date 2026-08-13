from . import *

# * Elektra

def GetAbilities() -> Sequence['Ability']:

    return [
        Fragile(),
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            ranged=True
        ),
    ]
