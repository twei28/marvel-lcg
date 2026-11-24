from . import *

# Sentry Awakens (1B) — MANIGANCE PRINCIPALE, stade 1 (Kree Sentry). Menace de depart 2, escalade +1, objectif 7, tous
# par joueur.
# [star] Forced Response: After resolving step one of the villain phase, deal 1 damage to each character for each copy
#   of Sentry's Grasp attached to it.
#
# Cartes de reference :
#  - « After resolving step one of the villain phase » : `AfterResolveVillainPhaseStep(ForcedResponse, 1, op)`, modele
#    gs117b (Majestrix) / OFFICIEL 04096b.
#  - « deal 1 damage to each character for each copy attached to it » : `DealDamage([personnage], n, effect)` (modele
#    54035), n = nombre de Poignes de CE personnage.
#  - valeurs : `desc.StartingThreat/EscalationThreat/TargetThreat` en « par joueur » (`*`), bases automatiques.
#
# ⚠ Mots-pieges : « EACH character » = identites, allies, sbires (Rick Jones compris), pas seulement les heros ;
# « FOR EACH copy attached to IT » : un personnage avec deux Poignes subit 2 degats, en UNE seule instance (lecture
# retenue : question Q3 de .planning/todos/2026-10-20-gs4-questions.md) ; « [star] » = capacite permanente, toujours
# active (convention du projet, fiche special.md).


def GetAbilities() -> Sequence['Ability']:

    def degats_des_poignes(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        DegatsDesPoignes(effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, degats_des_poignes),
    ]
