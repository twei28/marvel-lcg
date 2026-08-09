# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from cards.pack import *
def GetAbilities() -> Sequence['Ability']:
    def nova(effect: 'Effect2', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        this.DealDamage(effect.targets, 8, effect)
    return [AbilityFactory.WhenUnitInitiatesAttackAgainst(AbilityType.Interrupt, Enemy, 'You', nova).SetCost(Cost('Y')).SetTarget('Attacker')]
