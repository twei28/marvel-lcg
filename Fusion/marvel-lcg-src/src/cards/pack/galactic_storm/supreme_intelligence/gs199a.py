from . import *

# The Endless Mind (2A) — COMPLOT PRINCIPAL (Supreme Intelligence).
# When Revealed: Shuffle each set aside STARFORCE minion into the encounter deck.
#
# Cartes de reference :
#  - **`falcon/53033`** Adder-tisement : `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)` pour « shuffle
#    each <trait> minion from <zone> into the encounter deck » ; ici la zone est la mise de cote
#    (`Worlds.GetSetAsideAreaCards`, modele `aos/50104b`).
#  - `WhenThisRevealed(None, op)` sur une face A de complot principal : `mut_gen/32125b`.
#
# ⚠ Mots-pieges : « EACH set aside STARFORCE minion » (tous, Supremor compris dans la lecture Q1) ; « into
# the ENCOUNTER deck » (melange) ; aucun sbire mis de cote : rien.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        sbires = SbiresStarforceMisDeCote(effect)
        if sbires:
            Faces.ShuffleAllTo(sbires, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
