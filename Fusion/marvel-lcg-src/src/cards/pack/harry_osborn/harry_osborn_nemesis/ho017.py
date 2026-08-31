from . import *

# Refrain From Argument — complot annexe nemesis. Menace 2. Hinder 1[per_hero].
# Crisis 1. Boost 0 (etoile seule).
# Hinder 1 (place 1 menace par joueur ici a l'arrivee).
# (Crisis Icon: Threat cannot be removed from the main scheme.)
# [star] Boost: Reveal this card if there is no side scheme in play.
#
# Cartes de reference :
#  - Hinder et Crisis : bases automatiques du moteur, lues dans `desc`
#    (fiches mots-cles/hinder.md — le `1*` note « par joueur » — et
#    crisis.md). RIEN a coder pour elles ;
#  - le boost conditionnel : 16140 Sound the Alarms (`WhenCardBecomeBoost
#    ("This", RevealThisCard)`), la condition « sans complot annexe en jeu »
#    passant par le parametre `conditions` de la fabrique (boost.py:15).
#
# ⚠ « if there is NO side scheme in play » : ho014 et les complots annexes du
# scenario comptent — des qu'un seul est en jeu, le boost reste muet et la
# carte est defaussee normalement apres l'activation.

def GetAbilities() -> Sequence['Ability']:

    def aucun_complot_annexe(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        Unused(message)
        return len(Worlds.FindCardsOnField(effect, card_type=SchemeSide2)) == 0

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
            conditions=[aucun_complot_annexe],
        ),
    ]
