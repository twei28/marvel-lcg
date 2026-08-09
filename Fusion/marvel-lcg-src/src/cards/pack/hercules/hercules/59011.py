from . import *
def GetAbilities() -> Sequence['Ability']:
    def wisdom_of_athena(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
    def reduce_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = CountGifts(effect, player)
        if (value > 0):
            message.UpdateCost(-value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, wisdom_of_athena).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeyword, reduce_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
