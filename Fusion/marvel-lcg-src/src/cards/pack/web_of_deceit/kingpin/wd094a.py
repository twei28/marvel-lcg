from . import *

# Shadow of the Kingpin (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        # « Setup: Find Fisk Tower and put it into play. Place 1[per_hero]
        # counters on Pursued by the Past. »
        premier = Worlds.GetFirstPlayer(effect)
        tour = Search.SearchForCard(
            effect,
            premier,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            name="Fisk Tower",
        )
        if tour:
            tour.PutIntoPlay(premier, effect)

        CompteursDePoursuite(effect, Worlds.GetPlayerNumIcon(effect))

        # Regle commune a TOUS les scenarios de la campagne (livret p.3).
        MettreVoteForFiskEnJeu(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
    ]
