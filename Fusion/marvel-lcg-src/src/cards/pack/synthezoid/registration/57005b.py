from . import *
def GetAbilities() -> Sequence['Ability']:
    def hinder_value(effect: 'Effect', ui: List['CardFace']) -> int:
        num = len(effect.world.players)
        if (num <= 1):
            return 0
        return (2 * num)
    return [AbilityFactory.ThisGainKeyword(hinder_value, hinder=1),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(card_type=Leader), steady=1)]
