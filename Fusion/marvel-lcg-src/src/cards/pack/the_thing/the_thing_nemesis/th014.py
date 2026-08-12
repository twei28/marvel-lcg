from . import *

# * Hulk — custom « DesignHacker » (sbire némésis de The Thing)
# Guard (desc).
# [star] Hulk's attacks gain piercing and overkill.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            overkill=True,
        ),
    ]
