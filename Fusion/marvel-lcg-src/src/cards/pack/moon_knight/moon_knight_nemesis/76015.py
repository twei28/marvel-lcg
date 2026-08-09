from . import *

# Cull the Weak — custom « DesignHacker » (némésis de Moon Knight)
# When Revealed: Discard the ally you control with the least remaining hit
#   points. If you cannot, take 2 damage instead.


def GetAbilities() -> Sequence['Ability']:

    def cull_the_weak(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        allies = [
            x for x in Worlds.FindCardsOnField(effect, card_type=Ally)
            if x.GetControlByPlayer() == player
        ]
        if allies:
            plus_faible = min(allies, key=lambda x: x.health)
            Faces.DiscardAll([plus_faible], effect)
        else:
            identite = player.GetIdentity()
            if identite is not None:
                this.DealDamage([identite], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            cull_the_weak
        ),
    ]
