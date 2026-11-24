"""`dataclasses.asdict`, a l'identique, en trois fois moins de temps.

Backlog 22 (« tenir plus de joueurs »), 20/10/2026. Mesure au banc du
descripteur (`outils/banc-descripteur.py`, Spider-Man contre Rhino, graine 1) :
`dataclasses.asdict` sur le descripteur du monde pesait **31 % du temps CPU
d'une table**, plus que la construction du descripteur elle-meme. Il est
appele deux fois par rendu : l'enregistrement de « Revoir sa partie »
(`world_render.py`) et le masque de `/get_world` (`server_sync.py`, une fois
par client et par trame).

POURQUOI LA VERSION STANDARD EST LENTE : pour CHAQUE valeur feuille (un
entier, une chaine, un booleen : des centaines de milliers par rendu), elle
appelle `copy.deepcopy`, qui consulte sa table de dispatch et son memo pour
rendre... la meme valeur, ces types etant immuables (`copy._deepcopy_atomic`).

⚠ LE RESULTAT EST IDENTIQUE, PAS « EQUIVALENT ». Meme algorithme que
`dataclasses._asdict_inner` (Python 3.10), meme ordre des tests et des
cles ; seuls deux raccourcis sont ajoutes, et ils ne changent rien au
resultat :
  - les types atomiques EXACTS (`str`, `int`, `float`, `bool`, `None`,
    `bytes`, `complex`) sont rendus tels quels, comme le ferait
    `copy.deepcopy` ;
  - `list` et `dict` EXACTS (pas leurs sous-classes) sont reconstruits
    directement, ce que ferait la branche generique avec `type(obj)`.
Tout autre objet (sous-classe, tuple nomme, objet quelconque) passe par la
branche generique, copiee de la bibliotheque standard, `copy.deepcopy` compris.
Preuve : empreintes octet pour octet du banc, avant et apres.
"""
import copy
import dataclasses
from typing import Any, Dict, List, Tuple

_ATOMES = frozenset((str, int, float, bool, type(None), bytes, complex))
_CHAMPS: Dict[type, Tuple[str, ...]] = {}


def _noms_des_champs(classe: type) -> Tuple[str, ...]:
    noms = _CHAMPS.get(classe)
    if noms is None:
        noms = tuple(f.name for f in dataclasses.fields(classe))
        _CHAMPS[classe] = noms
    return noms


def _interne(obj: Any) -> Any:
    t = type(obj)
    if t in _ATOMES:
        return obj
    if t is list:
        return [_interne(v) for v in obj]
    if t is dict:
        return {_interne(k): _interne(v) for k, v in obj.items()}
    # Branche generique : `dataclasses._asdict_inner`, dict_factory=dict.
    if hasattr(t, '__dataclass_fields__'):
        resultat: List[Tuple[str, Any]] = []
        for nom in _noms_des_champs(t):
            resultat.append((nom, _interne(getattr(obj, nom))))
        return dict(resultat)
    if isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return t(*[_interne(v) for v in obj])
    if isinstance(obj, (list, tuple)):
        return t(_interne(v) for v in obj)
    if isinstance(obj, dict):
        return t((_interne(k), _interne(v)) for k, v in obj.items())
    return copy.deepcopy(obj)


def asdict_rapide(obj: Any) -> Dict[str, Any]:
    """Comme `dataclasses.asdict(obj)` (sans `dict_factory`), resultat identique."""
    if not hasattr(type(obj), '__dataclass_fields__'):
        raise TypeError("asdict() should be called on dataclass instances")
    return _interne(obj)


# ---------------------------------------------------------------------------
# Conversion ET masque en une seule passe (backlog 22, 20/10/2026, etape 2).
#
# `/get_world` faisait, pour CHAQUE client et a chaque trame : `asdict` (une
# copie complete du descripteur), PUIS `masquer` (un second parcours complet,
# en Python, de la copie). Mesure : ~1 ms pour la copie, ~3 ms pour le second
# parcours, sur ~8 ms par client et par trame. Ici, le masque est applique a
# chaque dictionnaire au moment ou il est construit.
#
# ⚠ MEME RESULTAT QUE `asdict` PUIS `masquer` (server_sync.py), ET VOICI
# POURQUOI. `masquer` decide d'un noeud en ne regardant QUE ce noeud (ses cles
# `visible_for_players` et `name`), jamais son parent : l'ordre (parent avant
# enfants chez `masquer`, enfants avant parent ici) ne change donc rien. Les
# valeurs qu'il pose ('' , {}, 0) sont neuves et vides : rien a masquer
# dedans. Et `masquer` ne descend QUE dans les `dict` et les `list` (sous-
# classes comprises), jamais dans un tuple ni dans les cles : le drapeau
# `descendre` reproduit exactement ce chemin.

def _masquer_noeud(noeud: Dict[Any, Any], autorises: Any) -> None:
    """Le corps de `masquer` (server_sync.py) pour UN noeud, a l'identique."""
    vus = noeud.get('visible_for_players')
    if isinstance(vus, list) and 'name' in noeud and not (set(vus) & autorises):
        noeud['name'] = ''
        noeud['card_id'] = ''
        noeud['pic_id'] = ''
        noeud['card_type'] = ''
        noeud['traits'] = {}
        noeud['info'] = {}
        noeud['buffs'] = {}
        noeud['cost'] = 0


def _interne_masque(obj: Any, autorises: Any, descendre: bool) -> Any:
    t = type(obj)
    if t in _ATOMES:
        return obj
    if not descendre:
        # Hors du chemin de `masquer` (sous un tuple) : conversion seule.
        return _interne(obj)
    if t is list:
        return [_interne_masque(v, autorises, True) for v in obj]
    if t is dict:
        d = {_interne(k): _interne_masque(v, autorises, True) for k, v in obj.items()}
        _masquer_noeud(d, autorises)
        return d
    if hasattr(t, '__dataclass_fields__'):
        # `dict_factory=dict` : le resultat est un `dict`, donc masque.
        resultat: List[Tuple[str, Any]] = []
        for nom in _noms_des_champs(t):
            resultat.append((nom, _interne_masque(getattr(obj, nom), autorises, True)))
        d = dict(resultat)
        _masquer_noeud(d, autorises)
        return d
    if isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return t(*[_interne(v) for v in obj])
    if isinstance(obj, tuple):
        return t(_interne(v) for v in obj)
    if isinstance(obj, list):
        return t(_interne_masque(v, autorises, True) for v in obj)
    if isinstance(obj, dict):
        d = t((_interne(k), _interne_masque(v, autorises, True)) for k, v in obj.items())
        _masquer_noeud(d, autorises)
        return d
    return copy.deepcopy(obj)


def asdict_masque(obj: Any, autorises: Any) -> Dict[str, Any]:
    """`asdict(obj)` puis le masque de `/get_world` pour `autorises` : meme resultat, une passe."""
    if not hasattr(type(obj), '__dataclass_fields__'):
        raise TypeError("asdict() should be called on dataclass instances")
    return _interne_masque(obj, autorises, True)
