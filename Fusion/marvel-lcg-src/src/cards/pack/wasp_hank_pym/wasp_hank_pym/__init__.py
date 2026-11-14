from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout  # noqa: F401

# Helpers partages du set « Wasp (Hank Pym) » (JackHKP, prefixe `hp`).
# ⚠ Les modules du set font `from . import *` : tout ce que les cartes appellent vit ICI
# (un helper pose dans le `__init__.py` du PACK leve un NameError avale, lecon hk005).

def forme_vers(effect: 'Effect', trait: str) -> None:
    """« Change to GIANT/TINY hero form » : la forme heros qui porte ce trait."""
    joueur = effect.GetInitiator()
    joueur.GetIdentity().ChangeToForm(CardFinder2(trait, Hero), effect)

def changer_de_forme(effect: 'Effect') -> None:
    """« Change form » : une AUTRE face de l'identite (alter ego, minuscule, geant). Avec deux
    choix possibles le joueur designe la forme voulue (les deux formes heros s'appellent « Wasp » :
    on distingue par les traits, `traits_str`)."""
    joueur = effect.GetInitiator()
    identite = joueur.GetIdentity()
    autres = joueur.GetAllIdentityFace(exclude=identite)
    if not autres:
        return
    if len(autres) == 1:
        cible = autres[0]
    else:
        par_nom = {face.traits_str: face for face in autres}
        cible = par_nom[joueur.AskChooseOneText(list(par_nom))]
    identite.ChangeToFace(cible, effect)

def formes_changees_ce_tour(effect: 'Effect') -> int:
    """« the number of times you have changed form this turn » (CORRECTIF world_stat.py)."""
    return effect.world.stat.CountFormChanges(effect.GetInitiator())

def size_manipulations(joueur: 'Player') -> List['CardFace']:
    return joueur.GetControlCards(CardFinder(name="Size Manipulation", card_type=Upgrade))

def en_forme(trait: str):
    """Condition « you are in <trait> hero form »."""
    return lambda effect, message: Condition.YouAreInHeroFrom(effect, trait)
