"""Enregistrement d'une partie pour « Revoir sa partie ».

Une ligne JSON par evenement, dans `<replays>/enregistrements/<partie>.jsonl` :
  {"k": "cle", "r": rendu, "t": ms, "m": monde}     monde complet (tous les 50 rendus)
  {"k": "d",   "r": rendu, "t": ms, "d": difference} difference avec le rendu precedent
  {"k": "q",   "r": rendu, "t": ms, "p": siege, "q": demande}
  {"k": "c",   "t": ms, "p": siege, "x": .., "y": .., "clic": id}   curseur
  {"k": "e",   "t": ms, "p": siege, "cle": etape}                   etape du cartouche
  {"k": "v",   "t": ms, "p": siege, "g": genre, "v": valeur}       ce que le joueur voit
                                             (selection, loupe, pile, reglages, ecran,
                                             messages, menus, manuel, glisser,
                                             defilements : `server_get.set_vu`)
  {"k": "res", "r": rendu, "m": {id: "YB"}}  ressources imprimees des cartes en main
                                             (le monde ne les porte pas : le bandeau
                                             de la relecture dit avec quoi on a paye)
Le monde est celui du moteur, NON filtre : la relecture montre toutes les mains.

Le format de difference (meme algorithme que `relecture/difference.ts`) :
  egal -> absent ; dict -> {"o": {cle: sous-difference}, "x": [cles retirees]} ;
  liste de meme longueur -> {"i": {"indice": sous-difference}} ; sinon {"v": valeur}.

Rien ici ne doit pouvoir arreter une partie : toute erreur d'ecriture est
avalee, la partie continue sans enregistrement.
"""
import gzip
import json
import os
import threading
import time
from typing import Any, Dict, List, Optional

VERSION_FORMAT = 1
CLE_TOUS_LES = 50
PARTIES_GARDEES = 3
# Les PARTIES TERMINEES de chaque joueur, pour l'administrateur (08/10/2026) :
# a la fin d'une partie (victoire ou defaite), le fichier .marvelreplay est
# range chez l'HOTE de la table, ses 3 dernieres gardees. Le site donne le
# pseudo et le dossier dans la configuration de la table ; sans eux (moteur
# lance a la main), rien n'est range.
PARTIES_PAR_JOUEUR = 3


def difference(a: Any, b: Any) -> Optional[Dict[str, Any]]:
    if a == b:
        return None
    if isinstance(a, dict) and isinstance(b, dict):
        changes: Dict[str, Any] = {}
        for cle, valeur in b.items():
            if cle not in a:
                changes[cle] = {"v": valeur}
                continue
            sous = difference(a[cle], valeur)
            if sous is not None:
                changes[cle] = sous
        retirees = [cle for cle in a if cle not in b]
        resultat: Dict[str, Any] = {}
        if changes:
            resultat["o"] = changes
        if retirees:
            resultat["x"] = retirees
        return resultat
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        indices = {}
        for i, (x, y) in enumerate(zip(a, b)):
            sous = difference(x, y)
            if sous is not None:
                indices[str(i)] = sous
        return {"i": indices}
    return {"v": b}


def appliquer(a: Any, d: Optional[Dict[str, Any]]) -> Any:
    if d is None:
        return a
    if "v" in d:
        return d["v"]
    if "i" in d:
        copie = list(a)
        for indice, sous in d["i"].items():
            copie[int(indice)] = appliquer(copie[int(indice)], sous)
        return copie
    copie = dict(a)
    for cle in d.get("x", []):
        copie.pop(cle, None)
    for cle, sous in d.get("o", {}).items():
        copie[cle] = appliquer(copie.get(cle), sous)
    return copie


def _ms() -> int:
    return int(time.time() * 1000)


class Enregistrement:
    verrou = threading.Lock()
    chemin: Optional[str] = None
    partie: str = ""
    dernier: Optional[Dict[str, Any]] = None
    depuis_cle = 0
    entete: Dict[str, Any] = {}
    entete_complet = False
    ressources_vues: set = set()

    @staticmethod
    def dossier() -> str:
        from engine.file.manager import REPLAY_FOLDERS
        racine = (REPLAY_FOLDERS.value or ["../replays/"])[0]
        return os.path.join(racine, "enregistrements")

    @classmethod
    def _ecrire(cls, ligne: Dict[str, Any]) -> None:
        if cls.chemin is None:
            return
        with open(cls.chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False, separators=(",", ":")) + "\n")

    @classmethod
    def _purger(cls, dossier: str) -> None:
        fichiers = sorted(
            (os.path.join(dossier, nom) for nom in os.listdir(dossier) if nom.endswith(".jsonl")),
            key=os.path.getmtime,
        )
        for vieux in fichiers[:-PARTIES_GARDEES]:
            try:
                os.remove(vieux)
            except OSError:
                pass

    @classmethod
    def _ouvrir(cls, partie: str, entete: Dict[str, Any]) -> None:
        dossier = cls.dossier()
        os.makedirs(dossier, exist_ok=True)
        nom = "".join(c for c in partie if c.isalnum() or c in "-_") or "partie"
        cls.chemin = os.path.join(dossier, nom + ".jsonl")
        cls.partie = partie
        cls.dernier = None
        cls.depuis_cle = 0
        cls.entete = entete
        cls.entete_complet = False
        cls.ressources_vues = set()
        with open(cls.chemin, "w", encoding="utf-8") as f:
            f.write(json.dumps({"k": "entete", **entete}, ensure_ascii=False) + "\n")
        cls._purger(dossier)

    @staticmethod
    def DossierDeLHote() -> Optional[str]:
        """Le dossier des parties terminees de l'hote de cette table, s'il est configure."""
        try:
            from engine.config import ConfigVariables
            pseudo = ConfigVariables.Str("pseudo_hote", "").value or ""
            racine = ConfigVariables.Str("parties_joueurs_dossier", "").value or ""
        except Exception:
            return None
        pseudo = "".join(c for c in pseudo.lower() if c.isalnum() or c in "-_.")
        return os.path.join(racine, pseudo) if pseudo and racine else None

    @staticmethod
    def PartiesDeLHote() -> List[str]:
        """Ses parties terminees, la plus recente en tete."""
        dossier = Enregistrement.DossierDeLHote()
        try:
            noms = os.listdir(dossier) if dossier else []
        except OSError:
            return []
        return sorted((n for n in noms if n.endswith(".marvelreplay")), reverse=True)

    @classmethod
    def _archiver_si_finie(cls, avant: Optional[Dict[str, Any]], monde: Dict[str, Any]) -> None:
        if not monde.get("game_over") or (avant or {}).get("game_over"):
            return
        dossier = cls.DossierDeLHote()
        if dossier:
            threading.Thread(target=cls._ranger_chez, args=(dossier,), daemon=True).start()

    @classmethod
    def _ranger_chez(cls, dossier: str) -> None:
        try:
            contenu = cls.Fichier()
            if contenu is None:
                return
            os.makedirs(dossier, exist_ok=True)
            scenario = "".join(c for c in str(cls.entete.get("scenario", "")) if c.isalnum())[:30] or "partie"
            nom = "partie-%s-%s.marvelreplay" % (time.strftime("%Y%m%d-%H%M%S"), scenario)
            with open(os.path.join(dossier, nom), "wb") as f:
                f.write(contenu)
            parties = sorted(n for n in os.listdir(dossier) if n.endswith(".marvelreplay"))
            for vieille in parties[:-PARTIES_PAR_JOUEUR]:
                os.remove(os.path.join(dossier, vieille))
        except Exception:
            pass

    @classmethod
    def Rendu(cls, partie: str, monde: Dict[str, Any], entete_si_nouvelle,
              ressources: Optional[Dict[int, str]] = None) -> None:
        try:
            with cls.verrou:
                if partie != cls.partie or cls.chemin is None:
                    cls._ouvrir(partie, entete_si_nouvelle())
                rendu = monde.get("render_id", 0)
                # Au premier rendu, les heros ne sont pas encore poses (l'identite
                # lue est la carte de regles) : l'en-tete se complete au round 1.
                if not cls.entete_complet and monde.get("round_id", 0) >= 1:
                    cls.entete = {**cls.entete, **entete_si_nouvelle()}
                    cls.entete_complet = True
                if cls.dernier is None or cls.depuis_cle >= CLE_TOUS_LES:
                    cls._ecrire({"k": "cle", "r": rendu, "t": _ms(), "m": monde})
                    cls.depuis_cle = 0
                else:
                    cls._ecrire({"k": "d", "r": rendu, "t": _ms(), "d": difference(cls.dernier, monde) or {}})
                    cls.depuis_cle += 1
                avant = cls.dernier
                cls.dernier = monde
                neuves = {i: r for i, r in (ressources or {}).items() if i not in cls.ressources_vues}
                if neuves:
                    cls._ecrire({"k": "res", "r": rendu, "m": {str(i): r for i, r in neuves.items()}})
                    cls.ressources_vues.update(neuves)
            cls._archiver_si_finie(avant, monde)
        except Exception:
            cls.chemin = None

    @classmethod
    def Evenement(cls, genre: str, donnees: Dict[str, Any]) -> None:
        try:
            with cls.verrou:
                if cls.chemin is None or cls.dernier is None:
                    return
                cls._ecrire({"k": genre, "r": cls.dernier.get("render_id", 0), "t": _ms(), **donnees})
        except Exception:
            pass

    @classmethod
    def Fichier(cls) -> Optional[bytes]:
        """Le fichier .marvelreplay de la partie enregistree (gzip), resultat compris."""
        with cls.verrou:
            if cls.chemin is None or not os.path.exists(cls.chemin):
                return None
            with open(cls.chemin, "r", encoding="utf-8") as f:
                lignes = f.read().splitlines()
            dernier = cls.dernier or {}
            complement = dict(cls.entete)
        entete = json.loads(lignes[0]) if lignes else {"k": "entete"}
        entete.update({k: v for k, v in complement.items() if k != "date"})
        entete["format"] = VERSION_FORMAT
        entete["rounds"] = dernier.get("round_id", 0)
        if dernier.get("game_over"):
            entete["resultat"] = "victoire" if dernier.get("players_won") else "defaite"
        else:
            entete["resultat"] = "inachevee"
        corps = "\n".join([json.dumps(entete, ensure_ascii=False)] + lignes[1:]) + "\n"
        return gzip.compress(corps.encode("utf-8"))


def entete_de(game: Any) -> Dict[str, Any]:
    """Ce qui decrit la partie avant de la lancer (scenario, heros, date, version)."""
    entete: Dict[str, Any] = {"date": time.strftime("%Y-%m-%d %H:%M"), "joueurs": []}
    try:
        campagne = getattr(getattr(game, "scene", None), "campaign", None)
        entete["scenario"] = str(getattr(campagne, "name", "") or "")
        entete["expert"] = bool(getattr(campagne, "expert", False))
        entete["version"] = str(getattr(getattr(game, "session", None), "version", "") or "")
        for joueur in game.world.const_players:
            identite = joueur.GetIdentity()
            try:
                heros = joueur.GetHero()
            except Exception:
                heros = None
            nom = getattr(getattr(heros or identite, "paper", None), "name", "")
            # Le nom du HEROS (« Spider-Man »), pas celui de l'identite du moment
            # (« Peter Parker » en alter ego) : `hero_name` est le nom du deck.
            deck = str(getattr(joueur, "hero_name", "") or "")
            entete["joueurs"].append({
                "heros": deck or str(nom or "").lstrip("* "),
                "deck": str(getattr(joueur, "hero_name", "") or ""),
            })
    except Exception:
        pass
    return entete


def ressources_des_mains(world: Any) -> Dict[int, str]:
    """Les ressources imprimees des cartes en main, par identifiant d'objet."""
    resultat: Dict[int, str] = {}
    try:
        for joueur in world.const_players:
            for face in joueur.hand_cards.GetAll():
                try:
                    texte = str(face.printed_resource.text or "")
                except Exception:
                    continue
                resultat[face.card.object_id] = texte
    except Exception:
        pass
    return resultat
