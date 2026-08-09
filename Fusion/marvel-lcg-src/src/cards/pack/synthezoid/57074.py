from . import *
def GetAbilities() -> Sequence['Ability']:
    def calculated_risk(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        Unused(initiator)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, calculated_risk).SetPlay().SetLabel()]
