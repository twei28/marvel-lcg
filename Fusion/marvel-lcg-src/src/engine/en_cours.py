"""Les parties EN COURS (non terminees) de cette table : le bandeau « Continuer la partie ».

Demande de l'utilisateur (18/11/2026) : comme dans Le Seigneur des Anneaux, un bandeau « Continuer la partie » sur l'accueil
et sur l'ecran de preparation, qui reprend la derniere partie la ou on l'avait laissee, et une liste des 4 ou 5 dernieres
parties non terminees.

Avant : UN seul fichier `save_auto.json`, ecrase a chaque debut de phase, donc une seule partie jamais proposee et aucune trace de
la precedente. Maintenant : un fichier PAR PARTIE, `<dossier de la table>/en-cours/<identifiant de partie>.json`, mis a jour a
chaque debut de phase (le plateau appelle `/en_cours_sauver`), et supprime a la fin de la partie (`Enregistrement` appelle
`supprimer`). On en garde 5, la plus ancienne saute quand une sixieme arrive.

Rien ici ne doit pouvoir arreter une partie : toute erreur est avalee (comme `Enregistrement`).

L'identifiant de partie est celui de l'enregistrement (`Enregistrement.partie`) : il change a chaque nouvelle partie ET a chaque
chargement d'une sauvegarde. Une partie reprise par le bandeau recevrait donc une SECONDE entree ; `noter_reprise` retient le
fichier repris, et la premiere sauvegarde de la partie reprise (meme graine) le remplace.
"""
import json
import os
import threading
from typing import Any, Dict, List, Optional

GARDEES = 5
_verrou = threading.Lock()
_reprise: Optional[Dict[str, Any]] = None  # {"fichier": chemin, "graine": int}


def dossier() -> str:
    from engine.file.manager import REPLAY_FOLDERS
    racine = (REPLAY_FOLDERS.value or ["../replays/"])[0]
    return os.path.join(racine, "en-cours")


def _nom(partie: str) -> str:
    sur = "".join(c for c in partie if c.isalnum() or c in "-_") or "partie"
    return os.path.join(dossier(), sur + ".json")


def _graine(chemin: str) -> Optional[int]:
    try:
        with open(chemin, encoding="utf-8") as f:
            return int(json.load(f).get("metadata", {}).get("seed"))
    except Exception:
        return None


def _purger() -> None:
    d = dossier()
    fichiers = sorted((os.path.join(d, n) for n in os.listdir(d) if n.endswith(".json")), key=os.path.getmtime, reverse=True)
    for vieux in fichiers[GARDEES:]:
        try:
            os.remove(vieux)
        except OSError:
            pass


def remplacer_reprise(chemin: str) -> None:
    """`chemin` vient d'etre ecrit : si c'est la partie reprise par le bandeau (meme graine) sous un nouvel identifiant, son ancienne
    entree est retiree, pour qu'elle n'apparaisse pas deux fois."""
    global _reprise
    with _verrou:
        if _reprise and _reprise.get("fichier") != chemin and _reprise.get("graine") == _graine(chemin):
            try:
                os.remove(_reprise["fichier"])
            except OSError:
                pass
            _reprise = None


def sauver(game: Any) -> Dict[str, Any]:
    """Ecrit la partie en cours dans son fichier. Rend {sauve, fichier | raison}."""
    try:
        from engine.enregistrement import Enregistrement
        monde = Enregistrement.dernier or {}
        partie = Enregistrement.partie
        if not partie:
            return {"sauve": False, "raison": "sans identifiant"}
        if monde.get("game_over"):
            return {"sauve": False, "raison": "terminee"}
        manche = int(monde.get("round_id") or 0)
        if manche <= 0:
            return {"sauve": False, "raison": "mise en place"}
        session = game.session
        scene = session.scene
        if scene is None or getattr(scene, "is_puzzle", False):
            return {"sauve": False, "raison": "aucune partie"}
        os.makedirs(dossier(), exist_ok=True)
        chemin = _nom(partie)
        # La manche et la phase voyagent dans le COMMENTAIRE du fichier (la fiche de reprise les relit) ; le commentaire de la
        # partie en cours, lui, est remis tel quel apres l'ecriture.
        ancien = scene.GetMetadataStr("comment")
        scene.SetMetadataStr("comment", "en-cours|%d|%s" % (manche, monde.get("phase", "")))
        try:
            ecrit = session.SaveScene(name=chemin, delete_old=False)
        finally:
            scene.SetMetadataStr("comment", ancien)
        if not ecrit:
            return {"sauve": False, "raison": "ecriture"}
        remplacer_reprise(chemin)
        with _verrou:
            _purger()
        return {"sauve": True, "fichier": chemin}
    except Exception as souci:
        return {"sauve": False, "raison": str(souci)}


def supprimer(partie: str, graine: Optional[int] = None) -> None:
    """La partie est finie : elle ne sera plus proposee. Silencieux.

    `graine` : celle de la partie qui vient de finir. Si elle est celle du fichier repris par le bandeau, ce fichier (que la
    partie reprise n'a pas encore remplace) part aussi ; sinon il s'agit d'une AUTRE partie et on n'y touche pas.
    """
    global _reprise
    try:
        chemin = _nom(partie)
        if os.path.exists(chemin):
            os.remove(chemin)
        with _verrou:
            if _reprise and graine is not None and _reprise.get("graine") == graine:
                try:
                    os.remove(_reprise["fichier"])
                except OSError:
                    pass
                _reprise = None
    except Exception:
        pass


def noter_reprise(chemin: str) -> bool:
    """Le joueur reprend ce fichier : la prochaine sauvegarde de la meme partie le remplacera."""
    global _reprise
    if chemin not in fichiers():
        return False
    with _verrou:
        _reprise = {"fichier": chemin, "graine": _graine(chemin)}
    return True


def fichiers() -> List[str]:
    """Les fichiers de la table, le plus recent d'abord (5 au plus)."""
    d = dossier()
    try:
        noms = [os.path.join(d, n) for n in os.listdir(d) if n.endswith(".json")]
    except OSError:
        return []
    return sorted(noms, key=os.path.getmtime, reverse=True)[:GARDEES]


def manche_et_phase(commentaire: str) -> Dict[str, Any]:
    morceaux = (commentaire or "").split("|")
    if len(morceaux) >= 2 and morceaux[0] == "en-cours":
        try:
            return {"round": int(morceaux[1]), "phase": morceaux[2] if len(morceaux) > 2 else ""}
        except ValueError:
            pass
    return {"round": 0, "phase": ""}
