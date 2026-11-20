from . import *

# Destroyer (I) — MECHANT, stade 1. ASGARD. SCH 1, ATK 2, PV 6.
# [star] Excess damage dealt by Destroyer's attacks is placed as threat on the main scheme.
#
# Cartes de reference :
#  - « excess damage ... placed as threat on the main scheme » : `Message.AfterUnitAttackUnit.excess_damage`
#    (sender_damage.py) + `MainScheme.PlaceThreatOnSchemes` (modele gs119 Majestrix's Verdict pour l'appel) ;
#    helper partage `ExcesVersMenaceSurManigancePrincipale` (earth_under_siege/__init__.py), reutilise par
#    gs179/gs180.
#
# ⚠ Mots-pieges : « Destroyer's attacks » = toutes ses attaques, contre n'importe quel personnage (pas
# seulement « against you ») ; l'exces se lit APRES resolution de l'attaque (`AfterUnitAttackUnit`), pas au
# moment de la declaration.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDestroyer()
