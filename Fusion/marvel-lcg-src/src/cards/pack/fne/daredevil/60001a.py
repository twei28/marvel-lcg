from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_sense_top(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (message.which_face == initiator.additional_deck.GetTop())
    return [*AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_sense_top]),
            # Rafraichissement du cache `is_like_in_hand` (voir
            # `RafraichirDessusDeckAnnexe`, __init__.py). `AbilityType.Rule`,
            # comme sur Echo (60037a.py) : c'est lui qui garde l'aptitude en
            # ecoute meme quand cette face HEROS part dans `aside_deck`.
            AbilityFactory.WhenCardWouldMoveToArea(
                AbilityType.Rule, CardFinder(card_ids=list(SENSE_DECK_IDS)),
                RafraichirDessusDeckAnnexe)]
