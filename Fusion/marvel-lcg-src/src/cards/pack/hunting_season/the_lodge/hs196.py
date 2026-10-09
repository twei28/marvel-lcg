from . import *

# hs196 Trap (Experience Cost 1)
# Interrupt : quand un ennemi t'attaque, defausse Trap -> 2 degats a cet ennemi.
# S'il est vaincu ainsi, Trap revient dans ta main.

def GetAbilities() -> Sequence['Ability']:

    def pieger(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        joueur = effect.GetInitiator()

        def vaincu(unit: 'Unit2') -> None:
            Unused(unit)
            joueur.GainCard([this], effect)

        this.DealDamage([message.attacker], 2, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.Interrupt, Enemy, pieger)
        .SetCostFunc(CostFunc.Discard("This")),
    ]
