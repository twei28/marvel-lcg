from . import *

# Tough Call

def GetAbilities() -> Sequence['Ability']:

    def tough_call(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        donnes = Faces.GiveStatus(effect.targets, "Tough", effect)
        if donnes and any(Enemy.IsType(f) for f in effect.targets):
            hero = effect.GetInitiator().GetHero()
            this.HealthUnits([hero], 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tough_call
        ).SetPlay()
        .SetCostFunc(CostFunc.TakeDamage(2, "Initiator"))
        .SetTarget("Character"),
    ]
