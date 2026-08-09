from . import *

# Breakthrough — custom « ekAugust »
# Hero Action (attack): Deal 4 damage to an enemy. Deal 1 additional damage to
#   that enemy for each side scheme in play.

def GetAbilities() -> Sequence['Ability']:

    def breakthrough(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        damage = 4 + len(Worlds.GetSideSchemes(effect))
        this.DealDamage(effect.targets, damage, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            breakthrough,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
