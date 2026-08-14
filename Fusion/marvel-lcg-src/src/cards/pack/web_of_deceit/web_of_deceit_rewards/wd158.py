from . import *

# * Spider-Boy

def GetAbilities() -> Sequence['Ability']:

    def coup_de_main(effect: 'Effect') -> None:
        # « Response: After Spider-Boy enters play or leaves play, remove
        # 1 threat from a scheme. »
        this = effect.this.CastTo(Ally)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            lambda effect, message: coup_de_main(effect)
        ).SetTarget(Scheme2),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            lambda effect, message: coup_de_main(effect)
        ).SetTarget(Scheme2),
    ]
