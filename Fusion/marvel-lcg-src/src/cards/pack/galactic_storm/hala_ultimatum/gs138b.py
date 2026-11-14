from . import *

# * Tanalth (I) — MECHANT, stade 1, face B (DISCOVERED). KREE. PV 15[per_hero]. SCH 2. ATK 2.
# [star] Forced Response: After Tanalth attacks and defeats a character, give her a tough status card. If she
#   already has a tough status card, give her a facedown boost card.
#
# Cartes de reference :
#  - « After X attacks and defeats a character, give her a tough status card. If ... already ... give her a
#    facedown boost card » : `AbilityFactory.AfterUnitAttackAndDefeatUnit` (modele 01051 Tigra, 01118 Sonic
#    Converter pour le type de cible « Character ») + `Faces.GiveStatus`/`Faces.GiveFacedownBoostCards`
#    (modele `skrull_menace/communs_modulaires.py`, `DonnerBoostAuMechant`) + `Faces.HasStatus` pour la
#    condition « already has ».
#  - Retournement HIDDEN -> DISCOVERED : `card.Flip` (gs142a), qui garde CE texte sur la MEME carte, les
#    attachements/statuts/degats restant du stade precedent (mots-cles/hidden.md).
#
# ⚠ Mots-pieges : « attacks AND DEFEATS » (il faut la defaite, pas un simple degat) ; « a character »
# (joueur OU allie, jamais un autre ennemi) ; « ALREADY has » = l'etat au moment de la Reponse, pas une
# nouvelle verification apres avoir donne le premier tenace.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesTanalth(1)
