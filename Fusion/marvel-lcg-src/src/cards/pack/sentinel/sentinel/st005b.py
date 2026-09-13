from . import *

# * Legs (Destroyed) — COMPONENT. DESTROYED. TECH.
# Permanent.
# You get -1 hand size.
#
# Carte de reference : `04165` Martial Law, mot pour mot
# (`GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)`), et `06007` Asgard
# pour le signe inverse.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **You** » : les DEUX faces de l'identite. Sentinel a 4 cartes en main en
#    heros et Juston 6 en alter-ego ; le malus s'applique aux deux, et c'est
#    pour cela que la cible est `"You"` et non un nom propre (piege inverse de
#    nt003a, ou le bonus visait le seul nom « Night Thrasher »).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            hand_size=-1,
        ),
    ]
