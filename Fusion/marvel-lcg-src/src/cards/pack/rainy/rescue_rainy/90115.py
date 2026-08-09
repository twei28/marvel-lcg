from . import *

# * Iron Man

def GetAbilities() -> Sequence['Ability']:

    def coup_de_pouce(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.GainValue(2, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            CardFinder(name="Iron Man"),
            coup_de_pouce
        ).SetTarget('Trigger')
        .SetCostFunc(CostFunc.Spend(Cost("1"))),
    ]
