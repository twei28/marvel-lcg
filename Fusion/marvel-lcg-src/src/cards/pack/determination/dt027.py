from . import *

# Cheap Shot

def GetAbilities() -> Sequence['Ability']:

    def cheap_shot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        valeur = 2
        for cible in effect.targets:
            statuts = cible.CastTo(CanStatus)
            if statuts.IsStunned() or statuts.IsConfused():
                valeur = 4
        this.DealDamage(effect.targets, valeur, effect,
                        property=AttackProperty(piercing=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cheap_shot
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
