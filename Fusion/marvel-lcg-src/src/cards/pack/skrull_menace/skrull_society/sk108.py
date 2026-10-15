from . import *

# Skrull Spy — SBIRE x2 (Skrull Society). SKRULL. SPY. SCH 2, ATK 1, 4 PV, ★.
# When Revealed: Discard 1 random card from your hand.
# ★ Boost: Discard 1 random card from your hand.
#
# Carte de reference : **`11044`** (`player.DiscardRandomHandCards(1, effect)`).
# ⚠ « RANDOM » ; « YOUR hand » = le joueur qui revele / qui est active.


def GetAbilities() -> Sequence['Ability']:

    def defausse(effect: 'Effect', message: 'Message.WhenCardRevealed|Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, defausse),
        AbilityFactory.WhenCardBecomeBoost("This", defausse),
    ]
