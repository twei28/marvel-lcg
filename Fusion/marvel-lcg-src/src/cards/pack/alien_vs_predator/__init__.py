from cards.pack import *

# ===========================================================================
# Pack ALIEN VS. PREDATOR — scenario custom de « RyCoRan » (« Custom Content By: RyCoRan », 06-26), 25/10/2026. Prefixe `ap`
# (tools/prefixes_fanmade.json), set 216. QUATRE sets :
#   alien_vs_predator/  « Alien vs. Predator » (ap001a-ap033 : mechants, complots, manigances, rencontre)
#   xenomorph_deck/     « Xenomorph Deck »     (ap101-ap104 : les 4 versions d'Alien Scout, 16 cartes)
#   apex_standard/      « Apex Standard »      (ap201-ap207 : remplace le Standard)
#   clan_yautja/        « Clan Yautja »        (ap301-ap306 : modulaire)
#
# LE SCENARIO EN UNE PHRASE : DEUX MECHANTS QUI SE PASSENT LE COMPTEUR ACTIF.
# Alien Queen et Predator Warlord sont en jeu ensemble ; seul le mechant ACTIF s'active (arbitrage du 25/10/2026), puis le
# compteur passe a l'autre (1B : apres chaque activation ; 2B : apres chaque attaque). Chacun manigance sur SA manigance annexe
# permanente (Expanding Hive / Skulls for the Taking). Le premier vaincu se retourne (face « Defeated ») : il soigne l'autre,
# saute au stade 3A (Reine vaincue) ou 4A (Warlord vaincu) et retire les deux manigances permanentes ; le second vaincu fait
# GAGNER les joueurs (arbitrage du 25/10/2026). Le deck Xenomorph (16 Alien Scout) est glisse sous la Reine : elle en melange un
# dans le deck du joueur qu'elle blesse ; un Scout pioche (ou defausse du deck) est distribue face cachee comme carte de rencontre.
#
# Transcriptions et arbitrages : docs/packs/alien-vs-predator/TRANSCRIPTIONS.md. Gabarits : docs/packs/alien-vs-predator/GABARITS.md.
#
# ⚠ Les modules d'un set font `from . import *` : ils voient le `__init__.py` de LEUR set, pas celui-ci (NameError avale par le
# moteur, lecon hk005). Les helpers partages vivent dans `commun.py`, que chaque `__init__.py` de set importe en entier.
# ===========================================================================
