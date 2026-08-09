from . import *
def GetAbilities() -> Sequence['Ability']:
    def gift_resources(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this
        player = this.GetControlByPlayer()
        value = CountGifts(effect, player)
        if (value <= 0):
            return None
        return Resources('G' * value)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.CanGenerateResources(AbilityType.Resource, resources_fn=gift_resources).SetCostFunc(CostFunc.Exhaust('This'))]
