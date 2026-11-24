from . import *

# Queen's Dominion (4A) — COMPLOT PRINCIPAL, stade 4 (atteint quand Predator Warlord est vaincu).
# When Revealed: Discard cards from the top of the encounter deck until a [[XENOMORPH]] attachment is discarded. Reveal it.
#
# Cartes de reference : 01192 Masterplan (`Worlds.DiscardEncounterCardsUntil(.., trait=, card_type=Attachment)` puis `Reveal`).
#
# ⚠ Mots-pieges : un ATTACHEMENT XENOMORPH (pas un sbire) ; aucun dans le deck -> rien n'est revele.


def GetAbilities() -> Sequence['Ability']:
    return StadeQuiFouille('XENOMORPH')
