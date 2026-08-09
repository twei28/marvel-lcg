from . import *
from cards.pack.aoa.missions import DoMissionAttempt, GetMissionScheme, GetMissionAllies, AllyToMission
def GetAbilities() -> Sequence['Ability']:
    def reduce_cost(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        Worlds.UpdateNextCardPlayCost(initiator, -2, effect, finder=CardFinder(card_type=Ally), in_this='Phase')
    def attempt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        DoMissionAttempt(effect, effect.GetInitiator())
    def check_can_attempt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        if (GetMissionScheme(effect) == None):
            return False
        return (len(GetMissionAllies(effect)) > 0)
    def send_to_mission(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this
        Unused(this)
        ally = message.played_face
        if ally and ally.IsInPlay():
            if (ally.GetCounters('mission') == 0):
                AllyToMission(effect, ally)
    def check_ally_played(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        if (GetMissionScheme(effect) == None):
            return False
        face = message.played_face
        if not Ally.IsType(face):
            return False
        return face.IsInPlay()
    return [AbilityFactory.FirstPlayerControlThis(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, reduce_cost).SetCostFunc(CostFunc.Exhaust('This')).SetName('Reduce the cost of the next ally by 2'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, attempt, conditions=[check_can_attempt]).SetCostFunc(CostFunc.Exhaust('This')).SetName('Make a mission attempt'),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'AnyPlayer', None, send_to_mission, conditions=[check_ally_played]).SetName('Send this ally to the mission')]
