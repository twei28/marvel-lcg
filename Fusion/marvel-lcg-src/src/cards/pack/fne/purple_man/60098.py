from . import *

# * Purple Man (60098) : voir CapacitesDePurpleMan (guard=True, villainous=True, patrol=False).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=True, patrol=False),
    ]
