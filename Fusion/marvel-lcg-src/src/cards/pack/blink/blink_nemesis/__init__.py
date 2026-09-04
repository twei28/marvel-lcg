from cards.pack import *

# ===========================================================================
# Helpers partages du set « Blink Nemesis » (Timebroker).
#
# Le set ne frappe pas les points de vie : Timebroker ne peut PAS subir de
# degats, et c'est la manigance `Damaged Reality` qu'il faut contrer pour s'en
# debarrasser. Elle monte d'une menace par PORTAL en jeu, donc plus Blink
# deploie son moteur, plus elle coute cher — le set est ecrit en miroir du kit.
# ===========================================================================

NOM_TIMEBROKER = "Timebroker"
NOM_MANIGANCE = "Damaged Reality"
TRAIT_PORTAIL: 'CardFace.TRAITS' = "PORTAL"


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """Jumeau du helper du set « Blink ». Dupliquе volontairement : les deux
    sets sont deux paquets Python distincts, un module nemesis ne voit que ce
    fichier-ci. ⚠ Ne JAMAIS employer `GetBindFace()`, qui leve quand la carte
    n'est pas attachee (leçon yondu, sortie par l'autoplay)."""
    return getattr(face, "bind_face", None) if face is not None else None


def PortailsEnJeu(effect: 'Effect') -> List['CardFace']:
    """Les ameliorations PORTAL sur le terrain (lues par bk019)."""
    return list(Worlds.FindCardsOnField(effect, card_type=Upgrade, trait=TRAIT_PORTAIL))


def ChercherTimebroker(effect: 'Effect') -> 'CardFace|None':
    """« Search the encounter deck AND DISCARD PILE for Timebroker. »

    ⚠ LES DEUX ZONES. Ne fouiller que le deck rendrait bk020 inerte des que
    Timebroker a ete defausse une fois — or c'est exactement le cas que la
    carte existe pour couvrir. Meme montage que yd017/yd018 et dr012/dr014.
    """
    joueur = effect.GetInitiator() if Player.IsType(getattr(effect, "initiator", None)) else None
    if joueur is None:
        joueur = Worlds.GetCurrentPlayer(effect)
    faces = Search.SearchForCards(
        effect, joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        name=NOM_TIMEBROKER,
        card_type=Minion,
    )
    return faces[0] if faces else None


def TimebrokerEnJeu(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=NOM_TIMEBROKER, card_type=Minion)


def ManiganceEnJeu(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=NOM_MANIGANCE, card_type=SchemeSide2)
