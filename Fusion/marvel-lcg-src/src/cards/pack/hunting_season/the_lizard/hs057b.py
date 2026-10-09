from . import *

# hs057b Using the Mammal Brain
# When Completed : Reptilian Rage monte a 3 compteurs de honte ; sans Lizard en
# jeu, Curtis Connors se retourne.

def GetAbilities() -> Sequence['Ability']:

    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        CompleterHonte(effect)
        if not LizardEnJeu(effect):
            v = Vilain(effect)
            if v:
                v.card.Flip(effect)

    return [
        AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.NonKeywordBold, "This", terminee),
    ]
