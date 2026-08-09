from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_sense_top(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (message.which_face == initiator.additional_deck.GetTop())
    return [*AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_sense_top])]
