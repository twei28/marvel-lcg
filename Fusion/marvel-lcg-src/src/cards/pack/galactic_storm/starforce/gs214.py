from . import *

# * Ronan the Accuser — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 2, 8 PV, 3 icones de boost.
# Villainous. Victory 1.
# While Ronan the Accuser is in the victory display, the villain gets +1 ATK.
#
# Cartes de reference : **`gs211`** Inndig-O (texte identique) ; **`next_evol/40006`**.
#
# ⚠ Mots-pieges : identiques a gs211. (La citation imprime « highes » : coquille de l'auteur, sans effet.)


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(attack=1)
