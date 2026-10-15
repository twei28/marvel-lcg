from cards.pack import *

# ===========================================================================
# Pack SKRULL MENACE — contenu custom de « Kajislav ». Set 143, prefixe `sk`.
# Coffret complet : campagne de 5 scenarios, 2 heros (Hulkling, Lyja), sets
# modulaires, cartes de campagne. Porte heros par heros puis scenario par
# scenario : plan et decisions dans .planning/skrull-menace/ (NOTES.md,
# HULKLING.md), textes des cartes dans .planning/skrull-menace/transcriptions/.
#
# card_id = `sk` + numero IMPRIME sur la carte (3 chiffres, + a/b pour les
# faces) : une seule numerotation pour tout le coffret, lisible contre les
# scans de l'auteur.
#
# Sets de ce dossier (FileManager.CleanName) :
#   - `Hulkling (Kajislav)`         -> hulkling_kajislav/
#   - `Hulkling (Kajislav) Nemesis` -> hulkling_kajislav_nemesis/
# ⚠ « (Kajislav) » dans le set_name : un Hulkling OFFICIEL existe (pack cw,
# 56029a, set « Hulkling »). Meme parade que `Spider-Woman (Kajislav)` ; un
# set partage ferait aussi perdre le credit auteur (`_auteurParSet`).
# ===========================================================================

# ⚠ Les helpers partages vivent dans le `__init__.py` DU SET, pas ici (les
# modules font `from . import *`, voir armored_spidey/__init__.py).
