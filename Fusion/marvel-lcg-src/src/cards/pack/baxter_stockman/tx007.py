from . import *

# Plague of M.O.U.S.E.R.S. — SBIRE (Baxter's Lab 8/22, x4). MOUSERS. SWARM. 1 boost.
# Enters play with 2 swarm counters on them.
# [star] This minion's SCH, ATK, and hit points are equal to the number of swarm counters here.
# Forced Interrupt: When this minion takes any amount of damage, remove that many swarm counters from
#   here instead.
#
# Carte de reference : `td016` Plague of M.O.U.S.E.R.s (pack donatello), MEME TEXTE au mot pres ;
# on reutilise `CapacitesEssaim` (donatello_nemesis/__init__.py), fiche mots-cles/swarm.md (PV dynamiques,
# aucune mort donnee a la main, degats remplaces par un retrait de compteurs).
#
# Mots-pieges : « SCH, ATK AND HIT POINTS » (les trois suivent le compteur) ; « that MANY » (autant
# de compteurs que de degats) ; « INSTEAD » (les degats n'ont pas lieu ; aucun exces ne passe).


def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesEssaim(2)]
