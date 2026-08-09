from . import *

# "Look At Me!" — custom « ekAugust »
# Purple Man cannot take damage.
# Forced Response: After a side scheme is defeated, place X threat on the main
#   scheme, where X is equal to the number of side schemes in play.
# Boost: After this activation ends, reveal this card.

def GetAbilities() -> Sequence['Ability']:

    def look_at_me(effect: 'Effect', message: 'Message.AfterSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        value = len(Worlds.GetSideSchemes(effect))
        if value:
            main = Worlds.FindMainScheme(this)
            if main:
                this.PlaceThreatOnSchemes([main], value, effect)

    def look_at_me_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        player = message.GetToPlayer()
        message.AfterThisActivation(effect, lambda: this.Reveal(player, effect))

    return [
        AbilityFactory.UnitCannotTakeDamageWhile(
            AbilityType.NonKeyword,
            CardFinder(name="Purple Man"),
        ),

        AbilityFactory.AfterSchemeBeDefeated(
            AbilityType.ForcedResponse,
            SchemeSide2,
            look_at_me,
        ),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            look_at_me_boost,
        ),
    ]
