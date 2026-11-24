from . import *

# Lady Yulan (A) : soigne 2 / defausse 6
# Voir capos/__init__.py (cartes de reference et pieges).

def GetAbilities() -> Sequence['Ability']:
    return LadyYulan(2, 6)
