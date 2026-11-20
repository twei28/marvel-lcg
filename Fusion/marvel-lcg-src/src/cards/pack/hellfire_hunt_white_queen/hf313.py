from . import *

# Hellfire Pawn (x4). Sbire HELLFIRE, Guard + Patrol + Surge (desc). « [star] Boost : Put Hellfire Pawn into play engaged with you. »
# Carte de reference EXACTE : 01121 Weapons Runner.


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.WhenCardBecomeBoost("This", PutThisIntoPlay)]
