from . import *

# Calculated Strike — custom « DesignHacker »
# Hero Action (attack/thwart): Remove 2 threat from a scheme, then deal 3
#   damage to the villain. If you paid for this card using only [wild]
#   resources, remove 2 additional threat.


def GetAbilities() -> Sequence['Ability']:

    def calculated_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        value = 2
        if PaidOnlyWithWild(effect):
            value += 2

        this.RemoveThreatFromSchemes(effect.targets, value, effect)

        villains = Worlds.FindCardsOnField(effect, card_type=Villain)
        villains = [x for x in villains if not x.IsDefeated()]
        if villains:
            this.DealDamage(villains, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            calculated_strike,
        ).SetPlay(hero_form_only=True)
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
