from . import *

# Sebastian Shaw (stade III, mode expert), vilain. Meme texte que (I)/(II) + « Place 1 additional energy counter here. » a la fin de l'Absorb.
# Cartes de reference : voir hf201.


def GetAbilities() -> Sequence['Ability']:
    return AbilitesDeShaw(energie_en_plus=1)
