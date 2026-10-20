from cards.pack import *

# ===========================================================================
# Pack GALACTIC STORM — contenu custom de « Kajislav ». Set 144, prefixe `gs`.
# Coffret complet : campagne de 5 scenarios, 2 heros (Binary, Quasar), sets
# modulaires, cartes de campagne. Inventaire, transcriptions, regles et
# questions : docs/packs/galactic-storm/ et .planning/todos/2026-10-20-gs*.
#
# card_id = `gs` + numero IMPRIME sur la carte (3 chiffres, + a/b pour les
# faces), decision de l'utilisateur du 20/10/2026, avec ses exceptions :
#  - Quasar : numero « n/16 » du pied de carte decale de 300 (lot GS-2) ;
#  - nemesis en collision (237, 239, 240) : identifiant simple pour BINARY,
#    suffixe `q` pour QUASAR ;
#  - Forgotten Life (Binary) imprime « 4 » comme Pursued by the Flame : elle
#    prend `gs031`, son rang dans la liste du deck de depart imprimee
#    (question Q1 de .planning/todos/2026-10-20-gs1-questions.md).
#
# Sets de ce dossier (FileManager.CleanName) :
#   - `Binary`         -> binary/
#   - `Binary Nemesis` -> binary_nemesis/
#   - `Quasar`         -> quasar/
#   - `Quasar Nemesis` -> quasar_nemesis/
#   - `Majestrix's Verdict` -> majestrixs_verdict/ (scenario 2, lot GS-5)
# ===========================================================================

# ⚠ Les helpers partages vivent dans le `__init__.py` DU SET, pas ici (les
# modules font `from . import *`, voir skrull_menace/__init__.py).
