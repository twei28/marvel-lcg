from . import *

# "Here I Come!" — custom « ekAugust »
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains
# overkill. If this attack defeats an enemy, ____.
# Bulle : « Deal 2 damage to the villain. »

def GetAbilities() -> Sequence['Ability']:

    def here_i_come(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        def defeated(unit: 'Unit2'):
            Unused(unit)
            ResolveBlank(effect)

        this.DealDamage(
            effect.targets, 5, effect,
            property=AttackProperty(overkill=True),
            if_this_attack_defeats=defeated,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            here_i_come
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
