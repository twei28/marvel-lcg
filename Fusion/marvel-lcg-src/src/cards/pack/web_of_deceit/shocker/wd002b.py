from . import *

# Shock Party (1B)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for the
        # Vibro-Shock Gauntlets attachment and reveal it. »
        ChercherEtReveler(effect, name="Vibro-Shock Gauntlets")

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
