from . import *

# * Hydro-Man — custom « DesignHacker » (sbire némésis de Human Torch)
# Hydro-Man cannot have flame counters placed on him.
# [star] Boost: Put Hydro-Man into play engaged with you.

def GetAbilities() -> Sequence['Ability']:

    def pas_de_flamme(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        message.maximum = 0

    return [
        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.Rule,
            "This",
            'flame',
            pas_de_flamme,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
