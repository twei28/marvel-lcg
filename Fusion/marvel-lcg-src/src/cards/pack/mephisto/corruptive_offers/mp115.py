from . import *

# Soul Gambling (mp115, deux exemplaires identiques) — TRAITRISE (Corruptive Offers). Pas d'icone de boost imprimee.
# Capacites : `AbilitesDeSoulGambling` (mephisto/__init__.py). Reference : `ThisCardGainSurge`, `ShuffleThisCardIntoEncounter` (pack/__init__), `MettreDeCoteLeDessus`.
# ⚠ Mots-pieges : « EACH player » : chacun avec SES pactes ; X = la SOMME des compteurs corrupt de tous ses BARGAIN, X[per_hero] cartes ; « Otherwise » : si rien n'a
# ete mis de cote (personne n'a de compteur), surge ; Boost : « each BARGAIN YOU control » (le joueur vise), « if NO counters were placed » = aucun pacte.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDeSoulGambling(),
    ]
