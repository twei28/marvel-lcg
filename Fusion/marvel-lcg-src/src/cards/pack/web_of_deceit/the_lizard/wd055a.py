from . import *
from cards.pack.web_of_deceit.campaign import ChaqueJoueurRetrouveSesTalents

# Chasing Down The Lizard (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Reveal the Lizard Brain environment. Place 1 formula counter
        # on The Lizard. In expert mode, place 1 additional formula counter. »
        ChercherEtReveler(effect, name="Lizard Brain")

        lizard = Worlds.FindVillain(effect)
        if lizard:
            combien = 2 if Worlds.IsExpert(effect) else 1
            Faces.PlaceCountersOn([lizard], combien, 'formula', effect)

        # Regle commune a TOUS les scenarios de la campagne (livret p.3).
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
        # Les paliers d'arbre de talents deja gagnes reviennent dans le
        # deck de leur proprietaire (voir `campaign.py`).
        ChaqueJoueurRetrouveSesTalents(),
    ]
