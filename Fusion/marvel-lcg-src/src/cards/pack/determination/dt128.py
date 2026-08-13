from . import *

# * MRVL Network

def GetAbilities() -> Sequence['Ability']:

    def mrvl_network(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    def check_phase_du_mechant(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        # La phase se lit par son objet, pas par une chaine (48014).
        return Worlds.Phase(effect).IsVillainPhase()

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            Enemy,
            mrvl_network,
            conditions=[check_phase_du_mechant],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'replay'))
        .SetTarget("YouControlUnit", canbe_ready=True),
    ]
