from . import *

# * Cadmi-M the Pursuer — SBIRE (Starforce). ELITE. KREE. STARFORCE. SCH 1, ATK 1, 8 PV, 3 icones de boost.
# Retaliate 1. Villainous. Victory 1.
# While Cadmi-M the Pursuer is in the victory display, the villain gains retaliate 1.
#
# Cartes de reference : **`next_evol/40006`** Technovirus Purge (`GiveKeywordToInPlayWhenApplyThis(...,
# works_in_the_victory_display=True, ...)`, RECETTES §3bis) ; Retaliate / Villainous / Victory : bases
# AUTOMATIQUES (`desc`), fiches retaliate.md, villainous.md, victory.md.
#
# ⚠ Mots-pieges : « WHILE ... in the victory display » (seulement la, pas en jeu ni en defausse ; le bonus
# tombe si Supremor Seed l'en retire) ; « the VILLAIN gains retaliate 1 » (s'ajoute : Korath en vitrine aussi
# = retaliate 2).


def GetAbilities() -> Sequence['Ability']:
    return BonusDeStatEnVitrine(retaliate=1)
