from . import *
from cards.pack.web_of_deceit.campaign import ChaqueJoueurRetrouveSesTalents

# Power Outage (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Put the Electricity Clones and Grounded environments into
        # play. » Les deux sont dans le deck rencontre, comme The Long Night
        # l'est dans celui de Shocker : on les en sort a la mise en place.
        premier = Worlds.GetFirstPlayer(effect)
        for nom in ("Electricity Clones", "Grounded"):
            carte = Search.SearchForCard(
                effect,
                premier,
                include_encounter_deck=True,
                include_encounter_discard_pile=True,
                name=nom,
            )
            if carte:
                carte.PutIntoPlay(premier, effect)

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
