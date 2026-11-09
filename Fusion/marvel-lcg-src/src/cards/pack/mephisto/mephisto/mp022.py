from . import *

# Dark Compulsions (mp022, deux exemplaires identiques) — TRAITRISE. Pas d'icone de boost imprimee.
# Capacites : `AbilitesDeDarkCompulsions` (voir mephisto/__init__.py). Reference : cw/spider_woman/56178 (`WhenCardBecomeBoost` + `GainBoostIcons`).
# ⚠ Mots-pieges : « EACH player ... IF THEY control » (une Hidden Clause par joueur qui a un pacte, une seule par joueur) ; « IF NO PLAYER controls »
# (la branche facultative ne part que si personne n'en a) ; icones de boost = pactes EN JEU (tous les joueurs), pas seulement les siens.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDeDarkCompulsions(),
    ]
