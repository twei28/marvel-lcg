from . import *
def GetAbilities() -> Sequence['Ability']:
    def size_advantage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        hero = effect.GetInitiator().GetHero()
        for target in effect.targets:
            bigger = hero.HasTrait('GIANT') or hero.health > target.health
            this.AttackDamage([target], 6 if bigger else 3, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, size_advantage).SetPlay().SetLabel('attack').SetTarget(Enemy, range=(1, 1))]
