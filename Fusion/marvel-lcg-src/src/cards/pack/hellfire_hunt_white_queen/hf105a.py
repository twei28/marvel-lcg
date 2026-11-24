from . import *

# Locating Cerebro (2A). « When Revealed : The first player searches the encounter deck and discard pile for a copy of the Crystalline
# Adaptation attachment and reveals it. (Shuffle.) » (la carte s'attache toute seule a White Queen : voir hf107.)
# Cartes de reference : 01180 Legions of Hydra (`Search.EncounterCard` + melange), 45144 (`face.Reveal`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChercherEtReveler(effect, "Crystalline Adaptation")

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
