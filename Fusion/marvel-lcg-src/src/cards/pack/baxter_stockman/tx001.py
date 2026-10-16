from . import *

# * Baxter Stockman (I) — VILAIN, stade 1 (Baxter's Lab 1/22). AERIAL. FLY. GENIUS.
# PV 13[per_hero], SCH 1, ATK 0. Toughness.
# Forced Interrupt: When the villain phase begins, each player resolves the "Special" on the
# Baxter's Laboratory scheme.
#
# Cartes de reference : `WhenVillainPhaseBegin(ForcedInterrupt, ...)` (modele 60199 Tombstone pour
# le declencheur de debut de phase) ; le Special : `ResolveSpecialAbility` (zeus `ResoudreLeSpecialDe`).
# Toughness est natif (`desc.Toughness`).
#
# Mots-pieges : « EACH player » (tous les joueurs, premier joueur d'abord, UN Special chacun) ;
# « resolves » (c'est le JOUEUR qui resout : « engaged with YOU » vise ce joueur) ; « When the villain
# phase BEGINS » : interruption forcee de DEBUT de phase, pas de fin.


def GetAbilities() -> Sequence['Ability']:
    return [AuDebutDeLaPhaseDuMechant()]
