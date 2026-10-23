"""L'API HTTP des puzzles publiés (E7), sans serveur : `traiter` rend (statut, corps, en-têtes).

`orchestrateur.py` lit la requête, appelle `traiter`, écrit la réponse. Tout ce qui se décide ici
se teste sans réseau (site/test_api_puzzles.py).

Routes (JSON) :
    GET  /api/puzzle/PZ-XXXX[?jouer=1]      lire (jouer=1 remet le compteur de 28 jours à zéro)
    POST /api/puzzle/publier                {puzzle, pseudo}  -> 201 {code, cle, expire_le}
    POST /api/puzzle/PZ-XXXX/modifier       {cle, puzzle}
    POST /api/puzzle/PZ-XXXX/supprimer      {cle}

⚠ CORS : le créateur tourne sur la table (`p<N>.<domaine>`), le serveur sur le site. On répond
à l'origine DEMANDÉE seulement si c'est le domaine, un de ses sous-domaines, ou le jeu local ;
jamais `*`. Aucun cookie n'est lu ni posé : une page tierce n'a rien à voler.
"""
from __future__ import annotations

import json
import re
import threading
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

import puzzles_publies as pp

CORPS_MAX_OCTETS = 400_000
# (nombre, fenêtre en secondes) par adresse et par type d'appel
PLAFONDS = {"publier": (10, 3600), "ecrire": (40, 3600), "lire": (240, 60)}

_VERROU = threading.Lock()
_APPELS: Dict[Tuple[str, str], List[float]] = {}
_DERNIER_NETTOYAGE = [0.0]

Reponse = Tuple[int, Dict[str, Any], List[Tuple[str, str]]]


def debit_ok(genre: str, adresse: str, maintenant: Optional[float] = None) -> bool:
    """Compte l'appel et dit s'il passe (chaque appel compte, valide ou non)."""
    nombre, fenetre = PLAFONDS[genre]
    maintenant = time.time() if maintenant is None else maintenant
    with _VERROU:
        recents = [t for t in _APPELS.get((genre, adresse), []) if maintenant - t < fenetre]
        if len(recents) >= nombre:
            _APPELS[(genre, adresse)] = recents
            return False
        recents.append(maintenant)
        _APPELS[(genre, adresse)] = recents
        return True


def origine_permise(origine: str, domaine: str) -> bool:
    if not origine:
        return False
    hote = urllib.parse.urlparse(origine).hostname or ""
    if hote in ("127.0.0.1", "localhost"):
        return True
    return bool(domaine) and (hote == domaine or hote.endswith("." + domaine))


def _entetes(origine: str, domaine: str) -> List[Tuple[str, str]]:
    entetes = [("Cache-Control", "no-store"), ("Vary", "Origin")]
    if origine_permise(origine, domaine):
        entetes += [("Access-Control-Allow-Origin", origine),
                    ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
                    ("Access-Control-Allow-Headers", "Content-Type"),
                    ("Access-Control-Max-Age", "600")]
    return entetes


def est_route_puzzle(chemin: str) -> bool:
    return chemin == "/api/puzzle" or chemin.startswith("/api/puzzle/")


_CODE = re.compile(r"^/api/puzzle/([A-Za-z0-9\- ]{2,12})$")
_ACTION = re.compile(r"^/api/puzzle/([A-Za-z0-9\- ]{2,12})/(modifier|supprimer)$")


def traiter(serveur: pp.PuzzlesPublies, methode: str, chemin: str, parametres: Dict[str, List[str]],
            corps: bytes, adresse: str, origine: str = "", domaine: str = "") -> Reponse:
    entetes = _entetes(origine, domaine)

    def erreur(statut: int, raisons: Any) -> Reponse:
        return statut, {"erreur": raisons if isinstance(raisons, list) else [raisons]}, entetes

    if methode == "OPTIONS":
        return 204, {}, entetes
    if len(corps) > CORPS_MAX_OCTETS:
        return erreur(413, "requête trop grosse")

    try:
        if methode == "GET":
            correspondance = _CODE.match(chemin)
            if not correspondance:
                return erreur(404, "route inconnue")
            if not debit_ok("lire", adresse):
                return erreur(429, "trop de demandes, réessaie dans une minute")
            jouer = (parametres.get("jouer") or [""])[0] == "1"
            trouve = serveur.lire(correspondance.group(1), jouer=jouer)
            if trouve is None:
                return erreur(404, "puzzle introuvable ou expiré")
            return 200, trouve, entetes

        if methode == "POST":
            donnees = json.loads(corps.decode("utf-8")) if corps else None
            if not isinstance(donnees, dict):
                return erreur(400, "un objet JSON est attendu")
            if chemin == "/api/puzzle/publier":
                if not debit_ok("publier", adresse):
                    return erreur(429, "trop de publications, réessaie plus tard")
                resultat = serveur.publier(donnees.get("puzzle"), donnees.get("pseudo", ""))
                maintenant = time.time()
                if maintenant - _DERNIER_NETTOYAGE[0] > 3600:   # nettoyage paresseux, une fois l'heure
                    _DERNIER_NETTOYAGE[0] = maintenant
                    serveur.nettoyer()
                return 201, resultat, entetes
            correspondance = _ACTION.match(chemin)
            if correspondance:
                if not debit_ok("ecrire", adresse):
                    return erreur(429, "trop de demandes, réessaie plus tard")
                code, action = correspondance.groups()
                if action == "modifier":
                    return 200, serveur.modifier(code, donnees.get("cle"), donnees.get("puzzle")), entetes
                serveur.supprimer(code, donnees.get("cle"))
                return 200, {"supprime": True}, entetes
            return erreur(404, "route inconnue")
    except pp.ErreurPuzzle as e:
        return erreur(e.statut, e.raisons)
    except (ValueError, UnicodeDecodeError):
        return erreur(400, "JSON invalide")
    return erreur(405, "méthode non permise")
