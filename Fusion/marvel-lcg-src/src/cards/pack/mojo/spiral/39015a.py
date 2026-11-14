from . import *
from cards.pack.mojo.campaign import CampaignSetup

# Across the Mojoverse

def GetAbilities() -> Sequence['Ability']:

    def across_the_mojoverse(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            name="The Search for Spiral",
            card_type=SchemeSide2
        )

        first_player = Worlds.GetFirstPlayer(effect)

        shows: List['CardFace']
        shows = Worlds.GetEncounterDeck(effect).FindCards(
            trait="SHOW",
            card_type=Environment
        )

        show = Rand.RandomChoice(shows, effect)
        show.PutIntoPlay(first_player, effect)
        shows.remove(show)

        cornered = Worlds.AsideDeck(effect).FindCard(
            name="Cornered!",
            card_type=Treachery
        )

        if cornered:
            shows.append(cornered)

        villain = Worlds.FindVillain(effect)
        assert villain
        GetShowDeck(effect).Create(effect, villain)
        GetShowDeck(effect).PushCards(
            shows,
            effect,
        )
        # « Shuffle each other SHOW environment together with the Cornered!
        # treachery to create the show deck ». `PushCards` ne melange pas, et
        # Cornered!, ajoutee en dernier, etait toujours le premier Show revele.
        # Trouve par l'audit des decks du 04/10/2026.
        GetShowDeck(effect).deck.Shuffle(effect)


    return [
        *CampaignSetup(2),
        AbilityFactory.WhenCardSetup(
            "This",
            across_the_mojoverse
        ),
    ]

