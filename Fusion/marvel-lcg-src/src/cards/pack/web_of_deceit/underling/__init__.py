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

    Le meme texte porte les trois stades. La riposte est CONDITIONNELLE, ce que
    le mot-cle `Retaliate` de la donnee ne saurait dire : elle est donnee ici, et
    seulement quand l'attaquant n'est pas aerien.
    """
    def pas_aerien(effect: 'Effect') -> bool:
        return not Worlds.FindCardOnField(
            effect, CardFinder(trait="AERIAL", card_type=Friend))

    return AbilityFactory.ThisGainKeyword(
        lambda effect, ui: 0 if pas_aerien(effect) else 1,
        retaliate=valeur,
        change_on_event=OnEvent.CardInPlay(None),
    )


def ChercherLesCieux(effect: 'Effect') -> None:
    """« Setup: Find the Skies Above New York environment and reveal it. »

    ⚠ La carte ecrit « Skies OVER New York », l'environnement s'appelle « Skies
    ABOVE New York » : une coquille de l'auteur, tranchee en faveur du nom de la
    carte cherchee.
    """
    ChercherEtReveler(effect, name="Skies Above New York")
