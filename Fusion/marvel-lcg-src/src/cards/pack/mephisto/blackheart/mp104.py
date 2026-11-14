from . import *

# Sinful Ambitions (mp104, deux exemplaires identiques) — TRAITRISE. Boost 1, Incite 2 (natifs). Capacites : `AbilitesDeSinfulAmbitions` (mephisto/__init__.py).
# ⚠ Mots-pieges : « If Blackheart is IN PLAY » ; « you MAY » ; « Otherwise » = pas de Blackheart, pas de pacte a remelanger, ou refus : la carte gagne Surge.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDeSinfulAmbitions(),
    ]
