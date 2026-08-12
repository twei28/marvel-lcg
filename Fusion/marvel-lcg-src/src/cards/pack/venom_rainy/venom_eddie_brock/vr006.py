from . import *

# Tendril Explosion — custom « Rainy » (cout X)
# Hero Action: Deal X damage to each enemy.

def GetAbilities() -> Sequence['Ability']:

    def tendril_explosion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        x = effect.GetCostX()
        if x <= 0:
            return
        ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
        if ennemis:
            this.DealDamage(ennemis, x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tendril_explosion
        ).SetPlay(hero_form_only=True),
    ]
