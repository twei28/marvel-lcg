from . import *
def GetAbilities() -> Sequence['Ability']:
    return [DiscountAbility(1, ['ATTORNEY', 'POLICE']),
            AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Minion)),
            *AbilityFactory.GiveKeywordToAttached(Minion, scheme=-2)]
