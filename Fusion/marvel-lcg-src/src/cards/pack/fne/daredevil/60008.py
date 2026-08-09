from . import *
def GetAbilities() -> Sequence['Ability']:
    def cross_examination(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        for target in effect.targets:
            damage = 3 + len(target.GetAttachedUpgrades())
            this.DealDamage([target], damage, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, cross_examination).SetPlay().SetLabel('attack').SetTarget(Enemy)]
