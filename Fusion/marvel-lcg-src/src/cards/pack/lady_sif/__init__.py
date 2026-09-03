from cards.pack import *

# ===========================================================================
# Pack LADY SIF — contenu custom de « Rainy ». Set 150, prefixe `ls`.
#
# DEUX sets dans ce pack, et c'est le seul de la vague 0 dans ce cas :
#   - `Lady Sif`         (ls001a-ls012, dossier lady_sif/lady_sif/)
#   - `Lady Sif Nemesis` (ls013-ls017, dossier lady_sif/lady_sif_nemesis/)
# 18 card_id : 2 faces d'identite, 10 cartes signature distinctes en 15
# exemplaires, 1 obligation, 5 cartes nemesis.
#
# ⚠ `FileManager.CleanName` rend `lady_sif` et `lady_sif_nemesis` : ce sont
# bien les noms des deux dossiers de modules, et c'est eux que
# `database.py:197` cherchera (leçon bt019, dont le module n'etait jamais
# charge, en silence).
# ⚠ `set_name` = « Lady Sif », verifie LIBRE : l'homonyme officiel `06002` est
# un ALLIE signature de Thor, pas un set.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : LES POUVOIRS DE BASE PAIENT DEUX FOIS
#
#   ls001a Valiant Warrior -> chaque pouvoir de base retire 1 menace
#   ls009 Sif's Crest      -> chaque pouvoir de base pioche 1 carte (1/phase)
#   ls008 Sif's Steed      -> chaque epuisement peut etre annule
#   ls004 Lead The Charge  -> une attaque de base EN PLUS, sans epuiser
#   ls006 Valiant Defense  -> une defense de base EN PLUS, sans epuiser
#
# Lady Sif frappe et contre avec ses statistiques imprimees plutot qu'avec des
# evenements : CTR 1 / ATQ 2 / DEF 2 ne paient pas gros, mais ils paient A
# CHAQUE FOIS, et le pack multiplie les occasions de s'en servir.
#
# ---------------------------------------------------------------------------
# ⚠ TROIS BASES AUTOMATIQUES DANS CE PACK, AUCUN SCRIPT POUR ELLES :
#   - `Restricted` (ls010, ls011)      -> `desc.Restricted`
#   - `Toughness`  (ls015)             -> `desc.Toughness`
#   - `Teamwork (ASGARD)` (ls015)      -> `desc.Teamwork`, fiche
#     docs/reference/mots-cles/teamwork.md, ecrite pour ce pack le 03/09/2026.
# Les recoder ferait doubler leur effet — pour Teamwork, le sbire s'activerait
# DEUX fois.
#
# ⚠ Le trait `TEMPTATION` (ls016, ls017) a ete AJOUTE a l'enum `TRAITS`
# (`src/game/card/face/card_face.py`) pour ce pack : sans lui, les deux
# attachements tombent a la construction, pas en jeu.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES PREEXISTANTS, verifies dans data/cards.json le 02/09/2026 :
#  - « Lady Sif » : `06002`, ALLIE signature de THOR (desc.Class = "Hero"),
#    et `21190` (campagne MTS). Notre heros porte le meme nom : le controle
#    « jamais une signature d'un autre heros dans un deck » (PROCESSUS-HEROS
#    etape 10) doit rester vert, et le deck le documente ;
#  - « Thor » (ls002) : six homonymes, dont le heros officiel `06001a`, les
#    allies `13011`/`25013`/`59020` et `ra001a` (Jane Foster). Notre allie est
#    une carte DISTINCTE de `25013`, aux capacites differentes ;
#  - « Enchantress » (ls014) : quatre homonymes officiels — c'est la
#    cinquieme ;
#  - « Skurge » (ls015) : `21144`, sbire du set Hela ;
#  - « Hypnotic Suggestion » (ls016) : `ag014`, traitrise d'un pack MAISON ;
#  - « Love Concoction » (ls017) : `55014`, meme personnage source, carte
#    differente.
# ⚠ « Shieldmaiden », le nom de la capacite de ls001b, est aussi le nom de la
# carte OFFICIELLE `25011` (Valkyrie) — dont le montage sert de modele a
# ls006. Deux choses distinctes qui portent le meme mot.
# ===========================================================================

# ⚠ Les helpers partages d'un set vivent dans le `__init__.py` DU SET, pas
# ici : les modules font `from . import *`, qui importe le `__init__` du
# dossier du set. Un helper defini ici leve un `NameError` avale par le
# moteur, et la carte echoue en silence (paye sur hk005 le 02/09/2026).
