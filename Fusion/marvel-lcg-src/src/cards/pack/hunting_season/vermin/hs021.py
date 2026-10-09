from . import *

# hs021 Bringer of Plague
# When Revealed: Place threat here equal to the amount of threat on RAT minions in play.

def GetAbilities() -> Sequence['Ability']:

    def menace(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        valeur = MenaceSurLesRats(effect)
        if valeur > 0:
            Faces.PlaceTokensOn([effect.this], valeur, 'threat', effect)

    return [
        AbilityFactory.WhenThisRevealed(None, menace),
    ]
