from . import *

# * Bloody Mary (Mary Walker) — Victory -1 : base.
# [star] Forced Response: After you reveal a side scheme, remove all damage
#   from here and flip this card.

def GetAbilities() -> Sequence['Ability']:
    return [RechuteVers(EncounterSideScheme)]
