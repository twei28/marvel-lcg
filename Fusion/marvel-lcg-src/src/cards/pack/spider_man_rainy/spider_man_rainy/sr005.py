from . import *

# Web Strike — custom « Rainy »
# Hero Action (attack): Deal 6 damage to an enemy. If that enemy is webbed,
#   deal 2 additional damage. This attack gains overkill.

def GetAbilities() -> Sequence['Ability']:

    def strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        for cible in effect.targets:
            degats = 6 + (2 if cible.GetCounters('web') > 0 else 0)
            this.DealDamage(
                [cible], degats, effect,
                property=AttackProperty(overkill=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            strike
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
