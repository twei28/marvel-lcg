from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_not_mission_attempt(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        this = effect.this
        if (message.trigger != this):
            return False
        by = message.by_effect
        if by and by.this and by.this.IsName('Mission Team'):
            return False
        return True
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, None, cannot_remove, conditions=[check_not_mission_attempt])]
