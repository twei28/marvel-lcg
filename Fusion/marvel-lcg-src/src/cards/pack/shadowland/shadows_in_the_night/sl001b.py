from . import *

# A Barricade of Blades (1B) — MANIGANCE PRINCIPALE, stade 1. Menace 7 par joueur, depart 2 par joueur, escalade +1 par joueur.
# In expert mode, the villain gets +1 SCH and +3[per_hero] hit points.
# Forced Interrupt : When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player
#   1 facedown encounter card.
# If the villain is defeated on side B, the players win the game.
#
# Cartes de reference : punisher_mcdc_2026/the_big_apple/pu001b (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `ResetHealth`), web_of_deceit/the_lizard/wd057 (retourner
# le vilain PUIS remettre ses PV : les PV sont portes par la carte), next_evol/on_the_run/40104b (`GiveKeywordToInPlayWhenApplyThis(Villain, ..., expert_mode_only=True)`).
# ⚠ Mots-pieges :
#  - « on side A » : seulement la face A ; vaincu face B, le vilain meurt normalement et les joueurs gagnent (rien a coder : il n'y a pas de stade suivant) ;
#  - « reset its hit points » : APRES le retournement (les PV de la face B), sinon la carte revient deja vaincue ;
#  - « change the villain's position » : INCONDITIONNEL (pas la restriction « if it has not changed this phase »), et il compte comme un changement de cette phase ;
#  - « each player 1 facedown encounter card » : une carte rencontre donnee face cachee a CHAQUE joueur ;
#  - expert : +1 SCH et +3 PV par heros, sur le vilain actif.


def GetAbilities() -> Sequence['Ability']:
    return AbilitesComplotAvecVilainRetourne(plus_sch_expert=True, plus_pv_expert=True)
