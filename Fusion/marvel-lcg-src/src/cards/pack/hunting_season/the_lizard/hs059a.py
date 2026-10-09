from . import *

# hs059a No Humanity Left
# When Revealed : sans Lizard en jeu, Curtis Connors se retourne ; Reptilian Rage
# monte a 3 compteurs de honte. Passage en 3B par le moteur.

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if not LizardEnJeu(effect):
            v = Vilain(effect)
            if v:
                v.card.Flip(effect)
        CompleterHonte(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
