from . import *

# "Legitimate Business"

def GetAbilities() -> Sequence['Ability']:

    def defaite(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        # « When Defeated: The first player discards cards from the top of the
        # encounter deck until an attachment is discarded and reveals that
        # card. »
        carte = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=Attachment,
        )
        if carte:
            carte.Reveal(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
