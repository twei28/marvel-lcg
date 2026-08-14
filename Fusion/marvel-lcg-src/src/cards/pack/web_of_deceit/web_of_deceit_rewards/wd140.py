from . import *

# * See the Future

def GetAbilities() -> Sequence['Ability']:

    def vision(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        # « When Defeated: Each player draws 2 cards. Until the end of the
        # round, play with the top card of the encounter deck faceup. »
        Players.ForEachPlayer(effect, lambda joueur: joueur.DrawUp(2, effect))

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vision
        ),
        # ⚠ ECART, ecrit : « Until the end of the round, play with the top card
        # of the encounter deck faceup » demande une fenetre temporaire que
        # `PlayWithTopCardOfDeckFaceup` ne sait pas ouvrir — elle est ecrite pour
        # une carte qui reste en jeu, et rend d'ailleurs une LISTE d'abilites.
        # Seule la pioche de deux cartes est rendue.
    ]
