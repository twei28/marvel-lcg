from . import *

# Mister Negative (B, expert) : la carte de boost de plus donne aussi overkill
# Voir capos/__init__.py (cartes de reference et pieges).

def GetAbilities() -> Sequence['Ability']:
    return MisterNegative(True)
