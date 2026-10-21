from . import *
from .jigsaw_commun import Jigsaw

# Jigsaw (pu056a) : voir jigsaw_commun.py

def GetAbilities() -> Sequence['Ability']:
    return [Jigsaw(1)]
