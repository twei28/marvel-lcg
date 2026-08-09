from . import *
def GetAbilities() -> Sequence['Ability']:
    def swordsman_defend(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Ally)
        being = message.being_message
        being.DeclareDefender(this.card.face.CastTo(Unit2), effect)
        Faces.ReadyAll([this], effect)
    def check_undefended(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        being = message.being_message
        if (being == None):
            return False
        return (being.defender == None)
    def check_against_you(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        this = effect.this.CastTo(Ally)
        being = message.being_message
        return (being.would_atk_message.property.against_player == this.GetControlByPlayer())
    return [AbilityFactory.UnitAttackGainKeyword('This', piercing=True),
            AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.HeroResponse, None, swordsman_defend, while_attack=True, conditions=[check_undefended, check_against_you]).SetTarget('This')]
