from . import *
from .jigsaw_commun import Jigsaw

# Jigsaw (pu057a) : voir jigsaw_commun.py

def GetAbilities() -> Sequence['Ability']:
    return [Jigsaw(1)]
