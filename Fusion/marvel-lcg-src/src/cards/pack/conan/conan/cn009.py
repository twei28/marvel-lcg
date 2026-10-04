from . import *

# * The Scarlet Citadel — manigance annexe joueur (13/16). Cout 0 [physical],
# menace de depart 5. Victory 0.
# While The Scarlet Citadel is in the victory display, if you have the:
#   • THIEF trait, you get +1 THW and ignore the patrol keyword.
#   • BARBARIAN trait you get +1 ATK and ignore the guard keyword.
#   • KING trait, all of the above.
#
# Aucune capacite ici : une carte en vitrine n'enregistre rien (recette §3bis,
# lecon rs009). Les bonus vivent sur les faces heros de l'identite
# (`CapacitesCitadelle`, conan/__init__.py, appelee par cn001a/c/d). La mise
# en jeu, la menace de depart et le passage en vitrine (Victory 0) sont lus
# dans `desc`.


def GetAbilities() -> Sequence['Ability']:
    return []
