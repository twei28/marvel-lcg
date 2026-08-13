from . import *

# * MRVL Network

def GetAbilities() -> Sequence['Ability']:

    def mrvl_network(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    def check_phase_du_mechant(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        return Worlds.GetPhase(effect) == "Villain"

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            Enemy,
            mrvl_network,
            conditions=[check_phase_du_mechant],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'replay'))
        .SetTarget("YouControlUnit", canbe_ready=True),
    ]
