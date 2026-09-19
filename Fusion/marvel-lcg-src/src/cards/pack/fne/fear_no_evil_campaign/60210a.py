from . import *

# * Typhoid Mary (Mary Walker) — alliee de campagne, Setup, Victory -1 : bases.
# [star] Forced Response: After you reveal a minion, remove all damage from
#   here and flip this card.
# « you » = le joueur qui controle l'alliee.

def GetAbilities() -> Sequence['Ability']:
    return [RechuteVers(Minion)]
