from . import *

# * Spider-Man (Pavitr Prabhakar)

def GetAbilities() -> Sequence['Ability']:

    def sortie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        # « Response: After Spider-Man leaves play, remove 4 threat from a
        # scheme. »
        this = effect.this.CastTo(Ally)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            sortie
        ).SetTarget(Scheme2),
    ]
