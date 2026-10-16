from . import *

# Street Phantoms — SBIRE nemesis, x3 (3/5, 4/5, 5/5 : meme card_id, les trois scans ne
# different que par le numero). PHANTOMS. SCH 1 / ATQ 1 / PV 1 / Boost 2.
# Toughness.
# When Revealed: Cloak Street Phantoms.
#
# Cartes de reference : `leonardo/tl016` Foot Soldiers — MEME effet (« When Revealed:
# Cloak <ce sbire> ») : `WhenThisRevealed(None, op)` + `Cloak(effect, this)`.
#
# ⚠ Mots-pieges :
#  - « Cloak STREET PHANTOMS » : la carte elle-meme, pas le vilain ni les autres sbires ;
#  - Toughness : BASE AUTOMATIQUE (`desc`) ;
#  - trois exemplaires du MEME card_id dans `nemesis_set`.


def GetAbilities() -> Sequence['Ability']:

    def street_phantoms(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Cloak(effect, this)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            street_phantoms,
        ),
    ]
