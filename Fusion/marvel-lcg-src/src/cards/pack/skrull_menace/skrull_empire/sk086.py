from . import *

# Skrull Empire (1) — ENVIRONNEMENT du stade 1. PV 14[per_hero], portes a la place des mechants.

# Incite Rebellion — Hero Action: Choose to either exhaust your hero or spend 2
#   resources of any type → choose 1 PLANET environment in play. Treat its
#   printed text box as if it were blank until the end of the round. (Limit
#   once per round per player.)
#
# Cartes de reference :
#  - **`21100a`** Avengers Tower : un environnement qui encaisse en compteurs
#    'damage' et agit a un seuil (`AfterCounterPlacedOn(..., at_least=...)`).
#  - **`39031`** Undercover Mojo : `WhenUnitWouldTakeDamage(ForcedInterrupt,
#    Villain, op)` + `SetBeInstead`, les degats du mechant detournes.
#  - **`16073b`** The Grand Collection : MEME cout « exhaust your hero or spend
#    2 resources of any type », `CostFunc.Custom` + `ForChoiceAbilityWithCost`.
#  - **`40092`** / treat_blank.py : `TreatAsIfBlankInternal` ; retablissement
#    en fin de round par `RunAt.RoundEnd`.
#  - `next_evol/mister_sinister` : remelanger des cartes mises de cote.
#
# ⚠ Mots-pieges : « Limit once per round PER PLAYER » ; « its PRINTED text box »
# (les traits LOCATION/PLANET restent) ; « until the end of the ROUND ». Le
# cadran de PV : decision de l'utilisateur du 15/10/2026 (vrai cadran, publie
# par Environment.cadran_pv). Detail des regles du stade : __init__ du set.


def GetAbilities() -> Sequence['Ability']:
    return EnvironnementAbilities(avec_overthrow=False)
