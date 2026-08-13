from . import *

# Go Wild

def GetAbilities() -> Sequence['Ability']:

    def go_wild(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        piochees = initiator.DrawUp(3, effect)
        valeur = FacesCounter.GetPrintedCost(piochees or [])
        if valeur > 0:
            this.DealDamage(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            go_wild
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.TakeDamage(2, "Initiator"))
        .SetTarget(Enemy),
    ]
