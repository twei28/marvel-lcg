from . import *
def GetAbilities() -> Sequence['Ability']:
    def foggy_nelson(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, foggy_nelson).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(Scheme2, has_threat=True)]
