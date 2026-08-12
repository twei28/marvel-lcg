from . import *

# Wild Lunge — custom « DesignHacker »
# You can only spend [wild] resources to pay for this card.
#   (Encodé par le coût coloré "G" dans cards.json, comme Crushing Blow 10002.)
# Hero Action (attack): Deal 4 damage to an enemy.


def GetAbilities() -> Sequence['Ability']:

    def wild_lunge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wild_lunge,
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
