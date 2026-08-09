from . import *
def GetAbilities() -> Sequence['Ability']:
    def mighty_avengers(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DealAdditionalDamage(1, effect)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.NonKeyword, CardFinder(card_type=Leader), mighty_avengers)]
