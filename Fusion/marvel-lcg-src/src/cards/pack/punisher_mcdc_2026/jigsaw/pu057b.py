from . import *
from .jigsaw_commun import Jigsaw

# Jigsaw (pu057b, expert final) : 2 menace au lieu de 1

def GetAbilities() -> Sequence['Ability']:
    return [Jigsaw(2)]
