from . import *

# * Model V Chassis

def GetAbilities() -> Sequence['Ability']:

    def blindage(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        hero = effect.GetInitiator().GetHero()
        Faces.GiveStatus([hero], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "You",
            blindage,
            conditions=[
                # « take no damage » : la defense n'a rien laisse passer.
                # (champ du message : taken_damage)
                lambda effect, message: message.taken_damage == 0
            ],
        # SetCostFunc empile : deux appels = deux couts a payer.
        ).SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Spend(Cost("1"))),
    ]
