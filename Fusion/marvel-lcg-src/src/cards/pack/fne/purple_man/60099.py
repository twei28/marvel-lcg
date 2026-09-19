from . import *

# * Purple Man (60099) : voir CapacitesDePurpleMan (guard=True, villainous=True, patrol=True).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=True, patrol=True),
    ]
