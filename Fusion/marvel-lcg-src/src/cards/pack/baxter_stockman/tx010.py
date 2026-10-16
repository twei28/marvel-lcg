from . import *

# Robotics Facility — MANIGANCE ANNEXE (Baxter's Lab 18/22, x3). 4 menaces, 1 boost.
# Hinder 1[per_hero]. Icones : Acceleration, Crisis (a verifier par decoupe, voir baxter-phase-a.md).
#
# AUCUN SCRIPT : Hinder, Acceleration, Crisis et Boost sont des bases automatiques lues dans `desc`
# (fiches mots-cles/hinder.md, acceleration.md, crisis.md). Le module existe pour porter le commentaire
# et la ligne de preuve ; `GetAbilities` est volontairement vide.
#
# ⚠ « 4 » imprime SANS icone de joueur : menace de depart FIXE (`StartingThreat "4"`), a la difference de
# Mad Lab (2 par joueur). Le Hinder 1 par joueur s'AJOUTE a l'entree en jeu.


def GetAbilities() -> Sequence['Ability']:
    return []
