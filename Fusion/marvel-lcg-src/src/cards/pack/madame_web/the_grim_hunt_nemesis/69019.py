from . import *

# * Kraven the Hunter — custom « Kajislav », minion nemesis
# Retaliate 1. Villainous. (mots-cles portes par cards.json)
# When Defeated: Set Kraven the Hunter aside, out of play.

def GetAbilities() -> Sequence['Ability']:

    def kraven(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)

        Faces.SetAside([this], effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            kraven
        ),
    ]
