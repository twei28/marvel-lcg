from . import *

# Self-Destruct Sequence (2B) — MANIGANCE PRINCIPALE, stade 2 (Kree Sentry). Menace de depart 1, escalade +1, objectif 10,
# tous par joueur.
# [star] Forced Response: After resolving step one of the villain phase, deal 1 damage to each character for each copy
#   of Sentry's Grasp attached to it.
# If this stage is completed, the players lose the game. (imprime « completes » : coquille, question Q1)
#
# Cartes de reference : meme Reponse forcee que gs079b (`DegatsDesPoignes`). « If this stage is completed, the players
# lose the game » : c'est la regle de base d'un DERNIER stade de complot principal (aucun stade suivant), le moteur
# fait perdre la partie sans carte (modele gs199b, qui n'a pas de script non plus) ; mesure par un cas.
#
# ⚠ Mots-pieges : voir gs079b ; la phrase en gras n'est PAS une capacite a coder, c'est la regle du dernier stade.


def GetAbilities() -> Sequence['Ability']:

    def degats_des_poignes(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        DegatsDesPoignes(effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, degats_des_poignes),
    ]
