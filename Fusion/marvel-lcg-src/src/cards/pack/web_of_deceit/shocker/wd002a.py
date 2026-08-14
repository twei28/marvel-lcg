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

        # Regle commune a TOUS les scenarios de la campagne (livret p.3) :
        # « Put the "Vote for Fisk" environment into play. » La face experte est
        # une carte a part, pas un dos : c'est ici qu'on choisit.
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
    ]
