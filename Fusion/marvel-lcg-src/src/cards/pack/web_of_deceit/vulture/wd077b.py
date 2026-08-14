from . import *

# Surveillance Pigeons (1B)

def GetAbilities() -> Sequence['Ability']:

    def bouclier(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        # « Forced Interrupt: When any amount of threat would be removed from
        # this scheme, if there are at least 3 pigeon counters here, remove
        # 3 pigeon counters from here instead. »
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([this], 3, 'pigeon', effect)

    def assez_de_pigeons(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return effect.this.CastTo(CanPlaceCounter).GetCounters('pigeon') >= 3

    return [
        AbilityFactory.WhenSchemeWouldRemoveThreat(
            AbilityType.ForcedInterrupt,
            "This",
            bouclier,
            conditions=[assez_de_pigeons],
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
