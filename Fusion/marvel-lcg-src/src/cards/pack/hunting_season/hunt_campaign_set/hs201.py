from . import *

# hs201 * Scorpion (allie, recompense du scenario 2)
# Response : apres avoir attaque et blesse un ennemi, inflige 1 degat a Scorpion
# -> etourdis cet ennemi et inflige-lui 1 degat.

def GetAbilities() -> Sequence['Ability']:

    def piquer(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        for ennemi in [message.attacked]:
            if ennemi.IsInPlay():
                Faces.GiveStatus([ennemi], "Stunned", effect)
                this.DealDamage([ennemi], 1, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.Response, "This", Enemy, piquer)
        .SetCostFunc(CostFunc.TakeDamage(1, "This")),
    ]
