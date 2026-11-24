from . import *

# Predator's Pursuit (3A) — COMPLOT PRINCIPAL, stade 3 (atteint quand Alien Queen est vaincue).
# When Revealed: Discard cards from the top of the encounter deck until a [[WEAPON]] attachment is discarded. Reveal it.
#
# Cartes de reference : 01192 Masterplan (`Worlds.DiscardEncounterCardsUntil(.., trait=, card_type=Attachment)` puis `Reveal`).
#
# ⚠ Mots-pieges : un ATTACHEMENT WEAPON (pas un sbire) ; aucun dans le deck -> rien n'est revele.


def GetAbilities() -> Sequence['Ability']:
    return StadeQuiFouille('WEAPON')
