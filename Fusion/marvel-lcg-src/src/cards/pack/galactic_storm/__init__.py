from cards.pack import *

# ===========================================================================
# Pack GALACTIC STORM — contenu custom de « Kajislav ». Set 144, prefixe `gs`.
# Coffret complet : campagne de 5 scenarios, 2 heros (Binary, Quasar), 5 sets
# modulaires, cartes de campagne. Inventaire, transcriptions et regles :
# docs/packs/galactic-storm/ ; decisions : .planning/todos/2026-10-20-gs0-questions.md.
#
# card_id = `gs` + numero IMPRIME sur 3 chiffres (+ a/b), sauf exceptions
# decidees le 20/10/2026 (Q1) : le heros Quasar porte « 4 » sur ses 17 cartes,
# il est numerote d'apres le pied « QUASAR (n/16) » + 300 (gs301-gs316,
# Quantum Bubble gs349, identite gs300a/gs300b) ; les nemesis de Quasar en
# collision avec Binary portent le suffixe `q`.
#
# Sets de ce dossier (FileManager.CleanName) :
#   - `Quasar`         -> quasar/
#   - `Quasar Nemesis` -> quasar_nemesis/
# ===========================================================================

# ⚠ Les helpers partages vivent dans le `__init__.py` DU SET, pas ici (les
# modules font `from . import *`, voir armored_spidey/__init__.py).
