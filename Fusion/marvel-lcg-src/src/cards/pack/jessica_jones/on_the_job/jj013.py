from . import *

# Chase Down a Lead — custom « ekAugust »
# Investigate 2.
# When Defeated: The Jessica Jones player searches the top 5 cards of their
#   deck for a hero-specific card and adds it to their hand. (Shuffle.)

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity is None or "Jessica Jones" not in identity.name:
                continue
            face = Search.PlayerDeckTop(
                effect,
                player,
                5,
                card_class="IdentitySpecific",
            )
            if face:
                player.GainCard(face, effect)

    return [
        Investigate(2),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
