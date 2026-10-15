from cards.pack import *

# ===========================================================================
# Pack MICHELANGELO (TMNT Heroes v3, auteur Inkwire). Prefixe `tm`.
#
# DEUX sets dans ce pack :
#   - `Michelangelo`          (tm001a-tm013, dossier michelangelo/michelangelo/)
#   - `Michelangelo Nemesis`  (tm014-tm016, dossier michelangelo/michelangelo_nemesis/)
# 17 card_id : 2 faces d'identite, 11 cartes signature distinctes (15
# exemplaires), 1 obligation, 3 cartes nemesis distinctes (5 exemplaires).
#
# ⚠ `FileManager.CleanName` rend `michelangelo` et `michelangelo_nemesis` :
# ce sont bien les noms des deux dossiers de modules.
#
# ---------------------------------------------------------------------------
# LES MECANIQUES DU PACK
#   tm001a Booyakasha        -> deplace jusqu'a 3 menaces d'une manigance a une autre
#   tm001b Mikey (Setup)     -> met en jeu la manigance-joueur tm009 (I'm Here to Help)
#   tm001b Mikey (Action)    -> cherche jusqu'a 2 NUNCHUCK, mis en jeu inclines
#   tm011 / tm012            -> chaque NUNCHUCK que vous controlez GAGNE une capacite
#                               (GiveAbilityToInPlayWhenApplyThis, modele 50070)
#
# ⚠ BASES AUTOMATIQUES, AUCUN SCRIPT POUR ELLES (desc) : `Retaliate`,
# `Toughness` (tm002, tm015), `Restricted` (tm011, tm012), `Crisis` (tm014),
# `Boost` (icones). Les recoder ferait doubler leur effet.
#
# ⚠ Traits NEUFS au depot : NUNCHUCK, NINJA (deja pris par sunfire),
# TURTLE, MUTANIMAL, TEENAGER, NYC, SEWERS, WORMS. Le champ `traits` n'est
# lu a l'execution que par Teamwork (voir sunfire) : aucun fichier moteur
# partage n'est touche.
#
# ⚠ NOMS DE CARTES UNIQUES : `CardFinder(name=...)` s'ecrit SANS l'etoile
# (« Mikey », pas « * Mikey »), lecon sunfire sf012/sf014.
#
# ⚠ HOMONYMES : verifies le 15/10/2026 dans data/cards.json ET
# data/cards_custom.json (noms sans l'etoile) : AUCUN des 17 noms du pack
# n'existe deja.
# ===========================================================================

# ⚠ Les helpers partages d'un set vivent dans le `__init__.py` DU SET, pas
# ici (leçon hk005 : un helper defini ici leve un NameError avale par le
# moteur).
