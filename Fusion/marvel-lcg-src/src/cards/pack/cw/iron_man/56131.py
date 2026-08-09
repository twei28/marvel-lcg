from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(name='Iron Man', card_type=Leader)),
            AbilityFactory.ThisGainKeyword(lambda effect, ui: 1, consider_as=('TECH', Attachment)),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCost(Cost('YB')).AnyPlayerCanDoThis()]
