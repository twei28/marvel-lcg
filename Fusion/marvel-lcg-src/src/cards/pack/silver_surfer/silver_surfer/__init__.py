from cards.pack import *

# Helpers partages du set « Silver Surfer ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le
# `__init__.py` du PACK leve un NameError avale par le moteur (lecon hk005).

NOM_PLANCHE = "The Silver Surfboard"
NOM_HEROS = "Silver Surfer"
NOM_DAWN = "Dawn Greenwood"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier :
    il leve un assert quand l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def LaPlanche(effect: 'Effect', joueur: 'Player|None'=None) -> 'CardFace|None':
    """The Silver Surfboard EN JEU chez le joueur, ou None."""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    trouvees = joueur.GetControlUpgrade(CardFinder(card_type=Upgrade, name=NOM_PLANCHE))
    return trouvees[0] if trouvees else None


def ChangerDeForme(joueur: 'Player', effect: 'Effect') -> None:
    """« Change your form » : fait passer l'identite du joueur a son autre face."""
    identite = joueur.GetIdentity()
    if identite is not None:
        identite.ChangeToOtherIdentityForm(effect)


def PeutConvoquer(joueur: 'Player', nom: str) -> bool:
    """La carte nommee existe-t-elle HORS JEU chez le joueur (deck, defausse, main) ? Sans ouvrir de fenetre
    de choix : sert de condition a une option, qui ne doit pas etre proposee si `Convoquer` ne trouve rien."""
    for zone in (joueur.player_deck.Get(), joueur.discard_pile.Get(), joueur.hand_cards.Get()):
        for face in zone:
            if face.paper.name.lstrip("* ").strip() == nom:
                return True
    return False


def Convoquer(effect: 'Effect', nom: str, card_type: Any=Ally, joueur: 'Player|None'=None) -> 'CardFace|None':
    """MOT-CLE MAISON `summon` (notice « Silver Surfer Insert » : « search the deck, discard pile, hand, or
    anywhere out of play for that card, then follow the additional instructions. If any decks were searched,
    shuffle them »). Meme definition et meme montage que le pack yondu (fiche mots-cles/summon.md).

    ⚠ Rend la carte SANS la deplacer : c'est a l'appelant de dire ce qu'il en fait (« add it to your hand »,
    « remove her from the game »...). `Search` la sort du deck (sas de traitement) : l'appelant DOIT la consommer.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    # Les zones ordinaires d'abord, la zone « retire de la partie » seulement en dernier recours : une carte
    # unique n'existe qu'a un endroit, mais un banc de test (ou une carte jouee deux fois) peut en laisser
    # un exemplaire retire, que la fouille ne doit pas preferer a celui qui est encore dans le deck.
    for retiree in (False, True):
        faces = Search.SearchForCards(
            effect, joueur,
            include_player_deck=not retiree,
            include_player_discard_pile=not retiree,
            include_player_hand_cards=not retiree,
            include_set_aside=not retiree,
            include_removed_area=retiree,
            name=nom,
            card_type=card_type,
        )
        if faces:
            return faces[0]
    return None
