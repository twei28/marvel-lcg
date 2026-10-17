from . import *

# * Rupert's Pizzeria (bandeau « ✦ X-Mansion ») — SOUTIEN 2 [mental], aspect Basic. LOCATION. NYC. STREETS.
# Alter-Ego Action: Exhaust Rupert's Pizzeria → heal 1 damage from a [[MUTANT]], [[MUTANIMAL]] or [[NINJA]]
#   character. Any player whose alter-ego has the [[MUTANT]] trait may trigger this ability.
#
# MODIFIEE de 32049 X-Mansion : « MUTANT or X-MEN » -> « MUTANT, MUTANIMAL or NINJA ». Script copie de 32049.


def GetAbilities() -> Sequence['Ability']:

    def ruperts_pizzeria(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            ruperts_pizzeria
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Unit2, traits=["MUTANT", "MUTANIMAL", "NINJA"], canbe_heal=True)
        .AnyPlayerCanDoThis(player_alter_ego_has_trait="MUTANT"),
    ]
