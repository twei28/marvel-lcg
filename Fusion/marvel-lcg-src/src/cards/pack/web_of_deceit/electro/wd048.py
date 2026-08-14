from . import *

# Accelerated Plans

def GetAbilities() -> Sequence['Ability']:

    def entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        # « Forced Response: After this side scheme enters play, place 2 threat
        # here for each acceleration icon and token in play. »
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = 2 * JetonsEtIconesDAcceleration(effect)
        if valeur > 0:
            this.PlaceThreatOnSchemes([this], valeur, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            entree
        ),
    ]
