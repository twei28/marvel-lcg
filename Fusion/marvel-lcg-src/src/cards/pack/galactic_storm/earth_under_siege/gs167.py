from . import *

# Annihilus (II) — MECHANT, stade 2. NEGATIVE ZONE. SCH 2, ATK 2, PV 7. Toughness.
# [star] Forced Response: After Annihilus activates against you, discard cards from the top of your deck
#   until you discard an identity-specific card.
#
# Texte identique a gs166 (stade I) hors Toughness (native, desc.Toughness) : voir son gabarit pour les
# cartes de reference et les mots-pieges.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesAnnihilus()
