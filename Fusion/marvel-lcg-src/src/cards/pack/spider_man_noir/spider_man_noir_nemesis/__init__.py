from cards.pack import *

# ===========================================================================
# Pack SPIDER-MAN NOIR — set nemesis « Spider-Man Noir Nemesis »
# (sn012-sn015, Rainy, set 160).
#
# Electro Noir attaque le heros PAR SA PILE. Les quatre cartes visent la meme
# ressource, celle sans laquelle Spider-Man Noir a ATQ 0 et CTR 0 :
#   - sn012 Power Struggle punit le contre lui-meme (1 degat par contre) et
#     porte AMPLIFY, donc grossit toutes les cartes de boost ;
#   - sn013 Electro Noir SE NOURRIT de la pile : il prend une carte glissee
#     comme carte de boost, ce qui lui donne de la force en RETIRANT au heros
#     son ATQ et son CTR du meme coup ;
#   - sn014 Lightning Strikes Twice fait payer la pile en degats, une par
#     icone de boost ;
#   - sn015 Thunderstorm donne SURGE a tout le set et saigne le heros a chaque
#     surge resolu.
#
# ⚠ « Electro Noir » (sn013) n'a RIEN de commun avec les onze Electro du
# depot, dont les six du pack `web_of_deceit` (`wd021`, `wd025`, `wd035`-`37`,
# `wd046`, `wd047`). Nom different, texte different, aucun code partage.
#
# ⚠ ELITE EST UN TRAIT, PAS UN MOT-CLE. Il se declare dans `traits`, jamais
# dans `desc`, et le moteur ne lui associe aucune mecanique (voir l'encadre du
# README des mots-cles). C'est la confusion la plus frequente sur un set
# nemesis.
# ===========================================================================

NOM_SBIRE = "Electro Noir"
