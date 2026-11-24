from . import *

# Meager Request (mp026, deux exemplaires identiques) — TRAITRISE. Pas d'icone de boost imprimee.
# Capacites : `AbilitesDeMeagerRequest` (voir mephisto/__init__.py). Reference : ar012 (`message.AfterThisActivation`), `ThisCardGainSurge` (pack/__init__).
# ⚠ Mots-pieges : « You MAY » : le refus donne Surge a cette carte (« Otherwise ») ; « If you do, resolve Hidden Clause » : seulement si accepte ;
# le Boost agit APRES l'activation (pas pendant), et revele le BARGAIN decouvert (pas d'attachement direct).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDeMeagerRequest(),
    ]
