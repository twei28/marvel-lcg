from . import *

# * Vulture (I) — sous-fifre

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        ChercherLesCieux(effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
        RiposteSaufContreLesAeriens(2),
    ]
