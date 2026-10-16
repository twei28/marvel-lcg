from cards.pack import *

# ===========================================================================
# Pack JENNIKA (TMNT Heroes v3, auteur Inkwire, « Kajislav/Inkwire »). Prefixe `tj`.
#
# DEUX sets dans ce pack :
#   - `Jennika`          (tj001a-tj012, dossier jennika/jennika/)
#   - `Jennika Nemesis`  (tj013-tj015, dossier jennika/jennika_nemesis/)
# 16 card_id : 2 faces d'identite, 9 cartes signature distinctes (15
# exemplaires dans le deck), tj011 Sosaiken (la Voie, Permanent, MISE DE COTE),
# 1 obligation, 3 cartes nemesis distinctes (5 exemplaires, Street Phantoms x3).
#
# ⚠ `FileManager.CleanName` rend `jennika` et `jennika_nemesis` : ce sont bien
# les noms des deux dossiers de modules.
#
# ---------------------------------------------------------------------------
# LES MECANIQUES DU PACK
#   tj001a Ninja Senpai    -> +1 CTR/ATQ/DEF quand on joue une carte SHINOBI
#                             (une fois par round POUR CHAQUE Shinobi)
#   tj001b Jenny           -> Setup : la Voie (tj011) en jeu ; Action : 2 Tekko-Kagi
#   tj009 / tj010          -> « each TEKKO-KAGI upgrade you control gains »
#                             (GiveKeywordToInPlayWhenApplyThis, modele tl011)
#   tj011 Sosaiken         -> Permanent, mise de cote (modele 58002 Ionic Physiology)
#
# LES CARTES SHINOBI. « This card is both a Jennika card and a Kuji-Kiri card » :
# la classe Shinobi est portee par `desc.Class` (« Hero;Kuji-Kiri »), comme
# « Campaign;Aggression ». Quatre classes, ajoutees a `ClassCard.CARD_CLASS`
# (fichier moteur partage `card_player.py`, additif) : Bushido, Ninjutsu,
# Kuji-Kiri, Taijutsu. Une carte SHINOBI = une carte portant l'une d'elles :
# tj003 (Kuji-Kiri), tj004 (Taijutsu), tj005 (Ninjutsu), tj006 (Bushido).
# Composure, Jenny's Crib, Bow, Tekko-Kagi n'impriment AUCUNE classe Shinobi :
# ce ne sont PAS des cartes Shinobi (voir .planning/tmnt/jennika-questions.md Q2).
#
# ⚠ BASES AUTOMATIQUES, AUCUN SCRIPT POUR ELLES (desc) : `Retaliate`,
# `Toughness` (tj014, tj015), `Restricted` (tj008), `Permanent` (tj011),
# `Uses` (tj006), `Hinder` / `Incite` / `Hazard` / `StartingThreat` / `Boost`
# (tj013). Les recoder ferait doubler leur effet.
#
# ⚠ Traits NEUFS : TEKKO-KAGI, BOW, OATH, PHANTOMS, SENPAI (TACTIC, SPELL, THWART,
# SKILL, ATTACK, WEAPON, NINJA, TURTLE, LOCATION, NYC, SKYLINE existent deja).
# Le champ `traits` n'est lu a l'execution que par Teamwork : rien a declarer.
#
# ⚠ NOMS DE CARTES UNIQUES : `CardFinder(name=...)` s'ecrit SANS l'etoile.
# ===========================================================================
