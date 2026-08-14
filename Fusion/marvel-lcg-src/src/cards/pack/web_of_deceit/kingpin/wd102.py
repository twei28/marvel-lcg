from . import *

# * Lady Bullseye

def GetAbilities() -> Sequence['Ability']:

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Place 2 pursuit counters on Pursued by the Past. »
        CompteursDePoursuite(effect, 2)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
