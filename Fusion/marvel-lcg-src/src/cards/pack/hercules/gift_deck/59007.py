from . import *
def GetAbilities() -> Sequence['Ability']:
    def draw_4(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        this.GetControlByPlayer().DrawUp(4, effect)
    return [*AbilityFactory.GiveKeywordToAttached(CardFinder(name='Hercules', card_type=Hero), health=1),
            AbilityFactory.UnitAttackGainKeyword(CardFinder(name='Hercules', card_type=Hero), piercing=True, is_basic_attack=True),
            AbilityFactory.AfterCardEnterPlay(AbilityType.Response, 'This', draw_4)]
