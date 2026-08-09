from . import *

# * Elsie-Dee — custom « Kajislav »
# Interrupt: When Elsie-Dee would be defeated by taking excess damage, deal
# X damage among enemies in play, where X is equal to the excess amount.

def GetAbilities() -> Sequence['Ability']:

    def elsie_dee(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)

        excess = message.excess_damage
        if excess <= 0:
            return

        player = this.GetControlBy()
        if player is None:
            return

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal the excess damage among enemies in play",
                lambda targets:
                    this.DealDamage(targets, 1, effect)
            ).SetTarget(Enemy, range=(1, excess), repeat_rules="Health")
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            elsie_dee,
            took_excess_damage=True,
        ),
    ]
