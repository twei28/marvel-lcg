from . import *
def GetAbilities() -> Sequence['Ability']:
    return [*AbilityFactory.GiveKeywordToAttached(CardFinder(trait=AVATAR_TRAIT, card_type=Villain), health='3*', steady=1)]
