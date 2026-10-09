from . import *

# hs112 * Kraven's Spear
# Attache a Kraven. ATK+1 (donnees). Kraven gagne retaliate 1.
# Interrupt : quand vous attaquez Kraven, 3 degats a votre identite → defaussez cet attachement.

def GetAbilities() -> Sequence['Ability']:
    return [
        AttacherALaRevelation(),
        *AbilityFactory.GiveKeywordToAttached(retaliate=1),
        InterruptContrePorteur(None, CostFunc.TakeDamage(3, "YourIdentity")),
    ]
