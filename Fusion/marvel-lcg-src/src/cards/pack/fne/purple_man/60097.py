from . import *

# * Purple Man (60097) : voir CapacitesDePurpleMan (guard=True, villainous=False, patrol=False).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=False, patrol=False),
    ]
