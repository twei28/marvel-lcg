from . import *

# * Luke Cage — custom « ekAugust »
# Toughness.
# While there is a side scheme in play, reduce any damage Luke Cage takes by 1.

def GetAbilities() -> Sequence['Ability']:

    def reduce_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.ReduceDamage(1, effect)

    def side_scheme_in_play(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return len(Worlds.GetSideSchemes(effect)) > 0

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            reduce_damage,
            conditions=[side_scheme_in_play],
        ),
    ]
