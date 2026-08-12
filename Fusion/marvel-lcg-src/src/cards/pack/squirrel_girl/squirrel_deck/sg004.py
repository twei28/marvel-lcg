from . import *

# The Lookout
# Aucune capacite imprimee : le corps de manigance du deck ecureuil.

def GetAbilities() -> Sequence['Ability']:
    return [
        *Ecureuil(),
    ]
