from . import *

# Foot Soldiers — SBIRE nemesis, x3 (3/5, 4/5, 5/5 : meme card_id, les trois
# scans ne different que par le numero de collection). FOOT CLAN. NINJA.
# MNG 1 / ATQ 1 / PV 1 / Boost 1.
# When Revealed: Cloak Foot Soldiers.
#
# Cartes de reference :
#  - `WhenThisRevealed(None, op)` : `an011` / `ho014` ;
#  - le seul effet est `Cloak(...)` : STUB sans effet, voir tl015 et
#    `leonardo_nemesis/__init__.py` (TODO-QUESTION Q1).
#
# Mots-pieges :
#  - « Cloak FOOT SOLDIERS » : la carte elle-meme (pas le vilain) ;
#  - trois exemplaires du MEME card_id dans `nemesis_set` — aucune raison de
#    separer les ids (aucune difference imprimee).


def GetAbilities() -> Sequence['Ability']:

    def foot_soldiers(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Cloak(effect, this)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            foot_soldiers,
        ),
    ]
