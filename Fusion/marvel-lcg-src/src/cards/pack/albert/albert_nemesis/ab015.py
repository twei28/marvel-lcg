from . import *

# * Weapon X — custom « Kajislav » (sbire némésis d'Albert)
# Quickstrike (desc).
# When Revealed: Discard 1 random card from your hand.

def GetAbilities() -> Sequence['Ability']:

    def weapon_x_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetToPlayer()
        player.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            weapon_x_revealed
        ),
    ]
