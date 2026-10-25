from . import *

# Predator's Pursuit (3B) — COMPLOT PRINCIPAL, stade 3. Seuil 8[per_hero], escalade +1[per_hero], depart 1[per_hero], Hazard.
# Predator Warlord is the active villain.
# When Revealed: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and reveals it.
# If this stage is completed, the players lose the game.
#
# Cartes de reference :
#  - « is the active villain » : `Villains.SetActive` a la revelation (seul mechant restant de toute facon) ;
#  - « searches ... and reveals it » : `Search.EncounterCard(.., include_discard_pile=True)` + `Reveal` (le « When Revealed » du sbire part) ;
#  - « the players lose » : `WhenMainSchemeStageWouldBeCompleted` + `Worlds.SetGameOver(False)` (27102b) ; sans lui le moteur
#    passerait au complot suivant encore dans le deck ;
#  - Hazard : `desc.Hazard`, natif (fiche hazard.md).
#
# ⚠ Mots-pieges : « EACH player » : un sbire par joueur ; « reveals » (pas « puts into play ») : son « When Revealed » part.


def GetAbilities() -> Sequence['Ability']:
    return StadeDuSurvivant('Predator Warlord', 'YAUTJA')
