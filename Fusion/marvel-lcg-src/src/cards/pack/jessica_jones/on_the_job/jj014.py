from . import *

# Hang Back and Watch — custom « ekAugust »
# Investigate 2[per_hero].
# When Defeated: Heal 2 damage from Jessica Jones.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity is not None and "Jessica Jones" in identity.name:
                this.HealthUnits([identity], 2, effect)

    return [
        Investigate(2, per_hero=True),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
