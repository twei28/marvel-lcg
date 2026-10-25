from cards.pack import *

# Helpers partages du set « Predator Nemesis » (la Reine, le camouflage).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK, ou dans celui du set
# « Predator », leve un NameError avale par le moteur (lecon hk005). Ce qu'appellent les cartes nemesis vit donc ICI.

ID_REINE = "pd017"
NOM_HEROS = "Predator"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def LaReineEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Xenomorph Queen (pd017) en jeu, ou None."""
    for face in Worlds.GetOnFieldMinions(effect):
        if face.paper.card_id == ID_REINE:
            return face
    return None


def AmenerLaReine(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """« Find Xenomorph Queen and put it into play engaged with you » : Find.Find balaie toutes les zones (set de cote
    compris : le sbire nemesis y attend). Rend la Reine posee, ou None (introuvable, ou deja en jeu)."""
    if joueur is None:
        return None
    reine = Find.Find(
        effect, who_perform=joueur,
        finder=CardFinder(card_ids=[ID_REINE], check_face_fn=lambda f: not f.IsInPlay()),
    )
    if reine is None or not reine.PutIntoPlay(joueur, effect):
        return None
    reine.CastTo(Minion).EngagePlayer(joueur, effect)
    return reine
