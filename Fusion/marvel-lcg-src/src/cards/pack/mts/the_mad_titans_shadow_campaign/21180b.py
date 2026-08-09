from . import *
def GetAbilities() -> Sequence['Ability']:
    def leaves_play(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        this = effect.this.CastTo(Ally)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.FirstPlayerControlThis(),
            *AbilityFactory.ThisNotCountAllyLimit(),
            AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, 'This', leaves_play)]
