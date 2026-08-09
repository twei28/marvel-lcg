from . import *
def GetAbilities() -> Sequence['Ability']:
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_thunderbolt(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return (Worlds.FindCardOnField(effect, trait='THUNDERBOLT', card_type=Minion) != None)
    return [AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_thunderbolt])]
