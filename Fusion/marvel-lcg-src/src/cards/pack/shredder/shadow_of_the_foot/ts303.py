from . import *

# Foot Soldiers (x2) — SBIRE (Shadow of the Foot). FOOT CLAN. NINJA.
# MNG 1 / ATQ 1 / PV 1, 1 icone de boost.
# When Revealed: Cloak Foot Soldiers.
#
# Cartes de reference : `tl016` Foot Soldiers (nemesis de Leonardo : MEME texte,
# `Cloak(effect, this)`) ; `ts010`. ⚠ `ts303` n'est pas `tl016` : homonymes, ids
# differents.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, effect.this)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
