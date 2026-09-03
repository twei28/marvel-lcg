from cards.pack import *

# Helpers partages du set « Night Thrasher ».
#
# ⚠ NEUF cartes du pack posent la MEME question : « ou est la Battle Board de
# ce joueur, et quelle face montre-t-elle ? ». Un seul chemin pour tout le
# monde, pour que les neuf ne puissent pas diverger — c'est la leçon des deux
# empreintes d'autoplay du 03/09/2026, qui lisaient chacune un sous-ensemble
# different du monde.

NOM_PLANCHE = "Battle Board"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif). Les capacites continues
    (nt009) sont evaluees hors tour de jeu, sans initiateur.
    `GetControlByOrOwner` retombe sur le PROPRIETAIRE quand la carte n'est pas
    en jeu, ce qui couvre l'evenement en cours de resolution.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def PlancheDuJoueur(joueur: 'Player|None') -> 'CardFace|None':
    """La Battle Board que CE joueur controle, quelle que soit sa face.

    ⚠ `GetControlUpgrade` balaie les ameliorations attachees aux personnages
    du joueur, pas le terrain entier : en multijoueur, la planche d'un autre
    Night Thrasher n'est jamais rendue. C'est le montage employe par le moteur
    lui-meme pour « your suit form upgrade » de Nick Fury
    (`selector_target_helper.py:264`).
    """
    if joueur is None:
        return None
    trouvees = joueur.GetControlUpgrade(CardFinder(card_type=Upgrade, name=NOM_PLANCHE))
    if not trouvees:
        return None
    return trouvees[0]


def MaPlanche(effect: 'Effect') -> 'CardFace|None':
    """Raccourci : la Battle Board du joueur de la carte qui agit."""
    return PlancheDuJoueur(JoueurDeCetteCarte(effect))


def RetournerLaPlanche(effect: 'Effect') -> 'CardFace|None':
    """« Flip the Battle Board upgrade. » — et rend la face APRES bascule.

    ⚠ Le retour est la raison d'etre du helper : `nt002` Disaster et `nt005`
    Kickflip lisent le trait APRES avoir retourne, jamais avant. Lire la face
    d'avant inverserait les deux branches de Disaster.
    ⚠ `card.Flip` peut etre REFUSE — `nt012` Practice et `nt014` Cemented
    interdisent justement le retournement. On relit donc la face reelle apres
    coup au lieu de supposer qu'elle a change.
    """
    planche = MaPlanche(effect)
    if planche is None:
        return None
    planche.card.Flip(effect)
    return MaPlanche(effect)


def PlancheEstVehicule(effect: 'Effect') -> bool:
    """« if the Battle Board upgrade has the [[VEHICLE]] trait » (5 cartes).

    ⚠ Le trait se lit sur l'AMELIORATION, pas sur le heros : nt003a porte
    VEHICLE, nt003b porte WEAPON a la place. Une planche absente du terrain
    n'est ni l'un ni l'autre, et les DEUX branches doivent alors tomber a
    vide. Modele `IfAlertLevelIsHighSide` (aos/batroc/__init__.py:6), meme
    montage sur une carte recto-verso dont le trait est la seule difference
    lisible.
    """
    planche = MaPlanche(effect)
    return planche is not None and planche.HasTrait("VEHICLE")


def PlancheEstArme(effect: 'Effect') -> bool:
    """« if the Battle Board upgrade has the [[WEAPON]] trait » (5 cartes)."""
    planche = MaPlanche(effect)
    return planche is not None and planche.HasTrait("WEAPON")
