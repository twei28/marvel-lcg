from . import *

# * Vulture (II)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for
        # Feather Daggers and reveal it. »
        ChercherEtReveler(effect, name="Feather Daggers")

    return [
        NePeutEtreAttaqueQueParLesAeriens(),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
