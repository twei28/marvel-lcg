from . import *

# * Inndig-O the Accuser — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 2, 8 PV, 3 icones de boost.
# Villainous. Victory 1.
# While Inndig-O the Accuser is in the victory display, the villain gets +1 ATK.
#
# Cartes de reference : **`next_evol/40006`** (`works_in_the_victory_display=True`, ici `attack=1`) ;
# Villainous / Victory : bases AUTOMATIQUES.
#
# ⚠ Mots-pieges : « +1 ATK » ; s'ajoute a Ronan the Accuser (+2 ATK si les deux sont en vitrine).


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(attack=1)
