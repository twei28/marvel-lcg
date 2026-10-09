from . import *

# Iguana

def GetAbilities() -> Sequence['Ability']:

    def bonus(effect: 'Effect', faces) -> int:
        return min(NombreReptiles(effect), 4)

    return [
        AbilityFactory.ThisGainKeyword(bonus, attack=1, scheme=1),
    ]
