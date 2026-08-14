from . import *

# Dynamo

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        # « Response: After you play a SUPERPOWER card, remove 1 energy counter
        # from Dynamo → stun an enemy and deal 2 damage to it. »
        this = effect.this.CastTo(Upgrade)
        Faces.GiveStatus(effect.targets, "Stunned", effect)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="SUPERPOWER"),
            decharge
        ).SetCostFunc(CostFunc.Counter("This", 1, 'energy'))
        .SetTarget(Enemy),
    ]
