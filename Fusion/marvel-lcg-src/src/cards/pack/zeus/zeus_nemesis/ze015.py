from . import *

# Shroud of the Nightmother (attachement, boost 2, CONDITION)
# Attach to your identity.
# You cannot spend [energy] resources while paying for cards.
# Alter-Ego Action: Spend 2 resources of any type → discard this card.
#
# LA CARTE LA PLUS DURE DU SET : sans energie, plus de Tempest, plus de
# Requirement, plus de Mount Olympus. Et l'obligation Alcohol Problems, qui
# coute un eclair, devient presque inamovible.
#
# COMMENT ON INTERDIT UNE COULEUR. Le moteur n'a pas de « tu ne peux pas
# depenser X » ; mais chaque moyen de paiement passe par le message
# `CheckEffectGeneratedResources` (resources.py:228), qui permet de REECRIRE
# ce qu'il genere : c'est le modele de `UpdateResourcesGeneratedWhilePlayingThis`
# (resources.py:340). On retire la part energie ; un moyen qui ne generait
# QUE de l'energie tombe a zero, et `CanPayThisCost` (resources.py:232) ne le
# propose plus. Un joker reste un joker : il n'est pas une energie.
#
# « while paying for cards » : seulement quand l'effet paye est une carte
# jouee (`ability.is_play`), pas une capacite de carte en jeu.
#
# Modeles : sg022 Ratatoskr's Whispers (attachement de rencontre sur
# l'identite + action d'alter ego a cout), 60020 (`CostFunc.Spend`).

def GetAbilities() -> Sequence['Ability']:

    def paye_par_le_joueur_porteur(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        porteur = effect.this.GetBindFace()
        if porteur is None or not Identity.IsType(porteur):
            return False
        return porteur.GetControlBy() is message.GetToPlayer()

    def pour_jouer_une_carte(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        return bool(message.for_effect.ability.is_play)

    def genere_de_l_energie(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        return message.res.GetColor("Y", convert_green_res=False) > 0

    def retirer_l_energie(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> None:
        energie = message.res.GetColor("Y", convert_green_res=False)
        message.SetResources(message.res - Resources("Y") * energie, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),

        Ability(
            AbilityType.NonKeyword,
            Message.CheckEffectGeneratedResources,
            [
                paye_par_le_joueur_porteur,
                pour_jouer_une_carte,
                genere_de_l_energie,
            ],
            retirer_l_energie,
            is_local=False,
        ),

        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Spend(Cost("2"))),
    ]
