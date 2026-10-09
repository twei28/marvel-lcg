from . import *

# hs033b Thirst for Revenge

def GetAbilities() -> Sequence['Ability']:

    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        PlacerUneBlessureSurJameson(effect)

    return [
        AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.NonKeywordBold, "This", terminee),
    ]
