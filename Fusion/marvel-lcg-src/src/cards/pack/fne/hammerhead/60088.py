from . import *

# * Hammerhead (60088) : [star] Forced Response, 2 degat(s) sur un personnage deja etourdi.
# Toughness / Retaliate sont des bases automatiques lues dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseForceeCoupDeBoule(2),
    ]
