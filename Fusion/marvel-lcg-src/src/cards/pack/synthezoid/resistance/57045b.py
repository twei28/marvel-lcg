from . import *
def GetAbilities() -> Sequence['Ability']:
    def enter_exhausted(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        ally = message.trigger
        Faces.ExhaustAll([ally], effect)
    return [AbilityFactory.WhenCardEnterPlay(AbilityType.NonKeyword, Ally, enter_exhausted)]
