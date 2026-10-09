from . import *

# hs035 * J. Jonah Jameson

def GetAbilities() -> Sequence['Ability']:

    def ami(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.trigger in Worlds.GetOnFieldFriendlyCharacters(effect)

    def prevenir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        Faces.PlaceCountersOn([effect.this], 1, 'wound', effect)
        message.PreventDamage("All", effect)

    def perdre(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt, CardFace, prevenir, conditions=[ami],
        ),
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedInterrupt, "This", 'wound', perdre,
            at_least=lambda effect: 3 + Worlds.GetPlayerNumIcon(effect),
        ),
    ]
