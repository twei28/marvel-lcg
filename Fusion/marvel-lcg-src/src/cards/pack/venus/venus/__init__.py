from cards.pack import *

# ===========================================================================
# Helpers partages du set « Venus » (Inkwire, TMNT Heroes, prefixe `tv`).
# Decisions de l'utilisateur sur les cas analogues des quatre tortues :
# .planning/tmnt/decisions-phase-b.md (« Raphael » en forme civile = l'IDENTITE).
#
# MECANIQUE CENTRALE : le compteur `dredge` (« compteur de dragage »), pose sur la
# CARTE d'identite : Venus et Bonnie sont les deux faces d'une meme carte, elles
# partagent le meme stock (modele `rage` de Raphael, pack `raphael`).
#  - `tv001a` Venus en POSE (1 par amelioration ELEMENT controlee, plafond 6) ;
#  - `tv001b` Bonnie en retire 1 pour soigner ;
#  - ameliorations / evenements du pack en retirent 1 ou 2 EN COUT.
#
# « Venus » dans le texte imprime = L'IDENTITE, meme quand le joueur est en forme
# civile (Bonnie) : decision du 15/10/2026 pour « Raphael » (tr002, tr007, tr010),
# appliquee ici a `tv011` Dragon Scale, seule capacite utilisable aux deux formes.
#
# ⚠ « ELEMENT » est un TRAIT (card_face.py, ajoute pour ce pack) : il se compte et se
# cherche par `HasTrait`, jamais par le nom de la carte.
# ===========================================================================

NOM_HEROS = "Venus"
NOM_ALTER_EGO = "Bonnie"
DREDGE = 'dredge'
PLAFOND_DREDGE = 6
TRAIT_ELEMENT = "ELEMENT"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele sunfire / raphael).

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception.
    """
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
    """L'IDENTITE du joueur (Venus OU Bonnie) : la cible de « Venus » / « Bonnie »."""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS (« Venus »), ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def ElementsControles(joueur: 'Player|None') -> List['CardFace']:
    """« each [[ELEMENT]] upgrade you control »."""
    if joueur is None:
        return []
    return [f for f in joueur.GetControlUpgrade()
            if f is not None and f.HasTrait(TRAIT_ELEMENT)]


def Dragage(identite: 'CardFace|None') -> int:
    """Nombre de compteurs de dragage sur l'identite."""
    if identite is None:
        return 0
    return int(identite.GetCounters(DREDGE) or 0)


def PlacerDragage(effect: 'Effect', n: int, joueur: 'Player|None' = None, *,
                  maximum: 'int|None' = None) -> int:
    """« Place n dredge counter(s) on Venus » (sur l'identite, quelle que soit sa forme).

    `maximum` = plafond du STOCK de l'identite (`PlaceCountersOn(maximum=...)` :
    le moteur ne pose que ce qui tient). Rend le nombre reellement pose.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or n <= 0:
        return 0
    place = Faces.PlaceCountersOn([identite], n, DREDGE, effect, maximum=maximum)
    return int(place or 0)


def PeutRetirerDragage(effect: 'Effect', n: int, joueur: 'Player|None' = None) -> bool:
    return Dragage(IdentiteDuJoueur(effect, joueur)) >= n


def DefausserJusquA(effect: 'Effect', joueur: 'Player', *, card_type: 'Any' = None,
                    verifier: 'Callable[[CardFace], bool]|None' = None) -> 'CardFace|None':
    """« Discard cards from the top of your deck until you discard <X> » (mot-cle `seek`,
    fiche `docs/reference/mots-cles/seek.md`).

    Rend la carte trouvee, DEJA defaussee (a l'appelant de la mettre en main / en jeu).

    ⚠ Quand la carte trouvee est la TOUTE DERNIERE du deck, le moteur remelange aussitot la
    defausse dans le deck vide (`Deck.DiscardUntil`, regle du deck epuise) : la carte trouvee est
    alors dans le deck, melangee avec le reste de la defausse. `DiscardDeckUntil` la RENDRE quand
    meme, et c'est a l'appelant de la prendre : on ne la cherche pas ailleurs. Mesure par le cas
    « tv001b Bonnie Setup : l'ELEMENT est la toute derniere carte du deck ».
    """
    kw: Dict[str, Any] = {}
    if card_type is not None:
        kw["card_type"] = card_type
    if verifier is not None:
        kw["check_face_fn"] = verifier
    return joueur.DiscardDeckUntil(effect, **kw)


def ProposerRetraitDragage(effect: 'Effect', joueur: 'Player|None', nombre: int,
                           libelle: str, operation: 'Callable[[Sequence[CardFace]], Any]',
                           **cible: 'Any') -> None:
    """« You may remove <nombre> dredge counters from Venus to <effet> » : un choix
    FACULTATIF (bouton Passer), dont le retrait est le COUT. Branche non offerte quand
    l'identite porte moins de `nombre` compteurs (modele `01165` Eviction Notice :
    `ForChoiceAbility(...).SetCostFunc(...)` dans un `MayChooseOneAbility`).
    """
    if joueur is None:
        return
    branche = AbilityFactory.ForChoiceAbility(libelle, operation).SetCostFunc(
        CostFunc.Counter("YourIdentity", nombre, DREDGE))
    if cible:
        branche = branche.SetTarget(**cible)
    joueur.MayChooseOneAbility(effect, branche)
