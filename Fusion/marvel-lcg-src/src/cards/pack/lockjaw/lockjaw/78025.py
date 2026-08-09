from . import *

# * Ms. Lion — custom « Nugget » (carte d'aspect BASIC)
# Companion. (Aucune autre capacité imprimée.)


def GetAbilities() -> Sequence['Ability']:

    return [
        *Companion(),
    ]
