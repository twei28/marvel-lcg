from . import *

# Locating Cerebro (2B), stade 2. « When Completed : Flip White Queen. » (puis le moteur avance au stade 3.)


def GetAbilities() -> Sequence['Ability']:
    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        RetournerWQ(effect)

    return [AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.ForcedInterrupt, "This", terminee)]
