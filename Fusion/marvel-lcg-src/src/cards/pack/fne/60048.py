from . import *
def GetAbilities() -> Sequence['Ability']:
    def army_of_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.ReadyAll(effect.targets, effect)
    def increase_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = len(player.allies.Get())
        if (value > 0):
            message.UpdateCost(value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, army_of_one).SetPlay().SetLabel().SetTarget('YourHero'),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeywordStar, increase_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
