from . import *

# Flight of Flyborgs — SBIRE (Cyber Swarm 1/6, x3). AERIAL. FLYBORG. SWARM. 2 boosts.
# Enters play with 4 swarm counters here.
# [star] This minion's SCH, ATK, and hit points are equal to the number of swarm counters here.
# Forced Interrupt: When this minion takes any amount of damage, remove that many swarm counters from
#   here instead.
#
# Carte de reference : `td017` Flight of Flyborgs (pack donatello) et `tx007` : meme montage, 4 compteurs.
# ⚠ Le trait imprime ici est FLYBORG (singulier), celui de td017 est FLYBORGS : `td014` Extermination!
# cherche « MOUSERS or FLYBORGS » et ne trouvera pas ce sbire (voir baxter-questions.md, Q4).


def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesEssaim(4)]
