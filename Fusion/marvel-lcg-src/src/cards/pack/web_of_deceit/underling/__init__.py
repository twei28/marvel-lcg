from cards.pack.web_of_deceit import *

# LA VARIANTE « SOUS-FIFRE » DU SET VULTURE
#
# Quatorze cartes numerotees « VULTURE (1/14) » a « (14/14) », dont DIX sont
# celles du set principal au mot pres : Feather Daggers, Vulturion x2, The
# Vulture's Plans, Sweeping Swoop, Falling x2, Aerial Advantage, Aerial Dogfight
# et Highway Robbery. Seules quatre sont neuves — les trois stades de Vulture et
# l'environnement « Skies Above New York ».
#
# Ce n'est donc pas un modulaire de plus : c'est une DEUXIEME FACON DE JOUER
# VULTURE, en sous-fifre d'un autre vilain. Il RIPOSTE au lieu d'etre
# intouchable, ce qui change tout : on peut le frapper depuis le sol, mais ca
# coute.


def RiposteSaufContreLesAeriens(valeur: int) -> 'Ability':
    """« Vulture gains retaliate N during the player phase unless the attacker or
    attack has the AERIAL trait. »

    Le meme texte porte les trois stades, a la valeur pres.

    ⚠ CE N'EST PAS LE MOT-CLE `Retaliate`, ET LE PREMIER JET L'AVAIT INVERSE.
    La riposte depend de QUI FRAPPE, un renseignement que le moteur ne connait
    qu'au moment de l'attaque : un mot-cle constant ne peut pas l'exprimer. Le
    premier jet lisait « une carte AERIAL est-elle en jeu ? » et donnait la
    riposte quand il y en avait une — l'exact contraire du texte, qui l'enleve
    dans ce cas.
    """
    def attaquant_aerien(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        attaquant = message.attacker
        if attaquant is not None and attaquant.HasTrait("AERIAL"):
            return True
        # « or attack has the AERIAL trait » : la carte qui porte l'attaque, un
        # evenement par exemple, compte autant que celui qui la lance.
        source = message.by_effect.this if hasattr(message, "by_effect") else None
        return bool(source is not None and source.HasTrait("AERIAL"))

    def riposter(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(EncounterVillain)
        attaquant = message.attacker
        if attaquant is not None:
            this.DealDamage([attaquant], valeur, effect)

    return AbilityFactory.AfterUnitBeAttacked(
        AbilityType.ForcedResponse,
        "This",
        riposter,
        conditions=[
            # « during the player phase » : la riposte ne mord que quand ce sont
            # les heros qui frappent, pas pendant la phase du vilain.
            lambda effect, message: Worlds.Phase(effect).IsPlayerPhase("AnyPlayer"),
            lambda effect, message: not attaquant_aerien(effect, message),
        ],
    )


def ChercherLesCieux(effect: 'Effect') -> None:
    """« Setup: Find the Skies Above New York environment and reveal it. »

    ⚠ La carte ecrit « Skies OVER New York », l'environnement s'appelle « Skies
    ABOVE New York » : une coquille de l'auteur, tranchee en faveur du nom de la
    carte cherchee.
    """
    ChercherEtReveler(effect, name="Skies Above New York")
