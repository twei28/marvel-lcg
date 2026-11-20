from . import *

# Dupe (Jamie Madrox) : ALLIE, cout 2. DUPLICATE. X-FACTOR. THW 1☆ / ATQ 1☆, PV 3. Quatre cartes distinctes (ressource imprimee differente).
# Separate Lives – Action: Exhaust this card → generate its printed resource to pay for an identity-specific card.
#
# CARTE DE REFERENCE : `21006` (Energy Duplication) : `CanGenerateResources(.., resources_fn=..)` + `FacesCounter.GetPrintedResources([face])` ; `ar003` : `card_class="IdentitySpecific"`.
# TEXTE CONTRE CODE : « its PRINTED resource » = la ressource imprimee de CE Dupe (physique / mentale / energie / polyvalente selon la carte). « an identity-specific card » : une carte
#  dont la classe est propre a l'identite (les cartes du set Multiple Man). Duplicate : trait sans effet. Chiffres : cout 2, THW 1, ATQ 1, PV 3.


def GetAbilities() -> Sequence['Ability']:
    return CapaciteSeparateLives()
