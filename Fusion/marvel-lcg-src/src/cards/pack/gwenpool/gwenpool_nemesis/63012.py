from . import *

# * Evil Gwenpool — custom « ekAugust » (sbire némésis de Gwenpool)
# Steady. Villainous. (desc)
# When Defeated: Shuffle Evil Gwenpool into the encounter deck.
# [star] Boost: Put Evil Gwenpool into play engaged with you.
# Bulle : « Gwenpool takes 1 damage. » (utilisée par Rules of the Universe)

def GetAbilities() -> Sequence['Ability']:

    def evil_gwenpool(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            evil_gwenpool,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
