from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.AttachToFaceWhenPutIntoPlayInternal(CardFinder(name='Magneto', card_type=Villain))]
