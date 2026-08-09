from . import *
def GetAbilities() -> Sequence['Ability']:
    def compound(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        initiator = effect.GetInitiator()
        tucked = list(this.GetPlacedCardArea().Get())
        if tucked:
            initiator.PlayCardsLikeInTurn(tucked[:1], effect, forced=False, if_not_play_discard_it=False)
            return
        faces = [f for f in initiator.hand_cards.Get() if Ally.IsType(f)]
        if not faces:
            return
        def action(targets: Sequence['CardFace']):
            for face in targets:
                this.TuckCardUnderHere(face, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Tuck 1 ally from your hand here', action).SetTarget(faces, range=(1, 1)))
    return [AbilityFactory.CanPlayThisSupportCard().SetPlay(only_if_your_identity_has_trait='AVENGER'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, compound).SetCostFunc(CostFunc.Exhaust('This'))]
