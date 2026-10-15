from . import *

# * Paibok (III) — MECHANT, stade 3 (Paibok). SKRULL. PV 20[per_hero], SCH 3, ATK 3.
# Toughness.
# While the number of POWER SKRULL cards attached to Paibok is equal to or less
#   than the number of mastery counters on him, POWER SKRULL cards cannot be
#   discarded.
# When Revealed: Search the encounter deck and discard pile for a POWER SKRULL
#   card and reveal it.
#
# Cartes de reference : `sk141` (regle des pouvoirs) et `sk142` (texte IDENTIQUE, memes
# fabriques : `RegleDesPouvoirs()` + `ChercherEtReveler`). Seules les stats changent (desc).
#
# ⚠ Mots-pieges : voir sk142. Le stade III n'existe qu'en mode expert (villain: sk142, sk143).


def GetAbilities() -> Sequence['Ability']:

    def pouvoir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChercherEtReveler(effect, message.GetToPlayer(), trait=TRAIT_POUVOIR, card_type=Attachment)

    return [
        *RegleDesPouvoirs(),
        AbilityFactory.WhenThisRevealed(None, pouvoir),
    ]
