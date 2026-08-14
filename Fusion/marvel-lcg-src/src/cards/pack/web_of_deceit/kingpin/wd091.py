from . import *

# * Kingpin (I)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for
        # Kingpin's Suit and reveal it. »
        ChercherEtReveler(effect, name="Kingpin's Suit")

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
