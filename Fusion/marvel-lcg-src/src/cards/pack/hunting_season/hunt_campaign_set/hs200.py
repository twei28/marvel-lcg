from . import *

# hs200 * Vermin (allie, recompense du scenario 1)
# Entre en jeu avec 3 pions rat. Interrupt : quand il attaque, retire un pion rat
# -> pas de degats consecutifs pour cette attaque.

def GetAbilities() -> Sequence['Ability']:

    def sans_contrecoup(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoesNotTakeConsequentialDamage(effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(3, 'rat'),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, "This", sans_contrecoup)
        .SetCostFunc(CostFunc.Counter("This", 1, 'rat')),
    ]
