from . import *

# Memory From The Future — OBLIGATION, boost 2. « Give to the Rachel Summers player. »
# You get -1 hand size.
# Alter-Ego Action: Exhaust Rachel Summers -> discard this obligation and end this turn.
#
# CARTES DE REFERENCE : `sf010` Shame et `st005b` (`GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)`),
# `PlayerActionToDiscardThis(.., ex_operation=fn)` + `CostFunc.Exhaust("YourIdentity")` (`32150`). « End this turn » : MOTEUR
# (`CORRECTIF`, `EventManager`) — la carte pose le drapeau `RM_FIN_DE_TOUR`, la boucle d'actions du tour s'arrete comme si
# le joueur avait fini son tour.
#
# MOTS-PIEGES : `effect.GetInitiator()` d'une capacite d'Action de joueur est le JOUEUR (jamais le mechant d'une revelation).
def GetAbilities() -> Sequence['Ability']:
    def finir_le_tour(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        effect.GetInitiator().flag.Set("RM_FIN_DE_TOUR", 1)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            hand_size=-1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            ex_operation=finir_le_tour,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
