from . import *

# Flight of Flyborgs — SBIRE nemesis (5/5). AERIAL. FLYBORGS. SWARM.
#   SCH / ATK / PV = ★, boost 3.
# Enters play with 4 swarm counters on them.
# [star] This minion's SCH, ATK, and hit points are equal to the number of
#   swarm counters here.
# Forced Interrupt: When this minion takes any amount of damage, remove that
#   number of swarm counters from here instead.
#
# JUMEAU de td016 (Plague of M.O.U.S.E.R.s) : 4 compteurs au lieu de 2, boost
# 3 au lieu de 1, traits AERIAL. FLYBORGS. SWARM. Cartes de reference, mots-pieges
# et PV dynamiques : voir `td016.py` et `CapacitesEssaim` (`__init__.py`).
#
# TEXTE CONTRE CODE
#  « 4 swarm counters » (td016 : 2). « remove THAT NUMBER of swarm counters » est
#  la meme lecture que « that many » de td016 : le texte imprime ne differe que
#  par ces mots, aucune difference de regle.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesEssaim(4)
