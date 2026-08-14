from . import *

# Surveillance Pigeons (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Each player puts a Wingsuit upgrade into play under their
        # control. Put each copy of Aerial Advantage into play. »
        def wingsuit(joueur: 'Player') -> None:
            carte = Search.SearchForCard(
                effect,
                joueur,
                include_set_aside=True,
                card_ids=["wd090"],
            )
            if carte:
                carte.PutIntoPlay(joueur, effect, under_control=True)

        Players.ForEachPlayer(effect, wingsuit)

        premier = Worlds.GetFirstPlayer(effect)
        for carte in CardFinder(name="Aerial Advantage").Checks(
                Worlds.GetEncounterDeckCards(effect)):
            carte.PutIntoPlay(premier, effect)

        # Regle commune a TOUS les scenarios de la campagne (livret p.3).
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
    ]
