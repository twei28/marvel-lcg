from . import *

# * Vulture (I)

def GetAbilities() -> Sequence['Ability']:

    return [
        # « Vulture cannot be attacked during the player phase unless the
        # attacker or attack has the AERIAL trait, or the attack has ranged. »
        NePeutEtreAttaqueQueParLesAeriens(),
    ]
