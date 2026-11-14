from cards.pack import *
import math

# ===========================================================================
# Set modulaire NEGA-BOMB (Galactic Storm, Kajislav) — gs222a/gs222b, gs223.
# Insert du set : « The Nega-Bomb modular encounter set includes the Nega-Bomb
# side scheme. This side scheme has the setup keyword, so it always begins the
# game in play. This modular encounter set can be included in any scenario, but
# it does not count toward the number of modular encounter sets required. »
# Trois cartes : le complot annexe Nega-Bomb (recto 222A) / Detonation (verso
# 222B, Environnement) et deux Green Interference.
#
# En CAMPAGNE (scenario 5, livret 1.2) la Nega-Bomb entre en jeu avec X menaces
# par joueur, X = la valeur notee en « Time Pressure » : c'est le lot GS-9
# (campagne), pas ce set. Hors campagne, la menace imprimee (8 par joueur) vaut.
# ===========================================================================

ATTR_MENACE = "gs_menace_detonation"


def PersonnagesAmisEtSbires(effect: 'Effect') -> List['CardFace']:
    """« each friendly character and minion in play » : identites (heros ou alter ego) et allies des
    joueurs, et tous les sbires en jeu."""
    faces: List['CardFace'] = []
    for joueur in Worlds.GetPlayers(effect):
        faces += list(joueur.GetControlCharacters())
    faces += [f for f in Worlds.GetOnFieldCards(effect) if Minion.IsType(f) and f.IsInPlay()]
    vus: List['CardFace'] = []
    for f in faces:
        if f not in vus:
            vus.append(f)
    return vus


def DegatsDeDetonation(menace: int, nombre: int) -> int:
    """« X is equal to the amount of threat here divided by the total number of friendly characters and
    minions in play (rounded up) »."""
    if nombre <= 0 or menace <= 0:
        return 0
    return int(math.ceil(menace / nombre))


def CompteursPolyvalents(face: 'CardFace') -> List[str]:
    """Les noms des compteurs (« all-purpose counters », FAQ officielle MC4DB du 29/09/2026 : la carte qui
    porte le compteur en definit le type) presents sur une carte, avec leur nombre > 0."""
    try:
        noms = list(face.components.counter.GetCounterNames())
    except AttributeError:
        return []
    # « damage » / « threat » nommes en compteurs par quelques packs representent des JETONS de degats ou
    # de menace, pas des compteurs polyvalents : exclus.
    return [n for n in noms if n not in ("damage", "threat") and face.components.counter.GetCounters(n) > 0]


def RetirerUnCompteur(face: 'CardFace', effect: 'Effect') -> bool:
    noms = CompteursPolyvalents(face)
    if not noms:
        return False
    Faces.RemoveCountersOn([face], 1, noms[0], effect)
    return True
