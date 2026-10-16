from . import *

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Rocksteady", card_type=Villain)),
    ]
