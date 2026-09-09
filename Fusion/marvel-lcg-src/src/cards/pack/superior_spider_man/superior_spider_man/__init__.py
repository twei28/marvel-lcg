from cards.pack import *

# ===========================================================================
# Helpers partages du set « Superior Spider-Man » (Rainy, set 167, prefixe
# `su`). Otto Octavius dans le corps de Peter Parker.
#
# ⚠⚠ DEUX ALTER-EGOS, ET C'EST STRUCTUREL. L'insert : « choose one of these
# alter-egos to use this game and its corresponding obligation (the other set
# will not be needed and cannot be changed to during this game) ». Le moteur
# ne monte qu'un alter-ego par deck de depart, d'ou DEUX decks
# (`superior_spider_man` = su001b Peter Parker + su013 Ghost of a Conscience ;
# `superior_spider_man_tolliver` = su001c Elliot Tolliver + su014 Crisis of
# Conscience). Arbitrage utilisateur du 08/09/2026. Les deux faces d'alter-ego
# portent le MEME texte (« Master Planner ») : leur module est identique, seul
# le nom propre change dans les commentaires.
#
# ⚠ LE PACK TOURNE AUTOUR DE DEUX CHOSES :
#  1. Le mot-cle maison **`track`** — « move 1 threat from a scheme to a minion
#     in play » (fiche `docs/reference/mots-cles/track.md`). C'est un
#     DEPLACEMENT : la menace quitte la manigance et se pose sur le sbire. La
#     coder comme un simple retrait ferait de tout le pack un contre gratuit.
#     Le compteur `threat` sur un SBIRE n'existe pas nativement dans le moteur :
#     il a ete AJOUTE a l'enum `COUNTER` le 08/09/2026, comme `surveillance`.
#  2. **Contingency Plan** (`su012`), une amelioration `Permanent` + `Setup` qui
#     commence en jeu et sur laquelle on pose UNE carte face cachee, jouable
#     ensuite comme si elle etait en main. Trois cartes l'alimentent : les deux
#     alter-egos et `su008` Mastermind.
#
# ⚠ HOMONYMES : « * Spider-Man » designe QUATRE cartes au depot (01001a,
# sr001a, sm001a, su001a) et « * Peter Parker » trois (01001b, sr001b, su001b).
# CONSEQUENCE : aucune carte de ce pack ne cherche par NOM. Contingency Plan et
# Hobgoblin se retrouvent par `card_ids`.
# ===========================================================================

SET_HEROS: 'CardFace.SETNAMES' = "Superior Spider-Man"
ID_HEROS = "su001a"
ID_PETER = "su001b"
ID_TOLLIVER = "su001c"
ID_CONTINGENCY = "su012"
ID_HOBGOBLIN = "su016"

COMPTEUR_MENACE: 'CardFace.COUNTER' = 'threat'
COMPTEUR_SURVEILLANCE: 'CardFace.COUNTER' = 'surveillance'
COMPTEUR_TOILE: 'CardFace.COUNTER' = 'web'
TRAIT_AERIAL: 'CardFace.TRAITS' = "AERIAL"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (lecon `Player.GetHero()`, pack lady_sif).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS, ou None en forme civile. ⚠ Filtre par TYPE, jamais par
    nom : « Spider-Man » designe quatre cartes au depot."""
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas."""
    return getattr(face, "bind_face", None) if face is not None else None


def CardId(face: 'CardFace|None') -> str:
    """⚠ `face.card_id` N'EXISTE PAS : le chemin est `face.paper.card_id`."""
    paper = getattr(face, "paper", None) if face is not None else None
    return getattr(paper, "card_id", "") or ""


################################################################################
# Le mot-cle maison `track`
################################################################################

def MenaceSurSbire(face: 'CardFace|None') -> int:
    """Les pions `threat` poses sur ce sbire.

    ⚠ `GetCounters` vit sur `CanPlaceCounter`, qui n'est PAS exporte par
    `cards.pack` : on passe par un `getattr` pour ne pas lever d'AttributeError
    que le moteur avalerait en silence.
    """
    if face is None:
        return 0
    lire = getattr(face, "GetCounters", None)
    if lire is None:
        return 0
    return int(lire(COMPTEUR_MENACE) or 0)


def SbiresEnJeu(effect: 'Effect') -> List['CardFace']:
    """TOUS les sbires en jeu — pas seulement ceux engages avec le joueur.
    L'insert est explicite : « they do not need to be engaged with you in order
    to be tracked »."""
    return [m for m in Worlds.GetOnFieldEnemies(effect)
            if m is not None and Minion.IsType(m)]


def SbiresTraces(effect: 'Effect') -> List['CardFace']:
    """Les sbires qui portent au moins un pion de menace."""
    return [m for m in SbiresEnJeu(effect) if MenaceSurSbire(m) > 0]


def PeutTracer(effect: 'Effect') -> bool:
    """Y a-t-il de quoi tracer ? Il faut un sbire ET de la menace quelque part.

    ⚠ Toute carte qui met `track` en COUT doit doubler son `CostFunc` de cette
    condition (RECETTES §5) : sans cible, le cout echoue APRES que la carte a
    ete jouee, et le joueur la perd pour rien.
    """
    if not SbiresEnJeu(effect):
        return False
    return any(f is not None and getattr(f, "threat", 0)
               for f in Worlds.GetOnFieldSchemes(effect))


def Tracer(effect: 'Effect', sbire: 'CardFace|None',
           complots: Sequence['CardFace']) -> int:
    """« TRACK » : deplace 1 menace d'une manigance vers un sbire.

    Rend le nombre de menaces reellement deplacees (0 ou 1).

    ⚠⚠ C'EST UN DEPLACEMENT, PAS UN RETRAIT. On ne pose sur le sbire que ce
    qu'on a REELLEMENT retire de la manigance : `RemoveThreatFromSchemes` peut
    ne rien retirer (manigance vide, `patrol` sur un sbire engage, icone crisis
    en jeu — le Q/R de l'insert le dit noir sur blanc). Poser un pion sans
    verifier le retrait CREERAIT de la menace au lieu de la deplacer.
    ⚠ Et surtout pas d'`ignore_crisis` : le Q/R veut justement que le complot
    principal soit protege par patrol et par crisis.
    """
    if sbire is None:
        return 0
    vises = [c for c in complots if c is not None]
    if not vises:
        return 0

    source = effect.this
    avant = sum(int(getattr(c, "threat", 0) or 0) for c in vises)
    source.RemoveThreatFromSchemes(vises, 1, effect)
    apres = sum(int(getattr(c, "threat", 0) or 0) for c in vises)

    deplacee = max(0, avant - apres)
    if deplacee > 0:
        Faces.PlaceCountersOn([sbire], deplacee, COMPTEUR_MENACE, effect)
    return deplacee


def ContingencyPlanDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """`su012` Contingency Plan sous le controle de ce joueur, s'il y est.

    Retrouve par `card_id` et non par nom (voir l'en-tete : le pack s'interdit
    les recherches par nom).
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    for carte in joueur.GetControlCards():
        if carte is not None and CardId(carte) == ID_CONTINGENCY:
            return carte
    return None


def CartesPoseesSous(face: 'CardFace|None') -> List['CardFace']:
    """Ce qui est pose SOUS cette carte — la carte face cachee de Contingency
    Plan.

    ⚠ `GetAttachedUpgrades` ne rendrait que les AMELIORATIONS : ici c'est
    n'importe quelle carte, posee par `PlaceCardHere(..., face_up=False)`.
    ⚠⚠ `Get(True)` et NON `Get()` : le drapeau demande aussi les cartes FACE
    CACHEE, et c'est precisement ainsi qu'elles sont posees. Sans lui la zone
    parait vide et Contingency Plan semble ne rien porter.
    """
    if face is None:
        return []
    lire = getattr(face, "GetPlacedCardArea", None)
    if lire is None:
        return []
    return [c for c in lire().Get(True) if c is not None]
