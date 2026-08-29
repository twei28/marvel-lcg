from . import *

# * Red Guardian's Shield
# Temporary.
# While this card is in your hand, you can control 1 fewer restricted card.
# Hero Interrupt: When your turn ends, return this card from play to your hand.
#
# La carte n'a PAS de cout et ne se joue jamais depuis la main comme une
# amelioration ordinaire : c'est « Shield Launch » (rg001a) qui l'attache a un
# ennemi ou a une manigance. `CanPlayThisUpgradeCard` declare donc seulement
# les cibles legales de l'attache (modele Webbed Up 01009 pour l'ennemi,
# Overwatch 30019 pour la manigance).
#
# ECART ASSUME : « you can control 1 fewer restricted card » n'est PAS rendu.
# Recherche faite dans le moteur, trois constats :
#   1. `RestrictedLimit` (game/player/limit_monitor/restricted_limit.py) ne
#      sait qu'AUGMENTER la limite : `Increase()` assert `diff` dans {1, -1}
#      et se contente d'ajouter/retirer une entree du dict
#      `additional_restricted_limit`. La base `restricted_limit` (2) n'est
#      modifiee nulle part dans tout le code.
#   2. Aucun message de verification n'existe pour le restreint, contrairement
#      aux limites voisines : `Message.CheckIfAllyCountLimit` (allies) et
#      `Message.CheckIfFaceCountHandSize` (taille de main) ont un crochet,
#      `RestrictedLimit.CheckLimit()` n'en envoie aucun.
#   3. `CheckLimit()` ne compte que les cartes de l'inventaire EN JEU et n'est
#      declenchee que par entree en jeu / flip / sortie de jeu. Un changement
#      de MAIN ne la reveille jamais, et une carte en main n'a d'abilites
#      actives que pour se jouer ou se payer (`CanWorkOnlyInHand`), pas pour
#      un effet continu.
# Le seul sens implemente dans la base de cartes est « 1 additional » (Venom
# 20001a/b, Side Holster 20021, Prehensile Tail 48005) via
# `control_additional_restricted`. rg008 est la seule carte du jeu a demander
# l'inverse. La clause est donc laissee au joueur, comme les autres
# approximations documentees du projet.


def GetAbilities() -> Sequence['Ability']:

    def rendre(effect: 'Effect', message: 'Message.WhenPlayerTurnEnd') -> None:
        RendreLeBouclier(effect)

    return [
        # `Enemy|Scheme2` et non un tuple : le moteur passe le type par
        # `Types.UnionTypeExtract`, qui lit `__args__` — donc une vraie union.
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy | Scheme2),
        ),
        AbilityFactory.WhenPlayerTurnEnd(
            AbilityType.HeroInterrupt,
            "You",
            rendre,
        ),
    ]
