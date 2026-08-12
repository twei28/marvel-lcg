from . import *

# Sneak Into the Crime Scene — custom « ekAugust »
# Investigate 2.
# When Defeated: Give Jessica Jones a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity is not None and "Jessica Jones" in identity.name:
                Faces.GiveStatus([identity], "Tough", effect)

    return [
        Investigate(2),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
