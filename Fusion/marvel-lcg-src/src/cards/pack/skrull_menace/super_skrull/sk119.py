from . import *

# * Super-Skrull — MECHANT, stade III (Super-Skrull). SKRULL. SCH 2, ATK 2,
# PV 19[per_hero].
# Forced Response: After resolving step two of the villain phase, shuffle each
#   SUPERPOWER attachment from play into the SUPERPOWER deck and reveal the top
#   2 cards of the SUPERPOWER deck.
#
# Cartes de reference :
#  - **`04079b`** None Shall Pass : `AfterResolveVillainPhaseStep(ForcedResponse,
#    1, op)` ; ici l'etape 2 (activation du mechant et des sbires, world.py).
#  - **`hs107a`** + `hunting_season/trap` : paquet de scenario cree a la mise en
#    place, cartes melangees dedans (`ShuffleAllTo`), revelees du dessus ; helpers
#    `RenouvelerSuperpouvoirs` / `ReponseDuMechant` du set (__init__).
#
# ⚠ Mots-pieges : « AFTER resolving step TWO » (pas l'etape 1 ni 3) ; « EACH
# SUPERPOWER attachment FROM PLAY » (les 4 reviennent, y compris ceux qu'une carte
# aurait defausses : voir en-tete du set) ; le paquet est MELANGE avant la
# revelation ; DEUX cartes revelees (stades II et III). PV `19*` = par joueur (desc), ATK/SCH sans etoile.


def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseDuMechant(2),
    ]
