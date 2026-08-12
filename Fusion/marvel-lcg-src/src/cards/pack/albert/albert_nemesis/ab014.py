from . import *

# * Patch — custom « Kajislav » (sbire némésis d'Albert)
# Retaliate 1 (desc).
# When Revealed: Deal 1 damage to each player.

def GetAbilities() -> Sequence['Ability']:

    def patch_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        identities = [
            player.GetIdentity()
            for player in list(effect.world.players)
            if not player.is_eliminated
        ]
        this.DealDamage(identities, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            patch_revealed
        ),
    ]
