from . import *

# Blackheart. Sbire DEMON ELITE, Guard + Patrol + Steady (desc, natifs). « [star] Boost : If this activation is an attack, this attack gains
# overkill, piercing, and ranged. »
# Cartes de reference : 27081 Tooth and Nail (`would_atk_message.GainPiercing`, `WhenCardBecomeBoost(..., during_attack=True)`), 27169 Unstable
# Sentience (`GainOverKill`), `GainRanged` (sender_damage.py:402). ⚠ « this activation is an attack » : `during_attack=True` (un complot ne
# declenche rien).


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        atk = message.would_atk_message
        atk.GainOverKill(effect)
        atk.GainPiercing(effect)
        atk.GainRanged(effect)

    return [AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True)]
