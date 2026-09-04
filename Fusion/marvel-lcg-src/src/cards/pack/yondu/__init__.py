from cards.pack import *

# ===========================================================================
# Pack YONDU — contenu custom de « BLUEHG + DESIGNHACKER », format
# « MC4 SEALED ». Set 154, prefixe `yd`.
#
# DEUX sets dans ce pack :
#   - `Yondu`         (yd001a-yd013, dossier yondu/yondu/)
#   - `Yondu Nemesis` (yd014-yd018, dossier yondu/yondu_nemesis/)
# 19 card_id : 2 faces d'identite, 11 cartes signature distinctes
# (15 exemplaires), 1 obligation, 5 cartes nemesis.
#
# ⚠ `FileManager.CleanName` rend `yondu` et `yondu_nemesis` : ce sont bien les
# noms des deux dossiers de modules (leçon bt019 — et leçon nt012, payee une
# seconde fois la veille sur le pack night_thrasher, ou l'OBLIGATION avait ete
# rangee dans le dossier nemesis alors que son `set_name` est celui du HEROS).
# ⚠ ICI L'OBLIGATION `yd013` Banished PORTE `set_name = "Yondu"` : son module
# vit donc dans `yondu/`, PAS dans `yondu_nemesis/`.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : UNE FLECHE QUI SE PLANTE, ET NEUF CARTES QUI LA BOUGENT
#
# `yd012` Yaka Arrow est une amelioration qui ne vit PAS sur son porteur
# habituel : elle s'attache a un ENNEMI, a l'IDENTITE, ou revient en MAIN.
# Le pouvoir du heros (`yd001a` D'ast Whistlin') transforme chaque
# DEPLACEMENT en effet :
#
#   arrive sur un ennemi   1 degat a cet ennemi
#   quitte un ennemi       1 degat a cet ennemi
#   arrive sur l'identite  1 soin sur Yondu
#
# La fleche fait donc mal DEUX FOIS par aller-retour, et le deck ne fait que
# la deplacer : `yd004` Whistle While You Work, `yd006` Twirlin' and Whirlin',
# `yd009` Invest et `yd011` Tahlei la posent ou la reprennent ; `yd002` Cheap
# Shot et `yd003` Fight Dirty frappent a 6 l'ennemi qui la porte ; `yd008`
# Ravager Redshirts previent les degats de cet ennemi ; `yd010` Ravage pose un
# compteur `wound` quand elle atterrit sur un sbire ; `yd005` Tough
# Motherlover recompense de l'avoir EN MAIN.
#
# ---------------------------------------------------------------------------
# ⚠ MOT-CLE MAISON `summon`, employe SIX fois et JAMAIS defini par l'auteur.
# Definition ARBITREE par l'utilisateur le 03/09/2026 : « summon X » =
# fouiller le DECK **ET** la DEFAUSSE pour la carte nommee, la prendre, puis
# remelanger. Fiche complete, montage et pieges :
# `docs/reference/mots-cles/summon.md`.
# Sans la defausse, une Yaka Arrow defaussee (l'obligation `yd013` le fait
# explicitement) serait perdue pour la partie et neuf cartes du pack
# deviendraient mortes.
#
# ⚠ COMPTEUR MAISON `wound`, ajoute a l'enum `COUNTER`
# (src/game/card/face/card_face.py) pour `yd010` Ravage. Sans lui,
# `IsCounter` refuse le nom et la carte tombe des la creation de la partie.
#
# ---------------------------------------------------------------------------
# ⚠ ASPECT AGRESSIVITE, DONNE PAR L'AUTEUR. Le zip contient sa decklist
# (scan « Yondu Starter Deck ») : 15 cartes signature, 18 cartes
# d'Agressivite, 7 cartes Basic. Aucune question d'aspect n'a ete posee,
# contrairement a lady_sif, iron_man_model_42 ou night_thrasher.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES, verifies dans data/cards.json le 03/09/2026 :
#  - « * Yondu » : `17013`, ALLIE officiel de Star-Lord. Notre face heros
#    porte le meme nom, c'est le set_name qui differe — et l'allie est de
#    classe Hero du set Star-Lord, donc jamais dans ce deck.
#  - « Jackpot! » : `40043`, ressource du pack Domino.
#  - « Cheap Shot » : `dt027`, evenement du pack determination.
#  - Les autres noms du pack ont ete verifies LIBRES.
# ===========================================================================

# ⚠ Les helpers partages du set vivent dans le `__init__.py` DU SET, pas ici :
# les modules font `from . import *`, qui importe le `__init__` du dossier du
# set. Un helper defini ici leve un NameError avale par le moteur (paye sur
# hk005 le 02/09/2026).
