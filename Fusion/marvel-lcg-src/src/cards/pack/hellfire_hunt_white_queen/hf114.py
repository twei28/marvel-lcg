from . import *

# Phantom Warrior (une des quatre illustrations). Sbire ILLUSION, Guard + Steady + Toughness (desc). « [star] Boost : Put Phantom Warrior into play
# engaged with you. » Carte de reference EXACTE : 01121 Weapons Runner (`WhenCardBecomeBoost("This", PutThisIntoPlay)`).


def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.WhenCardBecomeBoost("This", PutThisIntoPlay)]
