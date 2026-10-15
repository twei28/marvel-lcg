from . import *

# * Paibok (II) — MECHANT, stade 2 (Paibok). SKRULL. PV 16[per_hero], SCH 2, ATK 2.
# Toughness.
# While the number of POWER SKRULL cards attached to Paibok is equal to or less
#   than the number of mastery counters on him, POWER SKRULL cards cannot be
#   discarded.
# When Revealed: Search the encounter deck and discard pile for a POWER SKRULL
#   card and reveal it.
#
# Cartes de reference : `sk141` (regle des pouvoirs) ; `01136` Ultron
# (`Search.EncounterCard(include_discard_pile=True)` + `face.Reveal`) via le helper
# `ChercherEtReveler`. Meme module que sk143 (stade III, memes textes).
#
# ⚠ Mots-pieges : « Search the encounter deck AND DISCARD PILE » ; « A POWER SKRULL
# card » (le joueur choisit parmi celles du deck et de la defausse) ; « reveal »
# (l'attachement entre en jeu et s'attache a Paibok par son propre « Attach to »).
# Rien a trouver : la fouille ne fait rien (le deck est melange, comportement natif).


def GetAbilities() -> Sequence['Ability']:

    def pouvoir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChercherEtReveler(effect, message.GetToPlayer(), trait=TRAIT_POUVOIR, card_type=Attachment)

    return [
        *RegleDesPouvoirs(),
        AbilityFactory.WhenThisRevealed(None, pouvoir),
    ]
