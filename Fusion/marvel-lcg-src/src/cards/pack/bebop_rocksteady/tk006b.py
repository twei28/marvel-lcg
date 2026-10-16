from . import *

# Gone Berserk! (face FERAL de Destructive Dunderheads)
# Permanent (desc). « Attach to the villain » : fait par tk006a, qui retourne la carte
# puis l'accroche au vilain restant. Crisis / Amplify / Hazard : lus dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitCannotBeConfused(CardFinder(card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached(
            Villain,
            health=lambda effect: 12 * Worlds.GetPlayerNum(effect)),
    ]
