from . import *
def GetAbilities() -> Sequence['Ability']:
    def i_object(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        message.PreventThreat(3, effect)
    return [AbilityFactory.WhenSchemeWouldPlaceThreat(AbilityType.Interrupt, MainScheme, i_object).SetPlay().SetLabel()]
