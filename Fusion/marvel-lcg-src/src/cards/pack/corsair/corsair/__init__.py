from cards.pack import *

# Helpers partages du set « Corsair » (Phenexian et Mysteltainn, prefixe `cr`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

CORSAIR = "cr001a"
REMISE = "cr009"
RIPOSTE = "cr008"
PARRY = "cr007"


def JoueurDe(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (ou son initiateur)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def IdentiteDe(effect: 'Effect') -> 'CardFace|None':
    """L'identite (les deux faces partagent la zone des cartes glissees) du joueur de la carte."""
    joueur = JoueurDe(effect)
    return joueur.GetIdentity() if joueur is not None else None


def Glissees(identite: 'CardFace|None') -> List['CardFace']:
    """Les cartes glissees sous Corsair (zone `PlaceCardArea`, hors jeu)."""
    if identite is None:
        return []
    return list(identite.GetPlacedCardArea().Get())


def DerniereCarteJouee(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """« The last card you played » : la derniere carte jouee AVANT celle qui est en train de se resoudre.
    ⚠ Le moteur inscrit la carte jouee dans `this_round_played_cards` AVANT le calcul de son cout (lecon nt005 Kickflip) :
    on l'ecarte, sinon la carte se verrait elle-meme. La liste est celle de TOUTE LA PARTIE (`game_played_cards`,
    CORRECTIF du 26/10/2026) : « the last card you played » n'est borne ni au round ni au tour (Riposte se joue pendant
    la phase du vilain, Remise au tour du joueur suivant)."""
    if joueur is None:
        return None
    precedentes = [f for f in joueur.stat.game_played_cards if f is not effect.this]
    return precedentes[-1] if precedentes else None


def DerniereEstUne(effect: 'Effect', joueur: 'Player|None', card_id: str) -> bool:
    derniere = DerniereCarteJouee(effect, joueur)
    return derniere is not None and getattr(derniere.paper, "card_id", None) == card_id


def Ennemis(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsInPlay()]


def NomNu(face: 'CardFace') -> str:
    """Le nom sans l'etoile d'unicite, ni ses sous-titres entre parentheses."""
    nom = str(face.name).lstrip("* ").strip()
    return nom.split(" (")[0]


def ToujoursEnDefausse(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
    """La carte defaussee attend encore dans la defausse de son joueur. Pocket Universe Gems (cr001a) et Corsair's Rapier (cr003)
    repondent a la MEME defausse : declenchees ensemble, la 2e se resout apres que la 1re a deja glisse la carte (CORRECTIF du
    26/10/2026 : sans cette garde, la carte etait glissee deux fois)."""
    joueur = JoueurDe(effect)
    return joueur is not None and message.trigger.card.area is joueur.discard_pile


def GemmesDisponibles(effect: 'Effect') -> bool:
    """« (Limit once per round.) » partagee par les DEUX chemins de Pocket Universe Gems (depense de ressources, defausse
    en cout) : un marqueur de round sur l'identite, plutot que deux `LimitOncePerRound` qui donneraient deux usages."""
    identite = IdentiteDe(effect)
    return identite is not None and getattr(identite, "cr_gemmes_round", None) != effect.world.round_id


def GemmesUtilisees(effect: 'Effect') -> None:
    identite = IdentiteDe(effect)
    if identite is not None:
        identite.cr_gemmes_round = effect.world.round_id
