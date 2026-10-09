from . import *

# hs125 Ferocious Lion
# [star] +1 ATK si l'attaque n'est pas defendue.
# Forced Response : apres qu'un personnage du joueur engage attaque Kraven, le Lion attaque ce joueur.

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.UnitGetATKWhileAttacking(AbilityType.NonKeywordStar, "This", None, 1, is_undefended_attack=True),
        ReponseDeMeute(),
    ]
