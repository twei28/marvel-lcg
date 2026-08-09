from . import *
def GetAbilities() -> Sequence['Ability']:
    def gift_of_battle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 5, effect)
    def reduce_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = CountGifts(effect, player)
        if (value > 0):
            message.UpdateCost(-value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, gift_of_battle).SetPlay().SetLabel('attack').SetTarget(Enemy),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeyword, reduce_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
