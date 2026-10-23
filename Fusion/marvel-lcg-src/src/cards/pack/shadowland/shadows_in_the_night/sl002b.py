from . import *

# Fortress Lockdown (2B) — MANIGANCE PRINCIPALE, stade 2. Menace 8 par joueur, depart 2 par joueur, escalade +1 par joueur.
# Memes regles que sl001b (le vilain se retourne a la place d'etre vaincu face A) ; vaincu face B = victoire.
# If this stage is completed, the players lose the game.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesComplotAvecVilainRetourne(plus_sch_expert=True, plus_pv_expert=True),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
