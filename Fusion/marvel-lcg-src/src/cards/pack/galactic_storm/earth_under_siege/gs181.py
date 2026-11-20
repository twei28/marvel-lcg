from . import *

# Doctor Minerva (I) — MECHANT, stade 1. KREE. SCIENTIST. SCH 1, ATK 1, PV 6.
# [star] Forces Response: After Doctor Minerva schemes against you, deal yourself a facedown encounter
#   card.
#
# Cartes de reference :
#  - « After Doctor Minerva schemes against you, deal yourself a facedown encounter card » :
#    `AbilityFactory.AfterUnitSchemeEnd` + `message.GetAgainstPlayer()` + `Player.DealEncounterCards`
#    (modele ar012 Ares) ; helper partage `CapacitesDoctorMinerva` (earth_under_siege/__init__.py),
#    reutilise par gs182.
#
# ⚠ Mots-pieges : texte imprime « Forces Response » (sans « d », faute d'impression confirmee sur le scan,
# transcrite telle quelle) : codee comme un Forced Response, lecture evidente ; « schemes AGAINST YOU » =
# le joueur vise par LA manigance, pas forcement celui qui a revele une carte qui l'a declenchee.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesDoctorMinerva()
