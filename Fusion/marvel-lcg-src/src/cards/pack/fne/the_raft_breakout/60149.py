from . import *

# * Rhino (BRUTE, ELITE, PRISONER) — Toughness, Villainous : bases.
# [star] Rhino's attacks gain overkill.
# [star] Boost: Give the activating enemy a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
