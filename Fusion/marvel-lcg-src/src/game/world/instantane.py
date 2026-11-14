"""Instantane du monde : l'etat memorise, restaure EN PLACE.

AJOUT LOCAL (29/10/2026) : le bouton « Annuler » rejouait toute la partie
depuis zero. Ici, on memorise l'etat de chaque objet du jeu au moment de la
question du tour (« que fais-tu ? »), et on le remet tel quel pour annuler.

⚠ UNE COPIE (`copy.deepcopy`) ne convient PAS, et ce n'est pas qu'une
question de verrous de thread. Les capacites des cartes sont des lambdas qui
CAPTURENT les objets du graphe d'origine, et `deepcopy` ne copie pas les
fermetures : les effets du monde copie agiraient sur l'ancien monde, sans
aucune erreur. On garde donc les MEMES objets et on leur rend leur contenu
(`__dict__`, listes, dicts, sets, cellules de fermeture). Les fermetures
restent valides, l'identite des objets ne bouge pas.

⚠ CE QUI N'EST PAS DANS LE GRAPHE. Le parcours ne descend que dans les classes
du jeu (`game`, `cards`, `core`) et les conteneurs standard. Le reste est
opaque, laisse tel quel : le moteur (`engine`), le reseau, les verrous, le
rendu. L'etat du hasard, l'historique des reponses et le module d'annulation
ne sont pas des objets du jeu : `EtatExterieur` les prend a la main.
"""
import collections
import enum
import gc
import types
from typing import Any, Callable, List, Optional, Sequence, Tuple

_RACINES_SUIVIES = frozenset(("game", "cards", "core"))
_CellType = type((lambda x: lambda: x)(0).__closure__[0])

# Genres d'entree memorisee.
_DICT, _LISTE, _ENSEMBLE, _FILE, _OBJET, _CELLULE = range(6)
# Genres de parcours qui ne memorisent rien par eux-memes.
_G_IGNORE, _G_TUPLE, _G_FONCTION, _G_METHODE, _G_PARTIAL = range(6, 11)
# Sous-classes de dict/list du jeu : leur `__dict__` compte aussi.
_TYPES_AVEC_ETAT_EN_PLUS: set = set()
_GENRE_PAR_TYPE: dict = {}
_ATOMES = (int, float, str, bytes, bool, type(None), complex, range,
           types.BuiltinFunctionType, types.CodeType, type)


def _classe_suivie(classe: type) -> bool:
    """Un objet de cette classe porte-t-il de l'etat du jeu ?"""
    if issubclass(classe, (enum.Enum, type, types.ModuleType)):
        return False
    return classe.__module__.split(".", 1)[0] in _RACINES_SUIVIES


def _noms_de_slots(classe: type) -> List[str]:
    noms: List[str] = []
    for c in classe.__mro__:
        slots = c.__dict__.get("__slots__", ())
        if isinstance(slots, str):
            slots = (slots,)
        for nom in slots:
            if nom in ("__dict__", "__weakref__"):
                continue
            if nom.startswith("__") and not nom.endswith("__"):
                nom = f"_{c.__name__.lstrip('_')}{nom}"
            noms.append(nom)
    return noms


def _genre_du_type(t: type) -> int:
    """Que faire d'un objet de ce type ? (calcule une fois par type, voir `_GENRE_PAR_TYPE`)"""
    if issubclass(t, _ATOMES):
        return _G_IGNORE
    if issubclass(t, (dict, list, set)):
        if t not in (dict, list, set) and _classe_suivie(t):
            _TYPES_AVEC_ETAT_EN_PLUS.add(t)
        return _DICT if issubclass(t, dict) else _LISTE if issubclass(t, list) else _ENSEMBLE
    if issubclass(t, collections.deque):
        return _FILE
    if issubclass(t, (tuple, frozenset)):
        return _G_TUPLE
    if issubclass(t, types.FunctionType):
        return _G_FONCTION
    if issubclass(t, types.MethodType):
        return _G_METHODE
    if issubclass(t, _CellType):
        return _CELLULE
    if t.__module__ == "functools" and hasattr(t, "func"):
        return _G_PARTIAL
    return _OBJET if _classe_suivie(t) else _G_IGNORE


class Instantane:
    """Le contenu de chaque objet atteignable depuis les racines."""

    def __init__(self, racines: Sequence[Any], exclus: Sequence[Any] = ()) -> None:
        self.entrees: List[Tuple[int, Any, Any]] = []
        self._prendre(racines, {id(x) for x in exclus})

    def __len__(self) -> int:
        return len(self.entrees)

    def _prendre(self, racines: Sequence[Any], exclus: set) -> None:
        # Mesure du 30/10/2026 : le temps part dans les `isinstance` en cascade et dans le ramasse-miettes (des
        # dizaines de milliers de tuples alloues). D'ou le genre de chaque TYPE memorise une fois, et le GC suspendu.
        vus = set(exclus)
        pile = list(racines)
        entrees = self.entrees
        genre_de = _GENRE_PAR_TYPE
        gc_actif = gc.isenabled()
        gc.disable()
        try:
            while pile:
                o = pile.pop()
                i = id(o)
                if i in vus:
                    continue
                t = type(o)
                genre = genre_de.get(t)
                if genre is None:
                    genre = genre_de[t] = _genre_du_type(t)
                if genre == _G_IGNORE:
                    continue
                vus.add(i)

                if genre == _DICT:
                    entrees.append((_DICT, o, dict.copy(o)))
                    pile.extend(dict.keys(o))
                    pile.extend(dict.values(o))
                elif genre == _LISTE:
                    copie = list.copy(o)
                    entrees.append((_LISTE, o, copie))
                    pile.extend(copie)
                elif genre == _ENSEMBLE:
                    copie = set.copy(o)
                    entrees.append((_ENSEMBLE, o, copie))
                    pile.extend(copie)
                elif genre == _FILE:
                    copie = list(o)
                    entrees.append((_FILE, o, copie))
                    pile.extend(copie)
                elif genre == _G_TUPLE:
                    pile.extend(o)
                elif genre == _G_FONCTION:
                    if o.__closure__:
                        pile.extend(o.__closure__)
                    if o.__defaults__:
                        pile.extend(o.__defaults__)
                    if o.__kwdefaults__:
                        pile.append(o.__kwdefaults__)
                elif genre == _G_METHODE:
                    pile.append(o.__self__)
                    pile.append(o.__func__)
                elif genre == _CELLULE:
                    try:
                        contenu = o.cell_contents
                    except ValueError:
                        continue
                    entrees.append((_CELLULE, o, contenu))
                    pile.append(contenu)
                elif genre == _G_PARTIAL:
                    pile.append(o.func)
                    pile.extend(o.args)
                    pile.append(o.keywords)
                else:
                    self._objet(o, pile, entrees)
                if t in _TYPES_AVEC_ETAT_EN_PLUS and hasattr(o, "__dict__"):
                    self._objet(o, pile, entrees)
        finally:
            if gc_actif:
                gc.enable()

    @staticmethod
    def _objet(o: Any, pile: list, entrees: list) -> None:
        etat = getattr(o, "__dict__", None)
        copie = dict(etat) if etat is not None else {}
        slots = {}
        for nom in _noms_de_slots(type(o)):
            try:
                slots[nom] = object.__getattribute__(o, nom)
            except AttributeError:
                pass
        entrees.append((_OBJET, o, (copie, slots)))
        pile.extend(copie.values())
        pile.extend(slots.values())

    def restaurer(self) -> None:
        """Rend a chaque objet le contenu qu'il avait a la prise."""
        for genre, o, sauve in self.entrees:
            if genre == _DICT:
                dict.clear(o)
                dict.update(o, sauve)
            elif genre == _LISTE:
                list.__setitem__(o, slice(None), sauve)
            elif genre == _ENSEMBLE:
                set.clear(o)
                set.update(o, sauve)
            elif genre == _FILE:
                o.clear()
                o.extend(sauve)
            elif genre == _CELLULE:
                o.cell_contents = sauve
            else:
                copie, slots = sauve
                etat = getattr(o, "__dict__", None)
                if etat is not None:
                    etat.clear()
                    etat.update(copie)
                for nom, valeur in slots.items():
                    object.__setattr__(o, nom, valeur)


class EtatExterieur:
    """Ce que l'annulation doit aussi remettre, et qui n'est pas dans le graphe.

    Le hasard (sinon un melange apres l'annulation ne redonne pas le meme
    ordre qu'une partie rejouee), l'historique des reponses (sinon une
    sauvegarde rejouerait des actions annulees) et les repères du module
    d'annulation.
    """

    def __init__(self, controller_manager: Any) -> None:
        from engine.lib import Random
        self.cm = controller_manager
        replay = controller_manager.replay
        undo = controller_manager.undo
        self.historique = list(replay.history_inputs)
        self.pas = (replay.current_step_id, replay.replay_step_id)
        self.crc = list(replay.calculated_crc)
        self.undo = (undo.last_step, undo.next_step, undo.debut_action, undo.joueur_action)
        self.hasard_compteur = Random.counter
        self.hasard_etats = len(Random.states)
        self.hasard_numpy = None
        try:
            import numpy.random
            self.hasard_numpy = numpy.random.get_state()
        except Exception:
            pass

    def restaurer(self) -> None:
        from engine.lib import Random
        replay = self.cm.replay
        undo = self.cm.undo
        replay.history_inputs[:] = self.historique
        replay.current_step_id, replay.replay_step_id = self.pas
        replay.calculated_crc[:] = self.crc
        undo.last_step, undo.next_step, undo.debut_action, undo.joueur_action = self.undo
        Random.counter = self.hasard_compteur
        del Random.states[self.hasard_etats:]
        if self.hasard_numpy is not None:
            import numpy.random
            numpy.random.set_state(self.hasard_numpy)


class SignalRestaurer(BaseException):
    """Leve par `/undo` pour defaire la pile d'appels jusqu'a la question du tour.

    ⚠ `BaseException`, pas `Exception` : le jeu est plein de `except Exception`
    qui avaleraient un signal de flux. Seule la boucle du tour l'attrape.
    """

    def __init__(self, en_action: bool) -> None:
        super().__init__("SignalRestaurer")
        self.en_action = en_action


class PileInstantanes:
    """Les instantanes d'UN tour de joueur, du plus ancien au plus recent.

    Chacun est pris a la question du tour, avant que le joueur ne choisisse :
    « annuler » remet donc la partie telle qu'elle etait avant une action.
    Elle meurt avec la boucle du tour : la pile d'appels qu'elle suppose (ce
    joueur, ce round) n'existe plus apres, on retombe alors sur le rejeu.
    """

    # ~18 Mo par instantane (mesure du 29/10/2026, ~50 000 objets) : 40 en empilaient 720 Mo, presque le double de la
    # memoire du moteur, et le serveur allume un moteur PAR PARTIE. Au-dela, « Annuler » retombe sur le rejeu.
    PROFONDEUR_MAX = 10

    def __init__(self) -> None:
        self.pile: List[Tuple[Instantane, EtatExterieur, tuple]] = []

    def prendre(self, racines: Sequence[Any], exclus: Sequence[Any],
                controller_manager: Any, locales: tuple) -> None:
        self.pile.append((Instantane(racines, exclus), EtatExterieur(controller_manager), locales))
        del self.pile[:-self.PROFONDEUR_MAX]

    def peut_annuler(self, en_action: bool) -> bool:
        return len(self.pile) >= (1 if en_action else 2)

    def restaurer(self, en_action: bool) -> tuple:
        """Remet l'etat voulu, retire les instantanes devenus faux, rend les locales.

        En pleine action, c'est le dernier (la question qui l'a lancee). A la
        question du tour, le dernier est l'etat present : on remonte d'un cran.
        """
        if not en_action:
            self.pile.pop()
        instantane, exterieur, locales = self.pile.pop()
        instantane.restaurer()
        exterieur.restaurer()
        return locales
