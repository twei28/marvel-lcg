from . import *
def GetAbilities() -> Sequence['Ability']:
    def ferocious_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 6, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, ferocious_attack).SetLabel('attack').SetCost(Cost('3')).SetTarget(Enemy)]
