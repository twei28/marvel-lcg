from . import *

# Skrull Commander — SBIRE x2 (Army of Skrulls). SKRULL. SOLDIER. SCH 2, ATK 2,
# 5 PV, ★ + 1 boost.
# Each other SKRULL minion gets +1 ATK.
# ★ Boost: If this activation is an attack, this card gets +2 boost icons for
#   this activation.
#
# Cartes de reference : `GiveKeywordToInPlayWhenApplyThis(..., not_include_this=True)` ;
# **`60075`** (`during_attack=True`) ; **`46028`** (`GainBoostIcon`).
# ⚠ « each OTHER Skrull MINION » (pas le mechant, pas lui-meme).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(2, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), attack=1, not_include_this=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
