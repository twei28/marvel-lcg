from . import *

# Mole Man (I) — MECHANT, stade 1. GENIUS. SUBTERRANEAN. SCH 2, ATK 1, PV 6.
# [star] Forced Response: After Mole Man attacks you, shuffle a SUBTERRANEAN minion from the encounter
#   discard pile into the encounter deck.
#
# Cartes de reference :
#  - « After Mole Man attacks you, shuffle a SUBTERRANEAN minion from the encounter discard pile into the
#    encounter deck » : `AfterEnemyActivatesAgainstYou` (filtre sur `atk_message` pour ne garder que
#    l'ATTAQUE) + `Worlds.GetEncounterDiscardPileCards` + `Faces.ShuffleAllTo` ; helper partage
#    `CapacitesMoleMan` (earth_under_siege/__init__.py), reutilise par gs187.
#
# ⚠ Mots-pieges : « attacks YOU » = l'attaque seulement (une manigance de Mole Man ne declenche rien) ; si
# aucun sbire SUBTERRANEAN n'est dans la defausse de rencontre, rien ne se passe (pas de « if you cannot »
# imprime).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesMoleMan()
