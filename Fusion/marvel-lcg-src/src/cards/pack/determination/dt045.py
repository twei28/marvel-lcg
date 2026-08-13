from . import *

# Flight

def GetAbilities() -> Sequence['Ability']:

    def flight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        villain = Worlds.FindVillain(effect)
        if villain:
            Faces.GiveStatus([villain], "Stunned", effect)
            Faces.GiveStatus([villain], "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            flight
        ).SetPlay(only_if_your_identity_has_trait="AERIAL")
        .SetCostFunc(CostFunc.PlaceThreatOn("MainScheme", 2)),
    ]
