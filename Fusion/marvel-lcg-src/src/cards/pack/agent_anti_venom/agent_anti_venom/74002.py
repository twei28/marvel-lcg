from . import *

# * Spider-Man (Peter Parker) — custom « DesignHacker »
# Interrupt: When a non-ELITE minion would attack or scheme, spend a [mental]
#   resource -> cancel that activation.
#
# Montage de Web Binding (27006) : WhenEnemyWouldActivate couvre d'un coup
# l'attaque ET la manigance, `SetBeInstead` annule l'activation.

def GetAbilities() -> Sequence['Ability']:

    def spider_man(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.SetBeInstead(effect)

    def sbire_non_elite(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        enemy = message.trigger
        return Minion.IsType(enemy) and not enemy.HasTrait("ELITE")

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.Interrupt,
            None,
            spider_man,
            conditions=[sbire_non_elite],
        ).SetCost(Cost("B")),
    ]
