from cards.pack import *

# ===========================================================================
# Helpers partages du set « Casey Jones » (Inkwire, TMNT Heroes, prefixe `tc`).
#
# ⚠ Un helper vit DANS le `__init__.py` DU SET (lecon hk005) : defini dans
# `cards/pack/casey_jones/__init__.py`, il leverait un NameError avale par le
# moteur.
#
# LES ARMES ET LE SAC
#   - « WEAPON » (tc001a, tc001b, tc013) : n'importe quelle amelioration au
#     trait WEAPON (celles de Raphael, de Leonardo... comptent aussi).
#   - « a Casey Jones WEAPON upgrade » (tc002 Clap Back, tc006 Anything Goes) :
#     une arme DU SET « Casey Jones » (cinq cartes : tc007, tc009-tc012).
#
#     TODO-QUESTION (.planning/tmnt/casey-questions.md, Q1) : « Casey Jones
#     WEAPON » = arme du SET Casey Jones (lecture retenue, precedent `hd013`
#     « a Howard the Duck card » = `set_name`), ou toute arme que Casey
#     controle ? La premiere est la plus fidele : sinon le mot « Casey Jones »
#     n'aurait aucune fonction, « WEAPON upgrade you control » suffirait.
#   - Le Sac (tc013) range des cartes SOUS lui (`TuckCardUnderHere`,
#     mots-cles/tuck.md) ; on les relit par `GetPlacedCardArea()`.
# ===========================================================================

ENSEMBLE_CASEY = "Casey Jones"
ID_SAC = "tc013"          # Casey's Bag
TRAIT_ARME = "WEAPON"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele sunfire).

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


def EstUneArme(face: 'CardFace|None') -> bool:
    """« a WEAPON upgrade » : type Upgrade ET trait WEAPON."""
    return face is not None and Upgrade.IsType(face) and face.HasTrait(TRAIT_ARME)


def EstUneArmeDeCasey(face: 'CardFace|None') -> bool:
    """« a Casey Jones WEAPON upgrade » : une arme du set « Casey Jones »."""
    if not EstUneArme(face):
        return False
    paper = getattr(face, "paper", None)
    return paper is not None and getattr(paper, "set_name", None) == ENSEMBLE_CASEY


def ArmesSousControle(joueur: 'Player|None') -> List['CardFace']:
    """« a WEAPON upgrade you control » (en jeu, sous le controle du joueur)."""
    if joueur is None:
        return []
    return [f for f in joueur.GetControlUpgrade() if EstUneArme(f)]


def ArmesDeCaseySousControle(joueur: 'Player|None') -> List['CardFace']:
    """« a Casey Jones WEAPON upgrade you control »."""
    return [f for f in ArmesSousControle(joueur) if EstUneArmeDeCasey(f)]


def SacDuJoueur(joueur: 'Player|None') -> 'CardFace|None':
    """Casey's Bag (tc013) en jeu sous le controle du joueur, ou None.

    ⚠ Le filtre est le card_id, jamais le nom.
    """
    if joueur is None:
        return None
    for face in joueur.GetControlUpgrade():
        paper = getattr(face, "paper", None)
        if paper is not None and paper.card_id == ID_SAC and face.IsInPlay():
            return face
    return None


def CartesRangeesSousLeSac(joueur: 'Player|None') -> List['CardFace']:
    """Les cartes glissees sous Casey's Bag (liste vide s'il n'est pas en jeu)."""
    sac = SacDuJoueur(joueur)
    if sac is None:
        return []
    return list(sac.GetPlacedCardArea().Get())


def ArmesDeCaseyRangeesSousLeSac(joueur: 'Player|None') -> List['CardFace']:
    """« a Casey Jones WEAPON upgrade tucked under Casey's Bag »."""
    return [f for f in CartesRangeesSousLeSac(joueur) if EstUneArmeDeCasey(f)]


def ArmeLaPlusBasseDeLaDefausse(joueur: 'Player|None') -> 'CardFace|None':
    """« the bottommost WEAPON upgrade in your discard pile ».

    `discard_pile.Get()` rend la defausse du FOND vers le dessus
    (`Deck.GetAll(from_top=False)`, deck.py:381) : le premier element qui est une
    arme est donc la plus basse (meme lecture que `hd013`).
    """
    if joueur is None:
        return None
    for face in joueur.discard_pile.Get():
        if EstUneArme(face):
            return face
    return None


# ---------------------------------------------------------------------------
# « If a Casey Jones WEAPON upgrade was discarded TO PAY FOR THIS CARD »
# (tc002 Clap Back). La seule facon de defausser une arme POUR PAYER est
# Overswing (tc001a) : son cout defausse l'arme, puis la capacite verse ses
# ressources dans la reserve qui paie la carte. `DoGenerateResources` appelle
# `ex_operation` APRES le cout, avec `message.for_effect` = l'effet de la carte
# PAYEE : c'est la que Overswing consigne le fait, et Clap Back le relit.
# ---------------------------------------------------------------------------

def ConsignerArmeDefausseePourPayer(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
    """A appeler en `ex_operation` d'Overswing : releve les cartes que le cout
    `CostFunc.Discard` vient de defausser et marque la carte payee si l'une
    d'elles est une arme de Casey."""
    payee = message.for_effect
    for cout in message.cost_check_effect.cost_func.GetAll():
        for face in getattr(cout, "return_discarded_cards", None) or []:
            if EstUneArmeDeCasey(face):
                armes = getattr(payee, "armes_de_casey_defaussees", None)
                if armes is None:
                    armes = []
                    payee.armes_de_casey_defaussees = armes
                armes.append(face)


def ArmeDeCaseyDefausseePourPayer(effect: 'Effect') -> bool:
    """Clap Back : une arme de Casey a-t-elle ete defaussee pour payer CETTE carte ?"""
    return bool(getattr(effect, "armes_de_casey_defaussees", None))
