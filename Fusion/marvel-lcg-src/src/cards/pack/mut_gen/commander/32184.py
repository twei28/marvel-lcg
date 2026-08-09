from . import *
def GetAbilities() -> Sequence['Ability']:
    def shock_and_awe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 6, effect)
        Faces.ReadyAll(list(initiator.allies.Get()), effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, shock_and_awe).SetLabel('attack').SetCost(Cost('3')).SetTarget(Enemy)]
