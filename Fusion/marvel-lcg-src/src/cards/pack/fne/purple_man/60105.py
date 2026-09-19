from . import *

# "Fight." (obligation, Uses 3 command) — Forced Action: Exhaust this card and
# remove 1 command counter from it -> deal 2 damage to a hero or ally.

def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        this.DealDamage(effect.targets, 2, effect)

    return [
        ObligationCommandee("Fight.", frapper)[0].SetTarget(CardFinder(card_type=Hero|Ally)),
    ]
