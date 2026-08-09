from . import *
def GetAbilities() -> Sequence['Ability']:
    def know_your_enemy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        for _ in range(2):
            schemes = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2) if (s.threat > 0)]
            if not schemes:
                return
            def action(targets: Sequence['CardFace']):
                this.RemoveThreatFromSchemes(list(targets), 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', action).SetTarget(schemes, range=(1, 1), not_move=True))
    return [DiscountAbility(1, ['MARTIAL ARTIST']),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, know_your_enemy).SetPlay().SetLabel('thwart')]
