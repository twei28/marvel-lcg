from . import *
def GetAbilities() -> Sequence['Ability']:
    def sister_maggie(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(targets, effect)
        status_cards = list(identity.components.status.GetDeck().Get(True))
        if status_cards:
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a status card from your identity', action).SetTarget(status_cards))
    return [AbilityFactory.CanPlayThisSupportCard(),
            *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Matt Murdock'), recover=3),
            AbilityFactory.AfterUnitRecovery(AbilityType.Response, 'YourIdentity', sister_maggie)]
