from cards.pack import *
# Helpers partages du set « Major Victory ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
NOM_BOUCLIER = "Captain America's Shield"
NOM_SHIELD_TOSS = "Shield Toss"
NOM_COSTUME = "Containment Suit"
TRAIT_GUARDIAN = "GUARDIAN"


def ChoisirUne(joueur: 'Player', candidats: Sequence['CardFace'], effect: 'Effect', prompt: str) -> 'CardFace|None':
    """« an enemy » : la seule candidate part d'office, sinon le joueur choisit (obligatoire)."""
    if not candidats:
        return None
    if len(candidats) == 1:
        return candidats[0]
    return joueur.AskChooseFace(list(candidats), effect, prompt=prompt, forced=True)


def ControleUnGardien(joueur: 'Player') -> bool:
    """« a player who controls a GUARDIAN character » : identite ou allie portant le trait."""
    return any(f.HasTrait(TRAIT_GUARDIAN) for f in joueur.GetControlCharacters())


def DegatsDeShieldToss(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
    """« damage from your "Shield Toss" ability » : la source des degats est la capacite nommee de CE joueur."""
    par = getattr(message, "by_effect", None)
    capacite = getattr(par, "ability", None)
    if capacite is None or getattr(capacite, "name", "") != NOM_SHIELD_TOSS:
        return False
    return par.GetInitiator() == effect.GetInitiator() and message.trigger is not None and Enemy.IsType(message.trigger)
