from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('G'), for_card=CardFinder(card_type=Event), is_play_card=True).SetCostFunc(CostFunc.Exhaust('This')).AnyPlayerCanDoThis()]
