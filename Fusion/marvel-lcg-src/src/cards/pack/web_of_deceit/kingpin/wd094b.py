from . import *

# Shadow of the Kingpin (1B)

def GetAbilities() -> Sequence['Ability']:

    def deep_pockets(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        # « Deep Pockets — Forced Response: After resolving step one of the
        # villain phase, the first player places 1 pursuit counter on Pursued by
        # the Past. »
        CompteursDePoursuite(effect, 1)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            deep_pockets
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
