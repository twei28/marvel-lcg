from . import *

# "Who Do You Trust?" — ENVIRONNEMENT. Porte les jetons de SOUPCON.
# Forced Interrupt: When any amount of threat is placed on the main scheme, remove an equal amount of suspicion
#   counters from here.
# Forced Interrupt: When any amount of threat is removed from the main scheme, place an equal amount of suspicion
#   counters here.
#
# Cartes de reference : **`WhenSchemeWouldPlaceThreat` / `WhenSchemeWouldRemoveThreat`** (factory/scheme.py ;
# `message.value`) ; compteur maison 'suspicion' (card_face.py, comme 'mastery' de Paibok) ;
# **`skrull_empire/sk086`** (un environnement de scenario qui reagit a un message).
#
# ⚠ Mots-pieges : « placed ON THE MAIN SCHEME » (pas un complot annexe) ; « an EQUAL amount » : le jeton retire
# ne peut pas depasser ceux qui sont la ; pour le retrait de menace, le montant est borne par la menace reellement
# presente (le moteur ne retire pas plus que ce qui est la) ; ce sont deux Interruptions forcees (AVANT l'evenement).


def GetAbilities() -> Sequence['Ability']:

    def menace_posee(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        RetirerSoupcons(effect, min(message.value, NbSoupcons(effect)))

    def menace_retiree(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        PoserSoupcons(effect, min(message.value, message.trigger.threat))

    return [
        AbilityFactory.WhenSchemeWouldPlaceThreat(AbilityType.ForcedInterrupt, MainScheme, menace_posee),
        AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.ForcedInterrupt, MainScheme, menace_retiree),
    ]
