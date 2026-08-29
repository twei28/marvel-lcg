from cards.pack import *
# CORRECTIF (trouve par test_capacites.py) : les cartes du nemesis set ont
# leur PROPRE `from . import *` (ce fichier), distinct de celui du pack
# heros (iron_lad/iron_lad/__init__.py) -- NameError sans cet import
# explicite des aides partagees (UpgradesIronLadEnJeu, NOM_KANG, ...).
from cards.pack.iron_lad.iron_lad import UpgradesIronLadEnJeu, NOM_KANG, NOM_STATURE, StatureEnJeu

# ===========================================================================
# Set nemesis d'IRON LAD — contenu custom de CptScorp.
#
# 5 cartes physiques (numerotees 1/5 a 5/5 sur les scans) : Early Start
# (il018, side scheme), Kang the Conqueror (il019, sbire nemesis, Toughness +
# Villainous), Taking Responsability (il020, obligation), et 2 exemplaires
# physiques de la meme trahison "Pay the Price" (il021, il022) -- meme choix
# de design que okoye_nemesis (ok023/ok024, "War Drumming" x2).
# ===========================================================================
