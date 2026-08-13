from . import *

# Shock Party (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Search the encounter deck for The Long Night side scheme and
        # reveal it. Remove each obligation card in the encounter deck from the
        # game. »
        ChercherEtReveler(effect, name="The Long Night")

        obligations = CardFinder(card_type=Obligation).Checks(
            Worlds.GetEncounterDeckCards(effect))
        if obligations:
            Faces.RemoveAllFromGame(obligations, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
    ]
