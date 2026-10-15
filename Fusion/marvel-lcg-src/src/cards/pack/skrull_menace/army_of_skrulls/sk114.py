from . import *

# Skrull Soldier — SBIRE x3 (Army of Skrulls). SKRULL. SOLDIER. SCH 2, ATK 2,
# 4 PV, ★ + 1 boost.
# When Revealed: Place 2 threat on each side scheme in play.
# ★ Boost: Discard the top 2 cards of your deck.
#
# Cartes de reference : **`ho015`** (`PlaceThreatOnSchemes("EachSideScheme", 2, effect)`) ;
# **`46028`** (`player.DiscardDeckTopCards(2, effect)`).
# ⚠ « EACH side scheme » (annexes seulement, pas le principal) ; « YOUR deck ».


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        effect.this.CastTo(Minion).PlaceThreatOnSchemes("EachSideScheme", 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().DiscardDeckTopCards(2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
