from . import *

# * X-S Sentinel I — sbire. EARTH-6160. SENTINEL. PV 8, ATK 3★, SCH 1, boost ★ + 2.
# [star] X-S Sentinel I's attack gains ranged, overkill and piercing.
# [star] Boost: This attack gains ranged, overkill and piercing.
#
# Cartes de reference : `ho016` Bullseye (« [star] Bullseye's attack gains piercing and overkill » =
# `UnitAttackGainKeyword("This", piercing=True, overkill=True)`) ; `50107b` M.O.D.O.K. (`ranged=True`, fiche
# mots-cles/ranged.md) ; `an013` (« [star] Boost: This attack gains overkill » : `message.would_atk_message`, `getattr(..., None)`
# car la carte peut etre revelee hors attaque ; `GainOverKill/GainPiercing`, `GainRanged` du message d'attaque).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainRanged(effect)
            attaque.GainOverKill(effect)
            attaque.GainPiercing(effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            ranged=True,
            overkill=True,
            piercing=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
