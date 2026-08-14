from . import *

# Martha and Billy

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Place 1 sanity counter on Lizard Brain. »
        #
        # La seule carte du deck qui CHARGE le cerveau sans passer par la
        # defaite du Lizard : le souvenir de sa famille le retient.
        cerveau = LizardBrain(effect)
        if cerveau:
            Faces.PlaceCountersOn([cerveau], 1, 'sanity', effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
