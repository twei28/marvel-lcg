"""Le SERVEUR DE PUZZLES (E7, docs/puzzle/PLAN.md) : publier, lire par code, modifier, supprimer.

Module autonome (bibliothèque standard, SQLite), sans HTTP : `orchestrateur.py` n'y met que les
routes. Les règles :

- **Un puzzle publié vient d'un inconnu.** Il passe `validate_puzzle` (le même contrôle strict que
  le moteur, chargé depuis ses sources) À LA PUBLICATION ET À LA LECTURE, avec une LISTE BLANCHE de
  commandes `Puzzle.<Méthode>` : pas de `Win`, pas de `Lose`, rien qui sorte de la mise en place.
  Toute carte nommée dans une zone doit exister au catalogue.
- **Un code court** (type `PZ-A4F9`, alphabet sans caractères ambigus) et une **clé d'édition**
  secrète, rendue UNE SEULE FOIS : seule son empreinte est gardée.
- **Aucune donnée personnelle** : un pseudo libre, rien d'autre.
- **28 jours** : un puzzle est supprimé 28 jours après le dernier jour où quelqu'un l'a joué (la
  création compte comme un premier jeu ; `lire(code, jouer=True)` remet le compteur à zéro).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import secrets
import sqlite3
import time
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any, Callable, Collection, Dict, List, Optional

CONSERVATION_JOURS = 28
TAILLE_MAX_OCTETS = 300_000
PSEUDO_MAX = 30
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"   # ni I, L, O, U, ni 0, 1
LONGUEUR_CODE = 4
JOUR = 86400

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
VALIDATION = os.path.join(MOTEUR, "src", "game", "puzzle", "puzzle_validation.py")

# Les seules commandes qu'un puzzle publié peut appeler : de la MISE EN PLACE. Aucune ne termine
# la partie (Win, Lose, End), ne valide un objectif (ValidateObjective) ni ne sort de la table
# (AssembleeAutreTable). Les noms viennent de `puzzle_capture.py` et de `puzzle-brouillon.js`.
COMMANDES_PERMISES = frozenset("""
CreateEncounterDeck CreateEncounterDiscardPile CreateHandCards CreatePlayerDeck CreatePlayerDiscardPile
CreatePlayerAdditionalDeck SetFirstPlayer RestoreCard RestoreState AdvanceVillain AdvanceMainScheme
SetHealth SetThreat Damage Heal Stun Confuse Tough Cloak Daze Expose AddStatus AddTough AddCloak Intensify
Exhaust Ready Counter Token PlaceCounters PlaceThreat PutIntoPlay PlaceUnder Attach AttachReel Engage
MoveTo Shuffle Flip ChangeForm ChangeToFace Draw Gain Discard Remove EmptyHand EmptyPlayerDeck
EmptyPlayerDiscardPile EmptyEncounterDeck EmptyEncounterDiscardPile
""".split())

# Les valeurs par défaut d'un fichier de puzzle (celles de `PuzzleData`, puzzle_data.py : un test du
# moteur, outils/test_puzzle_format.py, vérifie qu'elles ne dérivent pas).
DEFAUTS: Dict[str, Any] = {
    "version": "", "author": "", "cover": "", "comment": "", "seed": 0, "villain": [], "schemes": [],
    "encounter_deck": [], "encounter_discard_pile": [], "set_aside": [], "expert": False, "players": [],
    "puzzle_command": [], "format": 1, "title": "", "description": "", "difficulty": 0, "hints": [],
    "objectives": [], "objectives_mode": "all", "start_phase": "", "start_step": "", "first_player": 0,
    "solution_visibility": "after", "has_solution": False,
}
DEFAUTS_JOUEUR: Dict[str, Any] = {
    "identities": [], "hand_cards": [], "player_deck": [], "player_discard_pile": [], "set_aside": [],
    "deck_name": "",
}
DEFAUTS_OBJECTIF: Dict[str, Any] = {"kind": "", "target": "", "text": ""}


class ErreurPuzzle(ValueError):
    """Un puzzle refusé ; `args[0]` est la liste des raisons, lisible par le créateur."""

    def __init__(self, raisons: List[str], statut: int = 400) -> None:
        super().__init__(raisons)
        self.raisons = raisons
        self.statut = statut


def _charger_validation():
    spec = importlib.util.spec_from_file_location("puzzle_validation_serveur", VALIDATION)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cartes_du_catalogue() -> frozenset:
    """Les identifiants de carte connus du jeu (data/cards.json)."""
    with open(os.path.join(MOTEUR, "data", "cards.json"), encoding="utf-8") as f:
        donnees = json.load(f)
    ids = set()

    def parcourir(x: Any) -> None:
        if isinstance(x, dict):
            if "card_id" in x and "type" in x:
                ids.add(str(x["card_id"]))
            else:
                for v in x.values():
                    parcourir(v)
        elif isinstance(x, list):
            for v in x:
                parcourir(v)

    parcourir(donnees)
    return frozenset(ids)


def _objet(valeur: Any, defauts: Dict[str, Any]) -> SimpleNamespace:
    """Un dictionnaire de puzzle -> un objet que `validate_puzzle` sait lire ; clés inconnues ignorées."""
    if not isinstance(valeur, dict):
        raise ErreurPuzzle(["le puzzle doit être un objet JSON"])
    return SimpleNamespace(**{cle: valeur.get(cle, defaut) for cle, defaut in defauts.items()})


def puzzle_en_objet(donnees: Any) -> SimpleNamespace:
    puzzle = _objet(donnees, DEFAUTS)
    puzzle.players = [_objet(j, DEFAUTS_JOUEUR) for j in puzzle.players] if isinstance(puzzle.players, list) else puzzle.players
    puzzle.objectives = [_objet(o, DEFAUTS_OBJECTIF) for o in puzzle.objectives] if isinstance(puzzle.objectives, list) else puzzle.objectives
    return puzzle


def _pseudo(texte: Any) -> str:
    propre = re.sub(r"[\x00-\x1f\x7f<>]", "", str(texte or "")).strip()
    return propre[:PSEUDO_MAX] or "Anonyme"


def _empreinte(cle: str) -> str:
    return hashlib.sha256(cle.encode("utf-8")).hexdigest()


class PuzzlesPublies:
    def __init__(self, base: str, *, cartes: Optional[Collection[str]] = None,
                 horloge: Callable[[], float] = time.time) -> None:
        self.base = base
        self.horloge = horloge
        self.cartes = frozenset(cartes) if cartes is not None else cartes_du_catalogue()
        self._validation = _charger_validation()
        with self._connexion() as cx:
            cx.execute("""CREATE TABLE IF NOT EXISTS puzzles_publies (
                code TEXT PRIMARY KEY, cle TEXT NOT NULL, pseudo TEXT NOT NULL, titre TEXT NOT NULL,
                contenu TEXT NOT NULL, cree REAL NOT NULL, modifie REAL NOT NULL,
                dernier_jeu REAL NOT NULL, nb_jeux INTEGER NOT NULL DEFAULT 0)""")

    @contextmanager
    def _connexion(self):
        cx = sqlite3.connect(self.base, timeout=10)
        cx.row_factory = sqlite3.Row
        try:
            yield cx
            cx.commit()
        except BaseException:
            cx.rollback()
            raise
        finally:
            cx.close()

    # ---------------------------------------------------------------- contrôle
    def controler(self, donnees: Any) -> Dict[str, Any]:
        """Rend le puzzle (dictionnaire) s'il est acceptable ; lève `ErreurPuzzle` sinon."""
        if not isinstance(donnees, dict):
            raise ErreurPuzzle(["le puzzle doit être un objet JSON"])
        if len(json.dumps(donnees, ensure_ascii=False).encode("utf-8")) > TAILLE_MAX_OCTETS:
            raise ErreurPuzzle([f"puzzle trop gros (plus de {TAILLE_MAX_OCTETS // 1000} Ko)"], 413)
        if donnees.get("format") != 2:
            raise ErreurPuzzle(["seul le format 2 se publie"])
        puzzle = puzzle_en_objet(donnees)
        raisons = list(self._validation.validate_puzzle(puzzle, COMMANDES_PERMISES))
        if not raisons:
            for nom, zone in self._zones(puzzle):
                for carte in zone:
                    for face in str(carte).split(","):
                        if face not in self.cartes:
                            raisons.append(f"{nom} : carte inconnue ({face[:20]!r})")
                            break
        if not puzzle.title.strip() and not raisons:
            raisons.append("titre : un titre est demandé")
        if raisons:
            raise ErreurPuzzle(raisons[:30])
        # On ne garde que les champs connus : rien d'autre ne traverse le serveur.
        propre = {cle: donnees.get(cle, defaut) for cle, defaut in DEFAUTS.items()}
        propre["players"] = [{cle: j.get(cle, defaut) for cle, defaut in DEFAUTS_JOUEUR.items()} for j in donnees["players"]]
        propre["objectives"] = [{cle: o.get(cle, defaut) for cle, defaut in DEFAUTS_OBJECTIF.items()} for o in donnees["objectives"]]
        return propre

    @staticmethod
    def _zones(puzzle: SimpleNamespace):
        yield "méchant", puzzle.villain
        yield "complots", puzzle.schemes
        yield "deck rencontre", puzzle.encounter_deck
        yield "défausse rencontre", puzzle.encounter_discard_pile
        yield "mis de côté", puzzle.set_aside
        for i, joueur in enumerate(puzzle.players, start=1):
            yield f"héros {i} (identités)", joueur.identities
            yield f"héros {i} (main)", joueur.hand_cards
            yield f"héros {i} (deck)", joueur.player_deck
            yield f"héros {i} (défausse)", joueur.player_discard_pile
            yield f"héros {i} (mis de côté)", joueur.set_aside

    # ---------------------------------------------------------------- publier
    def _nouveau_code(self, cx: sqlite3.Connection) -> str:
        for _ in range(50):
            code = "PZ-" + "".join(secrets.choice(ALPHABET) for _ in range(LONGUEUR_CODE))
            if not cx.execute("SELECT 1 FROM puzzles_publies WHERE code = ?", (code,)).fetchone():
                return code
        raise ErreurPuzzle(["plus de code libre, réessaie"], 503)

    def publier(self, donnees: Any, pseudo: Any = "") -> Dict[str, Any]:
        """Publie un puzzle. Rend `{code, cle, expire_le}` ; `cle` n'est rendue qu'ici."""
        propre = self.controler(donnees)
        auteur = _pseudo(pseudo)
        propre["author"] = auteur
        maintenant = self.horloge()
        cle = secrets.token_urlsafe(18)
        with self._connexion() as cx:
            code = self._nouveau_code(cx)
            cx.execute("INSERT INTO puzzles_publies (code, cle, pseudo, titre, contenu, cree, modifie, dernier_jeu) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (code, _empreinte(cle), auteur, propre["title"], json.dumps(propre, ensure_ascii=False),
                        maintenant, maintenant, maintenant))
        return {"code": code, "cle": cle, "expire_le": maintenant + CONSERVATION_JOURS * JOUR}

    # ---------------------------------------------------------------- lire
    @staticmethod
    def _normaliser(code: Any) -> str:
        texte = re.sub(r"[^A-Za-z0-9]", "", str(code or "")).upper()
        return "PZ-" + texte[2:] if texte.startswith("PZ") else "PZ-" + texte

    def lire(self, code: Any, jouer: bool = False) -> Optional[Dict[str, Any]]:
        """Le puzzle et ses métadonnées, ou None. `jouer=True` remet le compteur de 28 jours à zéro.

        Le contenu est CONTRÔLÉ À NOUVEAU : le validateur ou le catalogue ont pu évoluer depuis la
        publication, et un puzzle devenu invalide ne doit pas être servi.
        """
        code = self._normaliser(code)
        with self._connexion() as cx:
            ligne = cx.execute("SELECT * FROM puzzles_publies WHERE code = ?", (code,)).fetchone()
            if ligne is None:
                return None
            maintenant = self.horloge()
            if ligne["dernier_jeu"] + CONSERVATION_JOURS * JOUR < maintenant:
                return None
            puzzle = self.controler(json.loads(ligne["contenu"]))
            if jouer:
                cx.execute("UPDATE puzzles_publies SET dernier_jeu = ?, nb_jeux = nb_jeux + 1 WHERE code = ?",
                           (maintenant, code))
                dernier = maintenant
            else:
                dernier = ligne["dernier_jeu"]
        return {"code": code, "puzzle": puzzle, "pseudo": ligne["pseudo"], "cree": ligne["cree"],
                "modifie": ligne["modifie"], "nb_jeux": ligne["nb_jeux"] + (1 if jouer else 0),
                "expire_le": dernier + CONSERVATION_JOURS * JOUR}

    # ---------------------------------------------------------------- modifier, supprimer
    def _ligne_du_proprietaire(self, cx: sqlite3.Connection, code: str, cle: Any) -> sqlite3.Row:
        ligne = cx.execute("SELECT * FROM puzzles_publies WHERE code = ?", (code,)).fetchone()
        # Même réponse pour « inconnu » et « mauvaise clé » : on ne dit pas quels codes existent.
        if ligne is None or not secrets.compare_digest(ligne["cle"], _empreinte(str(cle or ""))):
            raise ErreurPuzzle(["code ou clé incorrects"], 403)
        return ligne

    def modifier(self, code: Any, cle: Any, donnees: Any) -> Dict[str, Any]:
        code = self._normaliser(code)
        propre = self.controler(donnees)
        with self._connexion() as cx:
            ligne = self._ligne_du_proprietaire(cx, code, cle)
            propre["author"] = ligne["pseudo"]
            maintenant = self.horloge()
            cx.execute("UPDATE puzzles_publies SET titre = ?, contenu = ?, modifie = ? WHERE code = ?",
                       (propre["title"], json.dumps(propre, ensure_ascii=False), maintenant, code))
        return {"code": code, "modifie": maintenant}

    def supprimer(self, code: Any, cle: Any) -> None:
        code = self._normaliser(code)
        with self._connexion() as cx:
            self._ligne_du_proprietaire(cx, code, cle)
            cx.execute("DELETE FROM puzzles_publies WHERE code = ?", (code,))

    # ---------------------------------------------------------------- nettoyage
    def nettoyer(self) -> int:
        """Supprime les puzzles non joués depuis 28 jours. Rend le nombre supprimé."""
        limite = self.horloge() - CONSERVATION_JOURS * JOUR
        with self._connexion() as cx:
            return cx.execute("DELETE FROM puzzles_publies WHERE dernier_jeu < ?", (limite,)).rowcount
