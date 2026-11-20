from . import *

# Hellfire Ascendant (3A). « When Revealed : Search the encounter deck, discard pile, and set-aside area for the Mutant Supremacy side
# scheme and reveal it. (Shuffle.) » Mutant Supremacy (hf124) est dans le deck de rencontre : la recherche couvre les trois zones.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChercherEtReveler(effect, "Mutant Supremacy", mis_de_cote=True)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
