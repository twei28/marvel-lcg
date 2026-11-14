from cards.pack import *
# Helpers partages du set « Raza » (Phenexian et Mysteltainn, prefixe `rl`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
SEUIL_DEGATS = 5


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
    joueur = JoueurDe(effect)
    return joueur.GetIdentity() if joueur is not None else None


def AbimeDe(effect: 'Effect') -> bool:
    """« If you have sustained 5 or more damage » : les degats SUBIS par l'identite du joueur de la carte."""
    identite = IdentiteDe(effect)
    return identite is not None and identite.sustained >= SEUIL_DEGATS


def CartesAvecTrait(effect: 'Effect', trait: str) -> List['CardFace']:
    """« each [[TRAIT]] you control » : toute carte en jeu sous le controle du joueur (allies, ameliorations, soutiens)."""
    joueur = JoueurDe(effect)
    if joueur is None:
        return []
    return [f for f in joueur.GetControlCards() if f.IsInPlay() and f.HasTrait(trait)]


def PresDeLIdentite(face: 'CardFace') -> bool:
    """Amelioration non attachee a une autre carte : `bind_face` absent, ou l'identite (cas ordinaire du moteur)."""
    hote = getattr(face, "bind_face", None)
    return hote is None or isinstance(hote, Identity)


def AmeliorationsTechOuArme(joueur: 'Player|None') -> List['CardFace']:
    """« unattached [[TECH]] or [[WEAPON]] upgrade you control » : chaque amelioration comptee UNE fois, meme TECH ET WEAPON.
    « Unattached » (RR Upgrade, arbitrage du 26/10/2026) : une amelioration ordinaire entre en jeu PRES de l'identite ; seules celles
    qui s'attachent (« attach to ») a une AUTRE carte (allie, sbire...) sont exclues. Dans le moteur une amelioration ordinaire a
    pour `bind_face` l'identite elle-meme : seule une carte attachee ailleurs que sur une identite est exclue."""
    if joueur is None:
        return []
    return [f for f in joueur.GetControlCardsByType(upgrade=True)
            if f.IsInPlay() and PresDeLIdentite(f) and (f.HasTrait("TECH") or f.HasTrait("WEAPON"))]
