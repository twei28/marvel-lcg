from . import *

# * Hairball — custom « Nugget » (carte d'aspect PROTECTION)
# Companion.
# Interrupt: When a friendly character would take any amount of damage from an
#   attack, exhaust Hairball → prevent 1 of that damage.


def GetAbilities() -> Sequence['Ability']:

    def amortir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        *Companion(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Friend,
            amortir,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
