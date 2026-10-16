from . import *

# Headstrong (Temper de Rocksteady, face ENRAGED)

def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(Villain, trait="ENRAGED"),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        *TempersEnrages("Rocksteady"),
    ]
