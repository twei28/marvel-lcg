from . import *

# * Dracula — SBIRE nemesis (N 2/8). ELITE. VAMPIRE. 12 PV, SCH 3, ATQ 3, 3 boost.
# Attacks with piercing deal double damage to Dracula.
# [star] Forced Response: After Dracula attacks and damages a character, heal all
#   damage from Dracula. If you cannot, give him a tough status card.
# (Blade's nemesis minion.)
#
# CARTES DE REFERENCE
#  - `39051` Vampire (Mojo, set Horror) : le texte est le MEME mot pour mot, a
#    « If you cannot » pres (= rien a soigner). `CapacitesDeVampire()` dans
#    le __init__ du set.
#
# TEXTE CONTRE CODE
#  ⚠ « If you CANNOT » heal -> aucun degat a soigner (`soin.value` nul) ->
#    Tenace. Meme lecture que « If no damage was healed this way » (Vampire).
#  ⚠ Le Setup d'Eric Brooks (bl001b) LAISSE Dracula dans la pile nemesis :
#    c'est la seule carte que Shadow of the Past trouvera encore.
#  ⚠ Elite : lu dans les traits, rien a coder.


def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDeVampire(),
    ]
