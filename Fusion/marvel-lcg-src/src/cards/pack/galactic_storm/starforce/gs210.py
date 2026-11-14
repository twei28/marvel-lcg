from . import *

# * Doctor Minerva — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 2, ATK 1, 8 PV, 3 icones de boost.
# Villainous. Victory 1.
# While Doctor Minerva is in the victory display, the villain gets +1 SCH.
#
# Cartes de reference : **`next_evol/40006`** (`works_in_the_victory_display=True`, ici `scheme=1`) ;
# Villainous / Victory : bases AUTOMATIQUES.
#
# ⚠ Mots-pieges : « +1 SCH » (pas ATK) ; « WHILE ... in the victory display ».


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(scheme=1)
