from . import *

# Foresight — amelioration. GENIUS. TACTIC. Cout 1.
# Hero Action: Take 2 damage and exhaust Foresight -> ready Venompool.
#
# Cartes de reference : 44010 (pack deadpool) pour
# `CostFunc.TakeDamage(n, "YourIdentity")`, 04001b pour l'epuisement en cout,
# 60054 Stand Alone (pack fne) pour `Faces.ReadyAll([identite], effect)`.
#
# Le cout est DOUBLE et indivisible (« Take 2 damage AND exhaust ») : deux
# `SetCostFunc` enchaines, que `Ability.SetCostFunc` empile (ability.py:999).

def GetAbilities() -> Sequence['Ability']:

    def foresight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        identity = GetVenompool(effect)
        if identity is not None:
            Faces.ReadyAll([identity], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            foresight,
        ).SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
