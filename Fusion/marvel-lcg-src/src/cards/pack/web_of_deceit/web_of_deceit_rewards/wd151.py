from . import *

# * Unity
#
# Le bout de l'arbre Symbiosis : le heros et le symbiote ne font plus qu'un, et
# tout monte d'un cran sans contrepartie. Les paliers precedents, eux, se
# payaient tous en menace ou en douleur.

def GetAbilities() -> Sequence['Ability']:

    return [
        # « You get +1 to each of your basic powers and +1 hand size. »
        *AbilityFactory.GiveKeywordToAttached(
            attack=1,
            thwart=1,
            defense=1,
            recover=1,
            hand_size=1,
        ),
    ]
