from . import *

# * Eddie Brock — custom « Rainy »
# Investigative Reporter — Response: After threat is placed on the main
#   scheme, remove 2 threat from a scheme. (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def investigative_reporter(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        this = effect.this.CastTo(AlterEgo)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.Response,
            MainScheme,
            investigative_reporter,
        ).SetName("Investigative Reporter")
        .SetTarget(Scheme2)
        .LimitOncePerRound(),
    ]
