from . import *

# Medical Clinic — custom "Rainy"
# Jane Foster gets +2 REC.
# Alter-Ego Action: Exhaust Medical Clinic and spend 1 resource -> heal 3
# damage from an identity.

def GetAbilities() -> Sequence['Ability']:

    def heal_identity(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.HealthUnits(effect.targets, 3, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Jane Foster", card_type=Identity),
            control_by="You",
            recover=2,
        ),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            heal_identity
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Spend(Cost("1")))
        .SetTarget(Identity, canbe_heal=True)
    ]
