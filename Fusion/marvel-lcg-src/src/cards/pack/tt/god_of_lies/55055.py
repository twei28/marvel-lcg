from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.CanGenerateResources(AbilityType.Resource, Resources('GG')).SetCostFunc(CostFunc.Counter('This', 1, 'synergy')).AnyPlayerCanDoThis(),
            AbilityFactory.DoGenerateResources(AbilityType.Resource, 'This')]
