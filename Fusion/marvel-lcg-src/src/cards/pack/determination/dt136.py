from . import *

# Leverage Impediments

def GetAbilities() -> Sequence['Ability']:

    def leverage_impediments(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        for cible in effect.targets:
            supplement = len(cible.GetInventoryDeck().GetAll())
            avant = cible.CastTo(CanHealth).health
            this.DealDamage([cible], 2 + supplement, effect)
            if cible.CastTo(Unit2).IsDefeated() and avant == 2 + supplement:
                this.HealthUnits([initiator.GetIdentity()], 2, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            your_identity_has_traits=["MARTIAL ARTIST"],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            leverage_impediments
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
