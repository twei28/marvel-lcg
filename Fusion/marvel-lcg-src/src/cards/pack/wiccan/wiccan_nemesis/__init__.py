from cards.pack import *
# Les cartes du set nemesis ont leur PROPRE `from . import *` (ce fichier),
# distinct de celui du pack heros (wiccan/wiccan/__init__.py) : sans cet
# import explicite, toute aide partagee part en NameError (lecon iron_lad).
from cards.pack.wiccan.wiccan import (
    NOM_WICCAN, NOM_BILLY, NOM_MORIDUN, NOM_NEW_VESSEL, NOM_DEMIURGE,
    MoridunEnJeu, NewVesselEnJeu,
)

# ===========================================================================
# Set nemesis de WICCAN — contenu custom de CptScorp.
#
# Composition du `nemesis_set` (data/nemesis/wiccan_nemesis.json) : wc019a
# New Vessel (manigance annexe, RECTO), wc020 Moridun, wc021 et wc022
# Inescapable Horror (deux exemplaires physiques de la meme trahison, meme
# choix de design qu'il021/il022 chez le meme auteur), wc023 Master Magus
# Returns — CINQ cartes, comme tout set nemesis officiel.
#
# wc019b The Demiurge est le VERSO de wc019a : elle n'est jamais tiree, on ne
# l'atteint qu'en retournant New Vessel une fois accomplie. Elle doit donc
# etre declaree AVEC son recto (« wc019a,wc019b ») partout ou la carte est
# listee, sans quoi `Card.Flip` ne trouve aucune face arriere et se contente
# de coucher la carte face cachee — elle QUITTE le jeu au lieu de devenir
# l'environnement (lecon Dazzler, verifiee ici par le cas `wc019a ... flip`).
#
# ECART D'AUTEUR ASSUME : wc020 Moridun est typee **Attachment** dans
# cards.json alors que son texte imprime se termine par « (Wiccan's Nemesis
# Minion.) ». Le TYPE IMPRIME fait foi — c'est bien une carte a attacher a
# l'identite, sans PV ni ATK ; la parenthese est une coquille de l'auteur.
# Non corrigee, documentee.
# ===========================================================================
