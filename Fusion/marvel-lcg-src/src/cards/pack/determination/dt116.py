from . import *

# * Agent Koenig

def GetAbilities() -> Sequence['Ability']:

    def agent_koenig(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)

        message.SetBeInstead(effect)
        this.HealthUnits([this], "All", effect)

    return [
        Fragile(),
        AbilityFactory.ThisEnterPlayWithCounters(1, 'LMD'),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if effect.this.CastTo(CanPlaceCounter).GetAllCounters() else 0,
            attack=1,
            change_on_event=OnEvent.Counter("This", 'LMD'),
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            agent_koenig
        ).SetCostFunc(CostFunc.Counter("This", 1, 'LMD')),
    ]
