from . import *
def GetAbilities() -> Sequence['Ability']:
    def spellcasting(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> None:
        this = effect.this.CastTo(Obligation)
        message.CancelEffects(effect, discard_it=True)
        Faces.DiscardAll([this], effect)
    def check_gave_to(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> bool:
        this = effect.this.CastTo(Obligation)
        return (message.to_player == this.GetGaveToPlayer())
    return [AbilityFactory.WhenPlayerWouldPlayCard(AbilityType.ForcedInterrupt, 'AnyPlayer', None, spellcasting, conditions=[check_gave_to, lambda effect, message: (not message.be_cancel)])]
