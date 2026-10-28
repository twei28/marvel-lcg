"""Stockage des projets du « créateur de cartes » (côté serveur du site).

Un projet = un document JSON (il porte des images en data URL, d'où des
dizaines de Mo). Gardé en FICHIERS, pas dans narwhal.db : une base SQLite n'a
rien à gagner à porter des blobs de 25 Mo, et un fichier se sauvegarde / se
restaure à la main.

Arborescence (RACINE = `dossier_racine`) :

    RACINE/<compte>/<id>/courant.json      la version en cours
    RACINE/<compte>/<id>/meta.json         nom, dossier, date : pour la liste
    RACINE/<compte>/<id>/versions/<n>.json les anciennes versions (30 dernières)
    RACINE/<compte>/.corbeille/<id>-<époque>/  un projet SUPPRIMÉ (les 20 derniers)

⚠ AUCUN CHEMIN N'EST CONSTRUIT DEPUIS L'ENTRÉE BRUTE. `<compte>` et `<id>` ne
passent qu'après validation par une liste blanche stricte (lettres, chiffres,
« - » et « _ »), `<n>` n'est qu'un entier. `_chemin_sur` revérifie en plus que
le résultat reste SOUS la racine : deux barrières valent mieux qu'une.

⚠ ÉCRITURE ATOMIQUE : fichier temporaire dans le même dossier, `fsync`, puis
`os.replace`. Un plantage au milieu laisse l'ancienne version intacte, jamais
un JSON tronqué.

Ce module ne connaît ni HTTP ni les comptes : il lève `ErreurCreateur`
(avec un code HTTP) et c'est `orchestrateur.Handler` qui répond.
"""
import json
import os
import re
import threading
import time

VERSIONS_GARDEES = 30
CORBEILLE_GARDEE = 20
RE_COMPTE = re.compile(r"^[a-z0-9_-]{3,24}$")
RE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


class ErreurCreateur(Exception):
    """Une erreur à rendre telle quelle au client (`code` HTTP + message)."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


# Un verrou par compte : deux PUT simultanés sur le même projet ne doivent pas
# se marcher dessus (numérotation des versions, quota).
_VERROUS: dict[str, threading.Lock] = {}
_VERROU_VERROUS = threading.Lock()


def _verrou(compte: str) -> threading.Lock:
    with _VERROU_VERROUS:
        return _VERROUS.setdefault(compte, threading.Lock())


def compte_valide(compte: str) -> str:
    compte = (compte or "").strip().lower()
    if not RE_COMPTE.match(compte):
        raise ErreurCreateur(400, "Nom de compte invalide.")
    return compte


def id_valide(identifiant: str) -> str:
    if not isinstance(identifiant, str) or not RE_ID.match(identifiant):
        raise ErreurCreateur(400, "Identifiant de projet invalide : 1 à 64 caractères,"
                                  " lettres, chiffres, « - » et « _ » seulement.")
    return identifiant


def _chemin_sur(racine: str, *morceaux: str) -> str:
    """Joint des morceaux DÉJÀ validés et vérifie qu'on reste sous la racine."""
    racine_reelle = os.path.realpath(racine)
    chemin = os.path.realpath(os.path.join(racine_reelle, *morceaux))
    if chemin != racine_reelle and not chemin.startswith(racine_reelle + os.sep):
        raise ErreurCreateur(400, "Chemin refusé.")
    return chemin


def _ecrire_atomique(chemin: str, octets: bytes) -> None:
    dossier = os.path.dirname(chemin)
    os.makedirs(dossier, exist_ok=True)
    temporaire = "%s.%d.%d.tmp" % (chemin, os.getpid(), threading.get_ident())
    try:
        with open(temporaire, "wb") as f:
            f.write(octets)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporaire, chemin)
    finally:
        if os.path.exists(temporaire):
            os.remove(temporaire)


def _iso(epoque: float) -> str:
    # UTC avec « Z » : la page compare ces dates à celles de son navigateur
    # (fusion « le plus récent gagne »), sans dépendre du fuseau du serveur.
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoque))


def usage_octets(racine: str, compte: str) -> int:
    """Octets occupés par un compte (courant + versions + méta ; pas la corbeille)."""
    total = 0
    base = _chemin_sur(racine, compte_valide(compte))
    for dossier, sous, fichiers in os.walk(base):
        # la corbeille ne compte pas : supprimer doit LIBERER de la place
        if os.path.dirname(dossier) == base:
            sous[:] = [d for d in sous if d != ".corbeille"]
        for nom in fichiers:
            try:
                total += os.path.getsize(os.path.join(dossier, nom))
            except OSError:
                pass
    return total


def _meta_depuis(identifiant: str, document: dict, taille: int, quand: float) -> dict:
    # Le créateur de cartes peut nommer ses champs en français ou en anglais.
    nom = document.get("nom", document.get("name", identifiant))
    dossier = document.get("dossier", document.get("folder", ""))
    return {
        "id": identifiant,
        "nom": str(nom if nom is not None else identifiant)[:200],
        "dossier": str(dossier if dossier is not None else "")[:200],
        "modifie": _iso(quand),
        "taille": taille,
    }


def lister(racine: str, compte: str) -> list[dict]:
    base = _chemin_sur(racine, compte_valide(compte))
    sortie = []
    if not os.path.isdir(base):
        return sortie
    for identifiant in sorted(os.listdir(base)):
        if not RE_ID.match(identifiant):
            continue        # on ne lit que ce que nous aurions pu écrire
        fichier_meta = _chemin_sur(racine, compte, identifiant, "meta.json")
        try:
            with open(fichier_meta, "r", encoding="utf-8") as f:
                meta = json.load(f)
            sortie.append({k: meta.get(k, "") for k in
                           ("id", "nom", "dossier", "modifie", "taille")})
        except (OSError, ValueError):
            continue
    sortie.sort(key=lambda m: m.get("modifie", ""), reverse=True)
    return sortie


def lire(racine: str, compte: str, identifiant: str) -> bytes:
    chemin = _chemin_sur(racine, compte_valide(compte), id_valide(identifiant), "courant.json")
    try:
        with open(chemin, "rb") as f:
            return f.read()
    except OSError:
        raise ErreurCreateur(404, "Projet introuvable.")


def _numeros_versions(dossier_versions: str) -> list[int]:
    if not os.path.isdir(dossier_versions):
        return []
    sortie = []
    for nom in os.listdir(dossier_versions):
        m = re.match(r"^(\d{1,9})\.json$", nom)
        if m:
            sortie.append(int(m.group(1)))
    return sorted(sortie)


def ecrire(racine: str, compte: str, identifiant: str, octets: bytes,
           quota: int, max_octets: int) -> dict:
    """Crée ou remplace un projet. Rend ses métadonnées."""
    compte = compte_valide(compte)
    identifiant = id_valide(identifiant)
    if len(octets) > max_octets:
        raise ErreurCreateur(413, "Projet trop volumineux : %d Mo au maximum."
                             % (max_octets // (1024 * 1024)))
    try:
        document = json.loads(octets.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise ErreurCreateur(400, "Le corps n'est pas du JSON valide.")
    if not isinstance(document, dict):
        raise ErreurCreateur(400, "Un projet est un objet JSON.")
    dossier_projet = _chemin_sur(racine, compte, identifiant)
    with _verrou(compte):
        utilise = usage_octets(racine, compte)
        if utilise + len(octets) > quota:
            raise ErreurCreateur(
                507, "Espace épuisé : %d Mo utilisés sur %d Mo. Supprime des projets"
                     " ou d'anciennes images pour continuer."
                     % (utilise // (1024 * 1024), quota // (1024 * 1024)))
        courant = os.path.join(dossier_projet, "courant.json")
        versions = os.path.join(dossier_projet, "versions")
        if os.path.exists(courant):
            os.makedirs(versions, exist_ok=True)
            existants = _numeros_versions(versions)
            suivant = (existants[-1] + 1) if existants else 1
            # `os.replace` : l'ancienne version GARDE sa date d'écriture, que
            # `versions()` rend comme « modifiée le ».
            os.replace(courant, os.path.join(versions, "%d.json" % suivant))
            existants.append(suivant)
            for ancien in existants[:-VERSIONS_GARDEES]:
                try:
                    os.remove(os.path.join(versions, "%d.json" % ancien))
                except OSError:
                    pass
        _ecrire_atomique(courant, octets)
        meta = _meta_depuis(identifiant, document, len(octets), time.time())
        _ecrire_atomique(os.path.join(dossier_projet, "meta.json"),
                         json.dumps(meta, ensure_ascii=False).encode("utf-8"))
    return meta


def supprimer(racine: str, compte: str, identifiant: str) -> None:
    """Met le projet à la CORBEILLE (avec ses versions) au lieu de l'effacer :
    renommer un dossier ou en vider un par erreur ne détruit plus l'historique.
    `.corbeille` ne passe pas `RE_ID` (le point est refusé) : `lister` l'ignore
    et aucune route ne peut le désigner. On en garde les 20 derniers."""
    compte = compte_valide(compte)
    dossier_projet = _chemin_sur(racine, compte, id_valide(identifiant))
    with _verrou(compte):
        if not os.path.isdir(dossier_projet):
            raise ErreurCreateur(404, "Projet introuvable.")
        corbeille = _chemin_sur(racine, compte, ".corbeille")
        os.makedirs(corbeille, exist_ok=True)
        destination = os.path.join(corbeille, "%s-%d" % (identifiant, int(time.time() * 1000)))
        os.replace(dossier_projet, destination)
        anciens = sorted(os.listdir(corbeille),
                         key=lambda n: os.path.getmtime(os.path.join(corbeille, n)))
        for nom in anciens[:-CORBEILLE_GARDEE]:
            vieux = os.path.join(corbeille, nom)
            for dossier, sous, fichiers in os.walk(vieux, topdown=False):
                for f in fichiers:
                    os.remove(os.path.join(dossier, f))
                for d in sous:
                    os.rmdir(os.path.join(dossier, d))
            os.rmdir(vieux)


def versions(racine: str, compte: str, identifiant: str) -> list[dict]:
    dossier = _chemin_sur(racine, compte_valide(compte), id_valide(identifiant))
    if not os.path.isdir(dossier):
        raise ErreurCreateur(404, "Projet introuvable.")
    sortie = []
    dossier_versions = os.path.join(dossier, "versions")
    for n in reversed(_numeros_versions(dossier_versions)):
        chemin = os.path.join(dossier_versions, "%d.json" % n)
        try:
            etat = os.stat(chemin)
        except OSError:
            continue
        sortie.append({"n": n, "modifie": _iso(etat.st_mtime), "taille": etat.st_size})
    return sortie


def lire_version(racine: str, compte: str, identifiant: str, numero: str) -> bytes:
    if not isinstance(numero, str) or not re.match(r"^\d{1,9}$", numero):
        raise ErreurCreateur(400, "Numéro de version invalide.")
    chemin = _chemin_sur(racine, compte_valide(compte), id_valide(identifiant),
                         "versions", "%d.json" % int(numero))
    try:
        with open(chemin, "rb") as f:
            return f.read()
    except OSError:
        raise ErreurCreateur(404, "Version introuvable.")
