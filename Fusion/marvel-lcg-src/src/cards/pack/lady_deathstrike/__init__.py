from cards.pack import *

# ===========================================================================
# Pack LADY DEATHSTRIKE — scenario custom de « Mysteltainn » (« MC Custom Content By: Mysteltainn »),
# inspire de X-Force (2011). Prefixe `ld` (tools/prefixes_fanmade.json), set 213.
#
# DEUX sets dans ce pack :
#   - `Lady Deathstrike` (ld001-ld014, dossier lady_deathstrike/lady_deathstrike/) : les 3 stades du vilain, le complot principal
#     Mutant Hunting Season (ld004a/b), Bleeding Out (ld005, x4 mis de cote) et les 15 cartes de rencontre ;
#   - `Reaver Resources` (ld015-ld018, dossier lady_deathstrike/reaver_resources/) : modulaire maison, version allegee du
#     Military Grade officiel (FAQ de l'auteur : 3 cartes identiques, une arme et une manigance annexe differentes).
#
# ⚠ `FileManager.CleanName` rend `lady_deathstrike` et `reaver_resources` : les noms des deux dossiers de modules.
#
# LE SCENARIO EN UNE PHRASE : UNE CAPACITE « SPECIAL » QU'ON RESOUT PAR REFERENCE.
# Bleeding Out (Permanent, attachee a l'identite de CHAQUE joueur, 3 compteurs bleed au depart) porte la capacite nommee
# « Special » : +1 compteur bleed, defausse du dessus du deck autant de cartes que de compteurs, 1 degat si une carte
# SPECIFIQUE A L'IDENTITE est defaussee. Neuf cartes la font resoudre (villain, Tracker, Bide Time, Mutant Hunter, Claws,
# Nanoskeleton...). Helper unique `ResoudreSaignement` du set : il rend « a-t-on defausse une carte d'identite ? »
# (Reaver Tracker en depend).
#
# ⚠ HOMONYMES au depot : `* Lady Deathstrike` (35034 Deathstrike, 43029 X-23 Nemesis : des SBIRES), Titanium Exoskeleton et
# Inhibitor Collar (40091/40092 Military Grade, MEMES textes), Stalking Prey (hs123, Kraven). Aucun module du pack ne cherche
# par NOM le vilain : tout passe par card_id (`IDS_VILAIN`).
# ===========================================================================
