from . import *

# * Protector — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 1, 8 PV, 3 icones de boost.
# Steady. Villainous. Victory 1.
# While Protector is in the victory display, the villain gains steady.
#
# Cartes de reference : **`next_evol/40006`** (`works_in_the_victory_display=True`, ici `steady=1`) ;
# Steady / Villainous / Victory : bases AUTOMATIQUES (fiche steady.md).
#
# ⚠ Mots-pieges : « gains STEADY » (une carte Sonne et une Desoriente de plus avant d'etre affecte).


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(steady=1)
