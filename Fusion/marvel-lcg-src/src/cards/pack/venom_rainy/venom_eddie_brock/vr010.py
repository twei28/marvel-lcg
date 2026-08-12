from . import *

# Regeneration — custom « Rainy »
# You get +2 hit points.
# Alter-Ego Response: After you use your REC, exhaust Regeneration -> ready
#   Eddie Brock.

def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetIdentity()], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=2,
        ),

        AbilityFactory.AfterUnitRecovery(
            AbilityType.AlterEgoResponse,
            "You",
            regeneration,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
