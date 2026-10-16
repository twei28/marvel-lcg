from . import *

# * Rocksteady — SBIRE UNIQUE (Foot Goon Squad). BRUTE. FOOT CLAN. RHINOCEROS.
# MNG 0 / ATQ 2* / PV 4, 1 icone de boost + etoile. Steady. Quickstrike.
# [star] Rocksteady's attacks gain overkill.
# [star] Boost: If this activation is an attack, it gains overkill. Otherwise,
#   deal this card to the first player as a facedown encounter card.
#
# Cartes de reference : `ts201` (meme montage, overkill au lieu de piercing) ;
# `fne 60149` Rhino (`UnitAttackGainKeyword("This", overkill=True)`) ; Steady et
# Quickstrike lus dans `desc`.
#
# ⚠ HOMONYME : sbire `ts205`, distinct du vilain Rocksteady du pack `tk`.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if EstUneAttaque(message):
            message.would_atk_message.GainOverKill(effect)
        else:
            FaceCacheeAuPremierJoueur(effect, effect.this)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
