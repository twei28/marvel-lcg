from . import *
def GetAbilities() -> Sequence['Ability']:
    def in_harms_way(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        value = initiator.GetHero().defense
        if (value <= 0):
            return
        this.DealDamage(effect.targets, value, effect)
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, value, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove X threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True))
    def increase_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = len(player.allies.Get())
        if (value > 0):
            message.UpdateCost(value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, in_harms_way).SetPlay().SetLabel('attack', 'thwart').SetTarget(Enemy),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeywordStar, increase_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
