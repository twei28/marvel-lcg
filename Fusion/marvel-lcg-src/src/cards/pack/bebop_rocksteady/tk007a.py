from . import *

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bebop", card_type=Villain)),
    ]
