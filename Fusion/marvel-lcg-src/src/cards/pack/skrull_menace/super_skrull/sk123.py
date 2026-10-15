from . import *
from game.ability.factory.additional_cost import CostFunction

# Invisibility — ATTACHEMENT (paquet SUPERPOWER). SUPERPOWER. +1 SCH.
# Attach to Super-Skrull.
# As an additional cost to attack Super-Skrull, you must spend 1 resource of
#   any type.
#
# Cartes de reference :
#  - **`58027`** Brother vs. Brother (pack wonder_man) : « As an additional cost
#    to attack <cible> » = `WhenUnitWouldBeAttacked` + abandon de l'attaque
#    (`SetBeInstead`) si le cout n'est pas paye. Le moteur n'a de cout
#    additionnel dedie que pour le pouvoir de BASE de l'attaquant
#    (`AdditionalCostToAttack`, 50173), pas pour « attaquer CETTE cible ».
#  - **`ability/factory/additional_cost.py` CostFunction** : meme paiement
#    (`cost_func.PayCost(effect, joueur)`, abandon `SetBeInstead` sinon) que
#    `AdditionalCostToThwartThisScheme`, le pendant le plus proche.
#  - **`50173`** Divided Loyalties : `CostFunc.Spend(Cost("1"))` = « 1 ressource
#    de n'importe quel type ».
#
# ⚠ Mots-pieges : « ATTACK Super-Skrull » (toute attaque contre lui, pouvoir de
# base ou carte) ; « you MUST spend » (le joueur de l'attaquant) ; « 1 resource
# of ANY type » (Cost("1") generique, pas une ressource nommee). Le cout est paye
# a la declaration : l'attaque est annulee s'il ne peut pas l'etre (limite
# documentee, voir defs/super_skrull_questions.md).


def GetAbilities() -> Sequence['Ability']:

    def payer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        CostFunction(effect, message.attacker, message, CostFunc.Spend(Cost("1")))

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=NOM_MECHANT, card_type=Villain)),
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.NonKeyword, "Attached", payer),
    ]
