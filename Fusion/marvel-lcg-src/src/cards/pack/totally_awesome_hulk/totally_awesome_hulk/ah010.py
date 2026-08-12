from . import *

# Irradiated Swipe — custom « DesignHacker »
# Hero Action (attack): Deal 5 damage to an enemy. If you paid for this card
#   using only [wild] resources, draw 2 cards.


def GetAbilities() -> Sequence['Ability']:

    def irradiated_swipe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 5, effect)

        if PaidOnlyWithWild(effect):
            effect.GetInitiator().DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            irradiated_swipe,
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
