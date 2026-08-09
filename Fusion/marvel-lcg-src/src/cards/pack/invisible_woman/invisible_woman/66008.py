from . import *


def GetAbilities() -> Sequence['Ability']:

    def incognito(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        deck = Worlds.GetEncounterDeck(effect)
        faces = deck.Get(True)[:4]
        stars = FacesCounter.CountTotalBoostStar(faces)
        if stars:
            effect.GetInitiator().DrawUp(stars, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            incognito,
        ).SetPlay(only_if_your_identity_has_trait="INVISIBLE")
        .SetName("Incognito"),
    ]
