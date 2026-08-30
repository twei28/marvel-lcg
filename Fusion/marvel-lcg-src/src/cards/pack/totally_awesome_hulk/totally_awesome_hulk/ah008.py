from . import *

# Calculated Strike — custom « DesignHacker »
# Hero Action (attack/thwart): Remove 2 threat from a scheme, then deal 3
#   damage to the villain. If you paid for this card using only [wild]
#   resources, remove 2 additional threat.
#
# CORRECTIF (30/08/2026) : le module ne posait que le label 'thwart' alors que la
# carte est imprimee « (attack/thwart) » et inflige 3 degats au vilain. Le label
# 'attack' est ce qui livre la capacite au statut Sonne
# (`cards/pack/status/stunned.py`) : un Amadeus Cho Sonne jouait la carte, retirait
# sa menace, frappait le vilain, et GARDAIT son statut.


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
        .SetLabel('attack', 'thwart')
        .SetTarget(Scheme2),
    ]
