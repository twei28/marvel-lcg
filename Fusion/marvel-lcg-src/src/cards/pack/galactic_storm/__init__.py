from cards.pack import *

# ===========================================================================
# Pack GALACTIC STORM — contenu custom de « Kajislav ». Set 144, prefixe `gs`.
# Coffret complet : campagne de 5 scenarios, 2 heros (Binary, Quasar), sets
# modulaires, cartes de campagne. Inventaire, transcriptions et regles :
# docs/packs/galactic-storm/ ; decisions de l'utilisateur du 20/10/2026 :
# card_id = `gs` + numero IMPRIME sur 3 chiffres (+ a/b), UN card_id par
# numero imprime (les copies sont des exemplaires du paquet).
#
# Sets de ce dossier (FileManager.CleanName) :
#   - `Majestrix's Verdict` -> majestrixs_verdict/ (scenario 2, lot GS-5)
# ===========================================================================

# ⚠ Les helpers partages vivent dans le `__init__.py` DU SET, pas ici (les
# modules font `from . import *`, voir skrull_menace/paibok/__init__.py).
