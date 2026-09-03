from cards.pack import *

# Helpers partages du set « Iron Man (Model 42) ».


def CompteursReacteur(face: 'CardFace') -> int:
    """Nombre de compteurs `reactor` portes par une face.

    Neuf cartes du pack posent la meme question, et deux d'entre elles
    (im009, im014) doivent savoir s'il y en a AVANT d'agir.
    """
    return face.GetCounters('reactor')


def RetirerUnReacteur(identite: 'CardFace', effect: 'Effect') -> bool:
    """Retire 1 compteur `reactor` de l'identite, et dit si ca a marche.

    ⚠ Le RETOUR est la raison d'etre de ce helper. Sept cartes du pack
    ecrivent « remove 1 reactor counter from Iron Man -> <effet> » : la
    fleche en fait un COUT, donc l'effet ne doit PAS tomber si le compteur
    n'etait pas la. Tester la presence AVANT de retirer est le seul moyen sur :
    `Faces.RemoveCountersOn` ne dit rien de ce qu'il a reellement enleve.
    """
    if CompteursReacteur(identite) < 1:
        return False
    Faces.RemoveCountersOn([identite], 1, 'reactor', effect)
    return True


def CoutDuReacteur(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
    """`CostFunc.Custom` pour « remove 1 reactor counter from Iron Man -> ... ».

    ⚠ LE RETRAIT VA DANS LE COUT, JAMAIS DANS LE CORPS, ET C'EST UN CORRECTIF
    PAYE EN AUTOPLAY (03/09/2026). Ecrit dans le corps sous la forme
    `if RetirerUnReacteur(...): <effet>`, la capacite RESOUT quand meme
    lorsqu'il n'y a aucun compteur — elle ne fait simplement rien. Le moteur
    la repropose alors a l'identique, le pilote la reprend, et la partie
    tourne en rond : **1 partie bloquee sur 32**, verdict « meme question
    posee a l'identique et le plateau n'a pas bouge ». C'est exactement le
    defaut du blocage Underling (SESSION du 20/08).

    Dans le COUT, le `False` empeche le paiement : l'option n'est meme pas
    offerte quand le reacteur est vide. im009 et im011 le faisaient deja ;
    im007, im008 et im013 ne le faisaient pas.
    """
    Unused(targets)
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    identite = joueur.GetIdentity()
    if identite is None:
        return False
    return RetirerUnReacteur(identite, effect)
