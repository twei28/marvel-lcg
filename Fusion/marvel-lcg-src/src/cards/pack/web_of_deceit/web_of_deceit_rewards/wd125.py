from . import *

# Spider-Healing Factor

def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        # « Response: After your turn begins, exhaust Spider-Healing Factor →
        # heal 1 damage from your identity. »
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        this.HealthUnits([joueur.GetIdentity()], 1, effect)

    return [
        # « You get +3 hit points. »
        *AbilityFactory.GiveKeywordToAttached(
            health=3,
        ),
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            regeneration
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
