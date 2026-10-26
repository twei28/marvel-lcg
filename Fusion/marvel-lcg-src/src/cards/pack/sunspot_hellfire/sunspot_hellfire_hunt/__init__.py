from cards.pack import *

# ===========================================================================
# LES COMPTEURS `solar` — helpers partages du pack SUNSPOT (Dipsome, `so`).
#
# MEME MONTAGE QUE `spider_woman_kajislav` (`sw`, compteurs `psionic web`) : le stock vit
# sur l'IDENTITE, jamais sur la face courante, et survit au changement de forme
# (« place 5 solar counters here » sur Roberto, « remove X solar counters from Sunspot » sur le heros :
# c'est la MEME carte, `joueur.GetIdentity()`).
#
# ⚠ AUCUN PLAFOND imprime sur les compteurs solaires (contrairement a `psionic web` : 10).
# ⚠ Le compteur `solar` est une entree a part de `CardFace.COUNTER` (CORRECTIF du 26/10/2026).
# ===========================================================================
COMPTEUR = 'solar'


def JoueurQuiControle(effect: 'Effect') -> "Player|None":
    """Le joueur qui controle la carte porteuse, ou None si ce n'en est pas un (cf. `sw`)."""
    proprietaire = effect.this.GetControlBy()
    return proprietaire if Player.IsType(proprietaire) else None


def IdentiteDe(joueur: 'Player') -> "CardFace|None":
    """L'identite du joueur, quelle que soit sa forme : le stock ne se perd pas au changement de forme."""
    if joueur is None:
        return None
    return joueur.GetIdentity()


def SolairesDe(joueur: 'Player') -> int:
    """Combien de compteurs solaires porte l'identite de ce joueur."""
    identite = IdentiteDe(joueur)
    if identite is None:
        return 0
    return identite.CastTo(CanPlaceCounter).GetCounters(COMPTEUR)


def PoserSolaires(joueur: 'Player', nombre: int, effect: 'Effect') -> int:
    """« place N solar counters on your identity » (aucun plafond imprime)."""
    identite = IdentiteDe(joueur)
    if identite is None or nombre <= 0:
        return 0
    return Faces.PlaceCountersOn([identite], nombre, COMPTEUR, effect) or 0


def RetirerSolaires(joueur: 'Player', nombre: int, effect: 'Effect') -> int:
    """Retire jusqu'a `nombre` compteurs et rend ce qui est VRAIMENT parti (la valeur rendue compte, pas la demandee)."""
    identite = IdentiteDe(joueur)
    if identite is None or nombre <= 0:
        return 0
    retire = min(nombre, SolairesDe(joueur))
    if retire <= 0:
        return 0
    return Faces.RemoveCountersOn([identite], retire, COMPTEUR, effect) or 0


def DemanderCombien(joueur: 'Player', effect: 'Effect') -> int:
    """« Remove X solar counters » : X est un CHOIX du joueur, borne au stock reel (cf. `sw`, `AskChooseOneText`)."""
    stock = SolairesDe(joueur)
    if stock <= 0:
        return 0
    return joueur.AskChooseOneText(list(range(stock, -1, -1)))


def EstAerien(joueur: 'Player') -> bool:
    """« If Sunspot has the AERIAL trait » / « if you have the AERIAL trait » : le trait vient de Solar Soar (so011)."""
    identite = IdentiteDe(joueur)
    if identite is None:
        return False
    return identite.HasTrait("AERIAL")
