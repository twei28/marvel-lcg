from . import *

# Pore Over the Evidence — custom « ekAugust »
# Investigate 1[per_hero].
# When Defeated: Reduce the cost of the next card the Jessica Jones player
#   plays this phase by 2.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity is not None and "Jessica Jones" in identity.name:
                Worlds.UpdateNextCardPlayCost(
                    player,
                    -2,
                    effect,
                    in_this="Phase",
                )

    return [
        Investigate(1, per_hero=True),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
