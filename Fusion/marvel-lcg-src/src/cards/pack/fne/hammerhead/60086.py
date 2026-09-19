from . import *

# * Hammerhead (60086) : [star] Forced Response, 1 degat(s) sur un personnage deja etourdi.
# Toughness / Retaliate sont des bases automatiques lues dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseForceeCoupDeBoule(1),
    ]
