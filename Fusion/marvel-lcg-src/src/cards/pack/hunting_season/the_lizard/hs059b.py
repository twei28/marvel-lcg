from . import *

# hs059b No Humanity Left

def GetAbilities() -> Sequence['Ability']:

    def pas_de_retournement(effect: 'Effect', message: 'Message.WhenCardWouldFlip') -> None:
        message.SetBeInstead(effect)

    return [
        Ability(
            AbilityType.NonKeyword,
            Message.WhenCardWouldFlip,
            [lambda effect, message: EstLizard(message.trigger)],
            pas_de_retournement,
        ),
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This"),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
