from . import *

# Big Apple Gang War! — ENVIRONNEMENT de campagne (combat 1, p263). Setup. Permanent.
# Battle Setup : Scenario The Big Apple ; sans Uptown ; chaque joueur a besoin d'un pion joueur ; sets Cops et Tracksuit Mafia (FNE).
# Victory : Flip this card and put Seized Tech Crates into play for battles 2 and 3.
#
# Cartes de reference : fne/typhoid_mary/60113a (« Permanent, Setup : bases desc », aucun script), pu005 The City (le pion joueur et
# la position dans la ville), skrull_menace/campaign.py (releve du carnet a la victoire, `WriteCampaignLogAtGameOver`).
# ⚠ Rien a coder sur la carte elle-meme : « Setup. Permanent. » sont des mots-cles lus dans `desc` (fiches setup.md et permanent.md) ;
# le Battle Setup est porte par le scenario (`data/scenarios/the_big_apple*.json` : modular_sets cops + tracksuit_mafia, pas d'Uptown) et
# par The City (pu005, le pion joueur) ; « Victory : flip... » = le RELEVE du carnet (`punisher_mcdc_2026/campaign.py` : « Big Apple Gang
# War! » = Flipped, « Seized Tech Crates » = 1), ecrit une seule fois pour toute la partie. L'entree en jeu est faite par
# `CampaignSetup()` du complot 1A (pu001a), car l'environnement n'est dans aucun deck.

def GetAbilities() -> Sequence['Ability']:
    return []
