from . import *

# hs031 * Scorpion

def GetAbilities() -> Sequence['Ability']:
    return [
        ForcedInterruptQueue(),
        AbilityFactory.UnitCannotBeStunned("This"),
    ]
