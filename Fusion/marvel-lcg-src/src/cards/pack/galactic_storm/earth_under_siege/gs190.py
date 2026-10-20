from . import *

# Veranke (I) — MECHANT, stade 1. SKRULL. SCH 2, ATK 1, PV 6.
# [star] Players cannot defend against Veranke's attacks.
#
# Cartes de reference :
#  - « Players cannot defend against X's attacks » : `AbilityFactory.UnitCannotDefend(Unit2, "This",
#    cannot_trigger_defense_ability=True)` (modele sk232 Enemy Adaptation / ip034 Molecule Man) ; helper
#    partage `CapacitesVeranke` (earth_under_siege/__init__.py), reutilise par gs191.
#
# ⚠ Mots-pieges : « PLAYERS cannot defend » = aucun personnage, identite ou allie (Unit2 generique, pas
# seulement le joueur vise) ; seules les attaques DE VERANKE sont concernees (un sbire de son ensemble
# reste defendable normalement).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesVeranke()
