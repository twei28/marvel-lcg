from . import *

# * Shredder (I) — VILAIN, stade 1. FOOT CLAN. NINJA. MNG 1 / ATQ 2 / PV 12[per_hero].
# Shredder can have up to 2 cloaked status cards.
# Forced Response: After the villain phase ends, give Shredder a cloaked status card.
#
# Cartes de reference :
#  - `sk189b` (Queen Veranke I) : `AbilityFactory.AfterPhaseEnd(ForcedResponse,
#    "Villain", op)` pour « After the villain phase ends » ;
#  - `ThisCanHaveAdditionalCloaked(N)` (game/ability/factory/status.py), jumelle
#    de `ThisCanHaveAdditionalTough` (colossus 32001a) : le maximum de cartes
#    Cloaked est 1 + N (encart du scenario : « the Shredder can have more than
#    one, depending on his villain stage »).
#
# Mots-pieges : « up to 2 » = maximum, pas « toujours 2 » ; « give Shredder a
# cloaked status card » = UNE carte (le stade III en donne DEUX) ; « after the
# VILLAIN phase ends » (pas la phase des joueurs).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDeShredder(1)
