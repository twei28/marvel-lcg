from cards.pack import *
from cards.pack.galactic_storm.binary import (
    JoueurDeCetteCarte, EnergieDeLaCarte, EnergieEnMain, CartesEnergieEnMain,
)

# Helpers partages du set « Binary Nemesis » (Galactic Storm, Kajislav) :
# Rogue (gs032), Goin' Rogue (gs239), Touched (gs237), Energy Transfer (gs240).
#
# Tout le set tourne autour d'UNE carte, Touched : Rogue la retrouve a chaque
# debut de phase des joueurs et l'attache a un personnage, et ce que Rogue
# gagne depend du TYPE de ce personnage (Touched) ou de son CAMP (Goin' Rogue).
#
# ⚠ « Rogue » et « Touched » sont designes par NOM ET TYPE : un heros officiel
# Rogue (38001a) et son amelioration Touched (38002) existent. Le sbire nemesis
# est un `Minion`, la carte nemesis Touched un `Attachment` : un joueur qui
# incarne Rogue n'est ni confondu avec la nemesis, ni pris pour « Rogue en
# jeu » (lecture notee au gabarit de gs237).

NOM_ROGUE = "Rogue"
NOM_TOUCHED = "Touched"


def EstRogue(face: 'CardFace|None') -> bool:
    return face is not None and Minion.IsType(face) and face.IsName(NOM_ROGUE)


def EstTouched(face: 'CardFace|None') -> bool:
    return face is not None and Attachment.IsType(face) and face.IsName(NOM_TOUCHED)


def RoguesEnJeu(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect) if EstRogue(f)]


def TouchedEnJeu(effect: 'Effect') -> 'CardFace|None':
    for f in Worlds.GetOnFieldCards(effect):
        if EstTouched(f):
            return f
    return None


def PorteurDeTouched(effect: 'Effect') -> 'CardFace|None':
    """Le personnage auquel Touched est attachee (None si elle n'est pas en jeu)."""
    touched = TouchedEnJeu(effect)
    if touched is None:
        return None
    return touched.CastTo(Attachment).attached_face


def TrouverTouched(effect: 'Effect') -> 'CardFace|None':
    """« find Touched » (livret p.4 : chercher dans chaque zone ou elle peut
    etre : en jeu, deck et defausse de rencontre, mise de cote, decks des
    joueurs...). Modele `rogue/38001a` (`Find.Find`)."""
    return Find.Find(
        effect,
        name=NOM_TOUCHED,
        card_type=Attachment,
    )


def PersonnagesSaufRogue(effect: 'Effect') -> List['CardFace']:
    """« a character other than Rogue » : identites, allies, vilain, sbires en
    jeu, sauf le sbire nemesis Rogue."""
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Unit2.IsType(f) and not EstRogue(f)]


def PorteurEst(effect: 'Effect', type_de_carte: Any) -> bool:
    porteur = PorteurDeTouched(effect)
    return porteur is not None and type_de_carte.IsType(porteur)


def RecalculRogue() -> List['OnEvent.Base']:
    """Touched change de porteur (attache / detache), entre ou sort du jeu, ou
    Rogue entre en jeu."""
    return [
        OnEvent.TemplateTrigger(Message.AfterCardAttachTo),
        OnEvent.TemplateTrigger(Message.AfterCardDetachFrom),
        OnEvent.CardInPlay(CardFinder(name=NOM_TOUCHED, card_type=Attachment)),
        OnEvent.CardInPlay(CardFinder(name=NOM_ROGUE, card_type=Minion)),
    ]


def CibleRogue() -> 'CardFinder':
    return CardFinder(name=NOM_ROGUE, card_type=Minion)
