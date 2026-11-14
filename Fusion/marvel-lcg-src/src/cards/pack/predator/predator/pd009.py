from . import *

# * Honor Hunt — MANIGANCE ANNEXE DE JOUEUR, cout 0, [wild]. Menace 5. Victory 0. Assault.
# While Honor Hunt is in the victory display, it gains "Action: Find a minion and put it into play engaged with you. Any player
#   may trigger this ability. (Limit once per round)."
#
# Cartes de reference :
#  - `40006` Technovirus Purge / `40018` Call for Backup : le type `PlayerSideScheme` (cout, `StartingThreat`, `Victory 0`),
#    SANS script ; `Assault` et `Victory` sont des bases automatiques (`desc`, fiches mots-cles/assault.md, victory.md).
#  - la capacite « en vitrine » : RECETTES §3bis, `rs009` Queen of Sogaria (pack red_sonja) : posee sur L'IDENTITE (pd001a ET
#    pd001b), `ActionHonorHuntEnVitrine` dans `__init__.py` ; `pu141` pour `AnyPlayerCanDoThis` + limite.
#
# ⚠ Mots-pieges :
#  - « Assault » : les contres de BASE contre cette manigance utilisent l'ATQ au lieu de la MNG (base automatique du moteur).
#  - « Victory 0 » : la manigance va a la vitrine quand elle est vaincue (`desc.Victory`).
#  - « While it is in the victory display, IT GAINS » : l'Action n'existe qu'en vitrine ; elle est portee par l'identite de
#    Predator (une carte en vitrine est hors jeu), declenchable par N'IMPORTE QUEL joueur, une fois par round.
#  - « Find a minion and put it into play engaged WITH YOU » : « you » = le joueur qui declenche, pas Predator.


def GetAbilities() -> Sequence['Ability']:
    return []
