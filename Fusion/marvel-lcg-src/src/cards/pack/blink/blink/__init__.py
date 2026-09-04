from cards.pack import *

# ===========================================================================
# Helpers partages du set « Blink » (Kajislav, set 156, prefixe `bk`).
#
# TOUT LE PACK TOURNE AUTOUR DE `bk009` PORTAL : une amelioration a cout 0,
# cinq exemplaires, qu'on plante sur un ENNEMI ou une MANIGANCE. Six cartes la
# lisent, les DEUX faces de l'identite la recyclent, et le set nemesis attaque
# precisement cette economie.
#
# ⚠ NE JAMAIS appeler `GetBindFace()` en direct : il fait `assert face`
# (card_face.py) et leve donc des que la carte n'est PAS attachee. Le moteur
# AVALE l'exception, la capacite ne fait rien, et aucun cas de test ne le voit
# — leçon payee sur le pack yondu, sortie par l'AUTOPLAY seulement. Un portail
# passe justement son temps a etre pose et retire : tout le pack lit son hote
# par `Hote()`.
# ===========================================================================

NOM_HEROS = "Blink"
NOM_CIVIL = "Clarice Ferguson"
NOM_PORTAIL = "Portal"
TRAIT_PORTAIL: 'CardFace.TRAITS' = "PORTAL"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (leçon lady_sif). ⚠ Passer le joueur EXPLICITEMENT quand la
    carte ne lui appartient pas — c'est le cas de l'obligation bk017, carte de
    RENCONTRE donnee au joueur (leçon yd013).
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


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()`.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def PortailsEnJeu(effect: 'Effect') -> List['CardFace']:
    """Toutes les ameliorations PORTAL sur le terrain, ou qu'elles soient.

    ⚠ Elles ne vivent PAS la ou vivent les autres ameliorations du joueur :
    elles s'attachent a un ENNEMI ou a une MANIGANCE, donc
    `GetControlUpgrade` ne les voit pas. C'est tout le terrain qu'il faut
    balayer — meme leçon que la Yaka Arrow du pack yondu.
    """
    return list(Worlds.FindCardsOnField(effect, card_type=Upgrade, trait=TRAIT_PORTAIL))


def PortailsSur(effect: 'Effect', cible: 'CardFace|None') -> List['CardFace']:
    """Les PORTAL accroches a CETTE carte precise.

    Sert aux cartes « ... for each [[PORTAL]] upgrade attached to it »
    (bk005 Lose Footing, bk006 Multiple 'Porting) et aux selections
    « chaque ennemi/manigance qui en porte un » (bk004).
    """
    if cible is None:
        return []
    return [p for p in PortailsEnJeu(effect) if Hote(p) is cible]


def PorteUnPortail(effect: 'Effect', cible: 'CardFace|None') -> bool:
    """Raccourci lisible pour les filtres de bk004."""
    return bool(PortailsSur(effect, cible))
