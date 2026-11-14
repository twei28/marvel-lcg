from . import *

# Smashing Pumpkins — TRAITRISE x2. Boost ★.
# When Revealed : Resolve the "Pumpkin Bomb" ability three times.
# ★ Boost : Resolve the "Pumpkin Bomb" ability.
#
# Cartes de reference : voir __init__.py (`ResoudrePumpkinBomb`) ; `WhenCardBecomeBoost("This", ...)`.
# ⚠ Boost « ★ » : une seule Pumpkin Bomb, pour le joueur qui subit l'activation ; desc.Boost `0**`.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ResoudrePumpkinBomb(effect, message.GetToPlayer(), 3)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        ResoudrePumpkinBomb(effect, message.GetToPlayer(), 1)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
