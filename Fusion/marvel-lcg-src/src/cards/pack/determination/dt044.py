from . import *

# Field Dressing

def GetAbilities() -> Sequence['Ability']:

    def field_dressing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        identity = effect.GetInitiator().GetIdentity()
        this.HealthUnits([identity], 6, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            field_dressing
        ).SetPlay()
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
