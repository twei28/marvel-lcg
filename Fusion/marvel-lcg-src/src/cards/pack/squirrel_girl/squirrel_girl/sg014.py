from . import *

# Squirrel Swarm
# Hero Action (attack): Deal 3 damage to an enemy. If you spent a Squirrel to
#   play this card, deal 3 additional damage to that enemy.

def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        degats = 6 if ADepenseUnEcureuil(effect) else 3
        this.DealDamage(effect.targets, degats, effect)

    return [
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, frapper)
            .SetPlay()
            .SetLabel("attack")
            .SetTarget(Enemy)),
    ]
