from . import *

# Collision Course

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for temper in TousLesTempers(effect):
            Faces.PlaceCountersOn([temper], 1, COMPTEUR, effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Faces.GiveStatus(VilainsEnJeu(effect), "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
