from . import *

# * Korath the Pursuer — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 1, 8 PV, 3 icones de boost.
# Retaliate 1. Villainous. Victory 1.
# While Korath the Pursuer is in the victory display, the villain gains retaliate 1.
#
# Cartes de reference : **`gs209`** Cadmi-M (texte identique) ; **`next_evol/40006`**.
#
# ⚠ Mots-pieges : identiques a gs209.


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(retaliate=1)
