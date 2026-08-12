from . import *

# Lethal Directive — custom « Kajislav »
# Hero Action (attack): Deal 4 damage to an enemy. If that enemy is defeated
# by this attack, resolve Albert's "Initiate Protocol" ability.

def GetAbilities() -> Sequence['Ability']:

    def lethal_directive(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        def defeated(unit: 'Unit2'):
            Unused(unit)
            ResolveInitiateProtocol(effect)

        this.DealDamage(effect.targets, 4, effect, if_this_attack_defeats=defeated)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lethal_directive
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
