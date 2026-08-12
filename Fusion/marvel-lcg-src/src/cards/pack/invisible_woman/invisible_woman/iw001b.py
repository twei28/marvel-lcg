from . import *


def GetAbilities() -> Sequence['Ability']:

    def great_minds_resources(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        player = message.GetToPlayer()
        value = 2 if player.IsControl(CardFinder(name="Reed Richards")) else 1
        return Resources("B") * value

    def ready_sue_if_paying_for_tech(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        paying_for = message.for_effect.this
        if paying_for and paying_for.HasTrait("TECH"):
            Faces.ReadyAll([effect.this], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=great_minds_resources,
            ex_operation=ready_sue_if_paying_for_tech,
        ).SetCostFunc(CostFunc.Exhaust("This")).LimitOncePerRound()
        .SetName("Great Minds"),
    ]
