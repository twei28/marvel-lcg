from . import *
def GetAbilities() -> Sequence['Ability']:
    def reduce_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(-1, effect)
    def check_event(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        check_effect = message.check_effect
        if not check_effect.ability.is_play:
            return False
        face = check_effect.this
        if not Event.IsType(face):
            return False
        return (face.CastTo(HasCost).printed_cost.val >= 3)
    return [AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeyword, reduce_cost, conditions=[check_event])]
