from . import *

# The Planet Cleaver — COMPLOT ANNEXE. Seuil 1 (FIXE), 3 icones de boost.
#
# Hinder 2[per_hero].
# Forced Interrupt: When facedown encounter cards are dealt to players during
#   the villain phase, deal each player 1 additional facedown encounter card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Hinder` (mots-cles/hinder.md) : BASE AUTOMATIQUE, `desc.Hinder = "2*"`.
#   Le moteur pose la menace sur CETTE carte a son entree en jeu. Aucun script.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « deal each player 1 ADDITIONAL facedown encounter card » : c'est l'icone
#   HASARD du moteur (`desc.Hazard`, mots-cles/hazard.md), qui fait
#   exactement cela — mais elle est une base automatique de la carte QUI LA
#   PORTE, appliquee quand cette carte est REVELEE, pas un effet continu tant
#   qu'elle est en jeu. Le texte, lui, est une Interruption Obligatoire qui
#   dure tant que le complot est sur la table : on le code donc, par
#   `ThisGainKeyword(hazard=1)`, la meme forme que 57005b emploie pour un
#   Hinder calcule.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « WHEN facedown encounter cards ARE DEALT ... during the VILLAIN PHASE » ->
#   au moment de la distribution de la phase du vilain, pas a toute
#   distribution (une carte qui en donne une hors phase n'est pas concernee).
# « 1 ADDITIONAL ... to EACH PLAYER » -> une de plus par joueur : c'est
#   exactement la definition de l'icone Hasard.
# « Seuil 1, FIXE » -> aucune icone joueur sur le chiffre, contrairement au
#   Hinder qui, lui, porte l'icone.


def GetAbilities() -> Sequence['Ability']:

    return [
        # L'icone Hasard est portee tant que ce complot est en jeu : le moteur
        # la lit au moment de la distribution de la phase du vilain.
        AbilityFactory.ThisGainKeyword(hazard=1),
    ]
