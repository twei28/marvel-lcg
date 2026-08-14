from . import *

# * Vulture (III) — sous-fifre

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for the
        # Feather Daggers attachment and reveal it. »
        ChercherEtReveler(effect, name="Feather Daggers")

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        RiposteSaufContreLesAeriens(3),
    ]
