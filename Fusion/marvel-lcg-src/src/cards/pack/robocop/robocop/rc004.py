from . import *

# No Collateral (x2) : EVENEMENT (ATTACK. DEFENSE.), cout 1, [energy].
# Hero Interrupt (attack/defense): When an enemy attacks, prevent all damage from that attack and deal 2 damage to the attacking enemy.
#
# CARTES DE REFERENCE
#  - `32021` Shadow and Steel : texte identique a 4 degats pres (`WhenUnitWouldAttack(HeroInterrupt, Enemy, ..)` + `message.PreventDamage("All", effect)` +
#    `this.DealDamage([message.attacker], N, effect)` + `SetLabel('attack', 'defense')`). Condition `not message.IsBePrevent()`.
#
# TEXTE CONTRE CODE
#  « prevent ALL damage from that attack » -> `PreventDamage("All")`. « the ATTACKING enemy » -> `message.attacker`, pas une cible choisie. Deux labels (attack/defense).
#  Chiffres : cout 1, 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def no_collateral(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        message.PreventDamage("All", effect)
        this.DealDamage([message.attacker], 2, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            no_collateral,
            conditions=[
                lambda effect, message:
                    not message.IsBePrevent(),
            ],
        ).SetPlay().SetLabel('attack', 'defense'),
    ]
