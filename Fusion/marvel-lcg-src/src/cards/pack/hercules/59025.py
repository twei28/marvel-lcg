from . import *
def GetAbilities() -> Sequence['Ability']:
    def confuse_cost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        player = effect.GetInitiator()
        if not player:
            return False
        identity = player.GetIdentity()
        if identity.HasTrait('ETERNAL'):
            return True
        return identity.GainStatus('Confused', effect)
    return [AbilityFactory.CanPlayThisAllyCard().SetCostFunc(CostFunc.Custom(None, confuse_cost))]
