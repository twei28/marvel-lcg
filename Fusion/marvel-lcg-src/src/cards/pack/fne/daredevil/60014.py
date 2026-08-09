from . import *
def GetAbilities() -> Sequence['Ability']:
    def karen_page(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)
        if initiator.IsAlterEgo():
            initiator.DrawUp(1, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, karen_page).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(finder=CardFinder(set_name='Daredevil'), from_where=['YourDiscardPile'], range=(1, 1))]
