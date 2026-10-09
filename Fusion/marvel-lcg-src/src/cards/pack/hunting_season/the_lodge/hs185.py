from . import *

# hs185 Hunting Rifle (Experience Cost 2)
# Restricted. Uses (3 ammo counters) : donnees.
# Hero Action (attack) : incline et retire 1 pion munition -> 2 degats a un ennemi, attaque ranged.

def GetAbilities() -> Sequence['Ability']:

    def tirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        this.DealDamage(effect.targets, 2, effect, property=AttackProperty(ranged=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, tirer).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget(Enemy),
    ]
