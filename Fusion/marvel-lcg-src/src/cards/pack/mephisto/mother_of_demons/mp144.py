from . import *

# Spawn Magic (mp144, deux exemplaires identiques) — TRAITRISE. Boost 1 (natif). Capacites : `AbilitesDeSpawnMagic` (mephisto/__init__.py).
# ⚠ Mots-pieges : « the top 2 cards of YOUR discard pile » (les deux, chacune face cachee et engagee) ; « Otherwise, FIND Call of the Demoness and reveal it » : deck, defausse
# et zone mise de cote ; Boost « resolve this card's When Revealed » : par le joueur vise par l'activation, comme a la revelation.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDeSpawnMagic(),
    ]
