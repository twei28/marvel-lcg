from . import *
def GetAbilities() -> Sequence['Ability']:
    def cloak(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, include_discard_pile=True, include_player_hand_cards=True, name='Dagger')
        if face:
            face.CastTo(Ally).PutIntoPlay(initiator, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, cloak).SetCostFunc(CostFunc.Exhaust('This')).SetCostFunc(CostFunc.Spend(Cost('YY')))]
