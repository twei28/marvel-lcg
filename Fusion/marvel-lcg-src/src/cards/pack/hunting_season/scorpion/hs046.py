from . import *

# hs046 Luring Out Prey

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Faces.PlaceTokensOn([this], Worlds.ConvertPerPlayerIconToInt("1*", effect), 'threat', effect)
    return [AbilityFactory.WhenThisRevealed(None, revelee)]
