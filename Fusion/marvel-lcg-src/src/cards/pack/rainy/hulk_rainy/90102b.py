from . import *

# * Bruce Banner

def GetAbilities() -> Sequence['Ability']:

    def bring_out_the_big_guy(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        effect.targets[0].CastTo(Identity).ChangeToForm(Hero, effect)
        message.SetBeInstead(effect)

        message.trigger.CastTo(Enemy).DoAttackYou(initiator, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.Interrupt,
            Enemy,
            bring_out_the_big_guy
        ).SetName("Bring Out The Big Guy")
        .SetCostFunc(CostFunc.Spend(Cost("R")))
        .SetTarget("YourIdentity"),
    ]
