from . import *

# * Venom

def GetAbilities() -> Sequence['Ability']:

    def venom(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            venom
        ),
    ]
