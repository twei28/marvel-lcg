from . import *

# Reckless Charge

def GetAbilities() -> Sequence['Ability']:

    def reckless_charge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        # Payee avec du [physical] : l'attaque gagne overkill.
        overkill = effect.GetPaidResources().HasColor("R")

        hero.DealDamage(effect.targets, 3, effect,
                        property=AttackProperty(overkill=overkill))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless_charge
        ).SetPlay().SetLabel('attack')
        # « Deal 1 damage to Hulk » est le cout de l'attaque.
        .SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetTarget(Enemy),
    ]
