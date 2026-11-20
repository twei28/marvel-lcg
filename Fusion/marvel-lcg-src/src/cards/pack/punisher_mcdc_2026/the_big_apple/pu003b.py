from . import *

# Gunrunner's Warehouse (3B) — MANIGANCE PRINCIPALE. Menace 9 par joueur, depart 0, acceleration +1 par joueur.
# The villain with Gunrunner attached is the active villain and each player is considered to be in their turf.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference : pu003a (la mise en oeuvre de « active villain » et de « in their turf » a la REVELATION de 3A : compteur actif,
# regle `Villains.Rule("Active")`, tous les joueurs dans la zone du CAPO), pu090b (meme regle « is the active villain »).
# ⚠ Le texte est une regle permanente : aucun script propre ; la perte a l'accomplissement est native (dernier stade).

def GetAbilities() -> Sequence['Ability']:
    return []
