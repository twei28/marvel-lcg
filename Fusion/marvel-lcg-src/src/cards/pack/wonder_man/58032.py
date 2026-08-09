from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=EncounterCard))]
