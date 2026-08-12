from . import *

# * Zombie Wolvie — custom « Kajislav » (sbire némésis d'Albert)
# When Defeated: Shuffle Zombie Wolvie into the encounter deck.

def GetAbilities() -> Sequence['Ability']:

    def zombie_wolvie(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            zombie_wolvie,
        ),
    ]
