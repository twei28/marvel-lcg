from cards.pack import *

# ===========================================================================
# Helpers partages du set « Iron Fist » (pack officiel MC64EN).
#
# MECANIQUE CENTRALE : le compteur `chi` (fiche docs/reference/mots-cles/chi-counter.md),
# pose sur la CARTE d'identite par la Reponse de la face heros 64001a (« place 1 chi
# counter here »). Iron Fist et Danny Rand sont les deux faces d'une meme carte : le
# stock est porte par la carte (component/counter.py) et RESTE au changement de forme
# (decision utilisateur n°5, Rules Reference : un personnage garde ses jetons).
# Modele : le compteur `dredge` du pack venus (tv001a), pose et depense sur l'identite.
#
# « Iron Fist » dans le texte d'une Technique = la face heros, c'est-a-dire l'identite
# du joueur en forme heros : toutes les capacites qui le nomment sont des Hero Action /
# Hero Interrupt / Hero Resource (forme heros obligatoire), sauf la retaliation
# d'Embody the Dragon, qui vise la face HEROS par son type (jamais Danny Rand).
#
# « une carte Iron Fist » (Deep Breathing) = une carte du set signature « Iron Fist »
# (bandeau « IRON FIST (n/15) ») : meme lecture que « Cyclops upgrade » de 33004 Field
# Commander, codee par `set_name`.
# ===========================================================================

CHI = 'chi'
SET_IRON_FIST = "Iron Fist"
TRAIT_TECHNIQUE = "TECHNIQUE"
CHI_CONSERVES = 4   # 64001a : « remove all but 4 chi counters from here »


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele venus / sunfire)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """L'identite du joueur (Iron Fist OU Danny Rand) : le porteur des compteurs de chi."""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def Chi(face: 'CardFace|None') -> int:
    """Nombre de compteurs de chi sur une carte (0 si aucune)."""
    if face is None:
        return 0
    return int(face.GetCounters(CHI) or 0)


def ChiDeLIdentite(effect: 'Effect') -> int:
    return Chi(IdentiteDuJoueur(effect))


def AuMoinsChi(n: int) -> 'Callable[[Effect, Any], bool]':
    """Condition « l'identite porte au moins n compteurs de chi » : le retrait est un COUT
    (fleche), la capacite n'est donc pas offerte quand il est impayable (RECETTES §5 :
    un cout dont l'echec est possible se double d'une condition)."""
    def condition(effect: 'Effect', message: 'Any') -> bool:
        return ChiDeLIdentite(effect) >= n
    return condition
