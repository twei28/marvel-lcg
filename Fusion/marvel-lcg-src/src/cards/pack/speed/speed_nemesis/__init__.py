from cards.pack import *
# Les cartes du set nemesis ont leur PROPRE `from . import *` (ce fichier),
# distinct de celui du pack heros (speed/speed/__init__.py) : sans cet import
# explicite, toute aide partagee part en NameError (lecon iron_lad).
from cards.pack.speed.speed import (
    NOM_SPEED, NOM_THOMAS, NOM_COAT_OF_ARMS,
    COMPTEUR_EXPLOSIF,
)

# ===========================================================================
# Set nemesis de SPEED — contenu custom de CptScorp.
#
# Composition du `nemesis_set` (data/nemesis/speed_nemesis.json) : sd018 The
# Real Question (manigance annexe), sd019 Coat of Arms (le sbire nemesis),
# sd020 Inspirational Art et sd021 Magic Chains (deux attachements), sd022
# Conflicted Feelings — CINQ cartes, comme tout set nemesis officiel.
#
# ⚠ sd022 est une OBLIGATION qui appartient au SET NEMESIS : le scan la
# numerote « SPEED NEMESIS (5/5) » et elle porte une icone de bonus. Elle vit
# donc dans `nemesis_set` (melangee au deck rencontre avec le reste du set
# quand sd017 est revelee) et PAS dans la cle `obligations`, qui ne porte que
# sd017 No Outrunning This. Elle RESTE EN JEU une fois donnee, comme 28021
# Weight of the World (Nova), le seul autre precedent du depot.
#
# ⚠ sd017 No Outrunning This n'est PAS ici : c'est l'obligation du set
# `Speed` (numerotee « SPEED » sans mention nemesis sur le scan), donc dans
# speed/speed/sd017.py.
#
# COLLISION PERMANENT ENTRE sd018 ET sd020, tranchee dans sd020.py : tant que
# The Real Question est en jeu, les attachements gagnent Permanent, et la
# « Hero Action: ... discard this card » d'Inspirational Art devient
# INDISPONIBLE (condition sur la capacite), au lieu d'echouer en silence a la
# defausse. C'est l'intention de l'auteur : battre la manigance d'abord.
# ===========================================================================

# Seul `NOM_COAT_OF_ARMS` est employe aujourd'hui (sd021 et sd022) ; les autres
# sont importes pour rester disponibles au set, comme chez `wiccan_nemesis`.
# `EteindreHyperkineticFuel` n'est PAS importe : l'obligation qui l'appelle
# (sd017) appartient au set `Speed`, pas au set nemesis.
Unused(NOM_SPEED, NOM_THOMAS, NOM_COAT_OF_ARMS)
Unused(COMPTEUR_EXPLOSIF)
