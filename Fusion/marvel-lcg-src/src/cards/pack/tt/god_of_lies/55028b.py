from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove)]
