from . import *

# Toro! Toro!

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurVainqueur(message, effect)
        tempers = TousLesTempers(effect)
        if not tempers:
            return
        cible = tempers[0] if len(tempers) == 1 else joueur.AskChooseFace(
            tempers, effect, prompt="Choose a TEMPER attachment")
        if cible is not None:
            Faces.PlaceCountersOn([cible], 2, COMPTEUR, effect)

    return [
        Dodgy(),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
