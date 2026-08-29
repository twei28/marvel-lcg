from . import *
def GetAbilities() -> Sequence['Ability']:
    def circumstantial_evidence(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        if alias:
            alias.PlaceCountersInternal(1, 'evidence', effect)
    return [
        AbilityFactory.AfterUnitBeDefeated(AbilityType.Response, Enemy, circumstantial_evidence)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
