from . import *

# Lady Yulan (B, expert) : soigne 3 / defausse 10
# Voir capos/__init__.py (cartes de reference et pieges).

def GetAbilities() -> Sequence['Ability']:
    return LadyYulan(3, 10)
