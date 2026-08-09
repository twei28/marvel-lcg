from . import *
def GetAbilities() -> Sequence['Ability']:
    def move_in_shadow(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        def action(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 1, effect)
        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', action).SetTarget(Scheme2, has_threat=True))
    return [DiscountAbility(1, ['MARTIAL ARTIST', 'SPY']),
            AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'You', None, move_in_shadow)]
