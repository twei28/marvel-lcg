from . import *

# Web Barrage — custom « Rainy » (cout X)
# Hero Action: Make the following attack against X enemies.
# (attack): Web an enemy and deal 2 damage to them. This attack gains ranged.

def GetAbilities() -> Sequence['Ability']:

    def barrage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        cibles = list(effect.targets)[:effect.GetCostX()]
        if not cibles:
            return
        Weber(cibles, 1, effect)
        this.DealDamage(
            cibles, 2, effect,
            property=AttackProperty(ranged=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            barrage
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy, range=(1, "All")),
    ]
