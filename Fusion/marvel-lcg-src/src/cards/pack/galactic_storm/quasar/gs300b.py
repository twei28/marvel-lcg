from . import *

# * Wendell Vaughn — face ALTER EGO (identite 1B, pied « HAND SIZE 6 / HIT POINTS 11 »).
# S.H.I.E.L.D. REC 3, MNG 6, 11 PV.
# Chosen as the Protector — Setup: Put Quantum Bands into play.
#
# Cartes de reference :
#  - **`sk001b`** * Teddy Altman (meme auteur) : « Setup: Put your origin form
#    upgrade into play » = `SetupPutIntoPlay(["sk002a,sk002b"], ...)` ;
#  - **`as001b`** * Peter Parker (Earth-31198) : meme fabrique, amelioration
#    PERMANENTE fabriquee au Setup (pas dans les 15 cartes du deck de heros).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Put Quantum Bands into play » : la 16e carte du set (QUASAR 1/16),
#    absente des 15 cartes du deck de heros ; `SetupPutIntoPlay` la FABRIQUE
#    puis la met en jeu sous le controle du joueur (factory/setup.py).
#  - « Setup » : une seule fois, a la mise en place, quelle que soit la forme
#    de depart (le joueur commence en alter ego, face qui porte le texte).
#  - Pas d'autre capacite : REC 3 et la taille de main sont lus dans `desc`.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.SetupPutIntoPlay(["gs301"]),
    ]
