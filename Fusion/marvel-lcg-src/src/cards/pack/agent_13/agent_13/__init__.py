from cards.pack import *

# Pack custom « Rainy » — Agent 13 (Sharon Carter).
# Mecanique du pack : COMPTER LES ICONES DE BONUS D'UNE CARTE DE RENCONTRE.
# Trois cartes s'appuient dessus : Sharon Carter (ag001b, action alter-ego :
# remet une carte de la defausse de rencontre sur le deck puis retire de la
# menace selon ses icones de bonus), Infiltrate (ag004) et Agent 13's Pistol
# (ag008). Le moteur sait deja compter ces icones :
# `FacesCounter.CountTotalBoostIcons` et `HasBoostIcon.CountBoostIconsInternal`
# (src/game/card/face/attribute/has_boost_icon.py). Precedent officiel a
# reprendre pour ces trois cartes : Scarlet Witch, qui regarde la carte du
# dessus du deck de rencontre et compte ses icones (src/cards/pack/scw/
# scarlet_witch/15004.py).
#
# Ce fichier ne porte que l'arborescence et ce commentaire d'ensemble : les
# six cartes de cette tache (ag002, ag003, ag006, ag007, ag009, ag010) n'ont
# pas besoin de compter les icones de bonus. Les trois cartes ci-dessus
# viennent dans une tache separee.
