from . import *

# Earn the People's Favor (1B) — MANIGANCE PRINCIPALE, stade 1. Seuil 3[per_hero], escalade +1[per_hero][star],
# depart 0.
# When Revealed: Place 1[per_hero] threat on Imprisoned on Chandilar.
# [star] Forced Response: After resolving step one of the villain phase, place 2 threat on Imprisoned on
#   Chandilar for each player in alter-ego form.
#
# Cartes de reference :
#  - When Revealed : `WhenThisRevealed(None)` + `PlaceThreatOnSchemes([prison], "1*")` (modele 50134), helper
#    `MenaceSurLaPrisonParJoueur()`.
#  - « After resolving step one of the villain phase » : `AfterResolveVillainPhaseStep(ForcedResponse, 1)`,
#    modele OFFICIEL 04096b Hunting Down Heroes, helper `ApresEtapeUn()`.
#  - l'etoile de l'escalade renvoie a la Reponse forcee (convention Skrull Menace) : EscalationThreat "1*".
#
# ⚠ Mots-pieges : « 2 threat ... FOR EACH PLAYER in alter-ego form » (2 x nombre de joueurs en alter ego, 0 si
# tous sont en heros) ; la menace va sur la PRISON, pas sur la manigance principale.


def GetAbilities() -> Sequence['Ability']:
    return [MenaceSurLaPrisonParJoueur(), ApresEtapeUn()]
