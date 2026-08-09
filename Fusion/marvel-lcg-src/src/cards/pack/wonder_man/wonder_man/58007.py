from . import *
def GetAbilities() -> Sequence['Ability']:
    def wonder_fans(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        def tuck(targets: Sequence['CardFace']):
            TuckEnergyEventFromDiscard(effect, initiator)
        def draw(targets: Sequence['CardFace']):
            initiator.DrawUp(1, effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Tuck 1 event with a printed [energy] resource under Ionic Physiology', tuck),
            AbilityFactory.ForChoiceAbility('Draw 1 card', draw))
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, wonder_fans).SetCostFunc(CostFunc.Exhaust('This'))]
