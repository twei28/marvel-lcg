from cards.pack import *

# Helpers partages du set « Predator » (Infralocked, Cloaked).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale
# par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

ID_INFRALOCKED = "pd002"
NOM_HEROS = "Predator"


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


def HerosDuJoueur(joueur: 'Player|None') -> 'CardFace|None':
    """La face HEROS de Predator (jamais l'alter-ego Yd'Nar : un statut Cloaked se pose sur le heros)."""
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None:
        return None
    heros = identite.GetHeroFace()
    if heros is None or not heros.IsName(NOM_HEROS):
        return None
    return heros


def Infralocked(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """L'UNIQUE carte Infralocked de ce joueur, en jeu (sur son identite ou sur un sbire), ou None."""
    if joueur is None:
        return None
    for face in Worlds.GetOnFieldCards(effect):
        if face.paper.card_id == ID_INFRALOCKED and face.GetOwnerPlayer() is joueur:
            return face
    return None


def EstCamoufle(joueur: 'Player|None') -> bool:
    """« You are cloaked » : Predator (forme heros) porte une carte Cloaked."""
    heros = HerosDuJoueur(joueur)
    return heros is not None and heros.IsCloaked()


def Camoufler(effect: 'Effect', joueur: 'Player|None') -> int:
    """« Give Predator a cloaked status card » : pose Cloaked sur le HEROS (une seule par personnage).
    Rend le nombre de cartes reellement posees (0 si deja camoufle, ou si Xenomorph's Prey l'interdit)."""
    heros = HerosDuJoueur(joueur)
    if heros is None:
        return 0
    return ShinobiCloak(effect, heros)


def TrouverUnSbire(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """« Find a minion and put it into play engaged with you » : Find.Find balaie toutes les zones (regle du 23/10/2026,
    `game/operate/find.py`) ; un sbire DEJA en jeu ne peut pas « entrer en jeu » : on ne le propose pas. Rend le sbire
    pose, engage avec `joueur`, ou None."""
    if joueur is None:
        return None
    sbire = Find.Find(
        effect, who_perform=joueur,
        finder=CardFinder(card_type=Minion, check_face_fn=lambda f: not f.IsInPlay()),
    )
    if sbire is None:
        return None
    if not sbire.PutIntoPlay(joueur, effect):
        return None
    sbire.CastTo(Minion).EngagePlayer(joueur, effect)
    return sbire


def IconesDeBoost(face: 'CardFace|None') -> int:
    """« each icon (★ and Y) in that card's boost area » : les icones de boost ordinaires PLUS l'icone a etoile."""
    if face is None:
        return 0
    return FacesCounter.CountTotalBoostIcons([face]) + FacesCounter.CountTotalBoostStar([face])


def RetirerMenaceDUneManigance(effect: 'Effect', joueur: 'Player|None', valeur: int = 1) -> None:
    """« Remove N threat from a scheme » : le joueur choisit parmi les manigances qui portent de la menace."""
    if joueur is None:
        return
    manigances = [x for x in (list(Worlds.GetMainSchemes(effect)) + list(Worlds.GetAllSideSchemes(effect)))
                  if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
    if not manigances:
        return
    cible = joueur.AskChooseFace(manigances, effect, prompt="Remove threat from")
    Faces.RemoveTokensOn([cible or manigances[0]], valeur, 'threat', effect)
