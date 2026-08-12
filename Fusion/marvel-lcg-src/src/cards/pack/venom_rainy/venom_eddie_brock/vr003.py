from . import *

# Just A Snack — custom « Rainy »
# Hero Action (attack): Deal 1 damage to an enemy (2 damage instead if you
#   paid for this card using a [physical] resource). Heal 2 damage from Venom.

def GetAbilities() -> Sequence['Ability']:

    def just_a_snack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        degats = 1
        paye = getattr(effect.context, 'paid_this_resources', None)
        if paye and paye.rbyg.r > 0:
            degats = 2

        this.DealDamage(effect.targets, degats, effect)

        initiator = effect.GetInitiator()
        this.HealthUnits([initiator.GetIdentity()], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            just_a_snack
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
