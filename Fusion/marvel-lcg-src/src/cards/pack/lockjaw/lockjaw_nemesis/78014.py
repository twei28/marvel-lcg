from . import *

# Dognapped! — custom « Nugget » (némésis de Lockjaw)
# Forced Response: After a TELEPORT event is played, place 1 threat here.


def GetAbilities() -> Sequence['Ability']:

    def apres_teleport(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "AnyPlayer",
            CardFinder2("TELEPORT", Event),
            apres_teleport,
        ),
    ]
