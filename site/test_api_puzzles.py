"""L'API des puzzles publiés, de bout en bout : un VRAI serveur HTTP (le Handler de l'orchestrateur)
sur une base temporaire, interrogé par urllib.

    python3 site/test_api_puzzles.py
"""

import copy
import json
import os
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
dossier = tempfile.mkdtemp(prefix="api-puzzles-")
os.environ["BASE"] = os.path.join(dossier, "site.db")
os.environ["DOMAINE"] = "exemple.test"

import orchestrateur as o  # noqa: E402
import api_puzzles  # noqa: E402
from puzzle_exemple import PUZZLE  # noqa: E402

echecs = []


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
    else:
        echecs.append(nom)
        print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))


serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
threading.Thread(target=serveur.serve_forever, daemon=True).start()
RACINE = "http://127.0.0.1:%d" % serveur.server_address[1]


def appel(methode, chemin, corps=None, origine=None):
    donnees = json.dumps(corps).encode("utf-8") if corps is not None else None
    requete = urllib.request.Request(RACINE + chemin, data=donnees, method=methode,
                                     headers={"Content-Type": "application/json", **({"Origin": origine} if origine else {})})
    try:
        with urllib.request.urlopen(requete, timeout=10) as r:
            texte = r.read()
            return r.status, (json.loads(texte) if texte else {}), dict(r.headers)
    except urllib.error.HTTPError as e:
        texte = e.read()
        try:
            return e.code, json.loads(texte), dict(e.headers)
        except ValueError:
            return e.code, texte, dict(e.headers)


statut, pub, _ = appel("POST", "/api/puzzle/publier", {"puzzle": PUZZLE, "pseudo": "Arnaud"})
cas("publier : 201", statut, 201)
code, cle = pub["code"], pub["cle"]
statut, lu, entetes = appel("GET", "/api/puzzle/" + code)
cas("lire : 200 et le titre", (statut, lu["puzzle"]["title"]), (200, "Mon puzzle"))
cas("lire : jamais de cache", entetes.get("Cache-Control"), "no-store")
cas("lire : la clé ne fuit pas", cle in json.dumps(lu), False)
cas("lire en minuscules", appel("GET", "/api/puzzle/" + code.lower())[0], 200)
cas("jouer=1 compte une partie", appel("GET", "/api/puzzle/%s?jouer=1" % code)[1]["nb_jeux"], 1)
cas("code inconnu : 404", appel("GET", "/api/puzzle/PZ-ZZZZ")[0], 404)

mauvais = copy.deepcopy(PUZZLE); mauvais["puzzle_command"] = ["Puzzle.Win()"]
statut, corps, _ = appel("POST", "/api/puzzle/publier", {"puzzle": mauvais, "pseudo": "x"})
cas("commande interdite : 400 et raison", (statut, "inconnue" in json.dumps(corps)), (400, True))
cas("JSON qui n'est pas un objet : 400", appel("POST", "/api/puzzle/publier", ["a"])[0], 400)
requete = urllib.request.Request(RACINE + "/api/puzzle/publier", data=b"{pas du json", method="POST")
try:
    urllib.request.urlopen(requete, timeout=10)
    cas("JSON cassé : 400", 200, 400)
except urllib.error.HTTPError as e:
    cas("JSON cassé : 400", e.code, 400)

cas("modifier avec une mauvaise clé : 403", appel("POST", "/api/puzzle/%s/modifier" % code, {"cle": "x", "puzzle": PUZZLE})[0], 403)
nouveau = copy.deepcopy(PUZZLE); nouveau["title"] = "Autre titre"
cas("modifier avec la bonne clé : 200", appel("POST", "/api/puzzle/%s/modifier" % code, {"cle": cle, "puzzle": nouveau})[0], 200)
cas("le titre a changé", appel("GET", "/api/puzzle/" + code)[1]["puzzle"]["title"], "Autre titre")
cas("supprimer avec une mauvaise clé : 403", appel("POST", "/api/puzzle/%s/supprimer" % code, {"cle": "x"})[0], 403)
cas("supprimer avec la bonne clé : 200", appel("POST", "/api/puzzle/%s/supprimer" % code, {"cle": cle})[0], 200)
cas("puis introuvable", appel("GET", "/api/puzzle/" + code)[0], 404)

# --- CORS : seulement le domaine, ses sous-domaines et le jeu local
for origine, permis in (("https://p3.exemple.test", True), ("https://exemple.test", True), ("http://127.0.0.1:2345", True),
                        ("https://exemple.test.evil.com", False), ("https://evil.com", False)):
    _, _, e = appel("GET", "/api/puzzle/PZ-ZZZZ", origine=origine)
    cas("CORS %s" % origine, e.get("Access-Control-Allow-Origin") == origine, permis)
cas("jamais d'étoile", appel("GET", "/api/puzzle/PZ-ZZZZ", origine="https://p3.exemple.test")[2].get("Access-Control-Allow-Origin") != "*", True)
requete = urllib.request.Request(RACINE + "/api/puzzle/publier", method="OPTIONS", headers={"Origin": "https://p3.exemple.test"})
with urllib.request.urlopen(requete, timeout=10) as r:
    cas("OPTIONS : 204 avec les méthodes", (r.status, "POST" in r.headers.get("Access-Control-Allow-Methods", "")), (204, True))

# --- trop gros
cas("corps énorme : refusé", appel("POST", "/api/puzzle/publier", {"puzzle": {"description": "x" * 500_000}})[0] in (400, 413), True)

# --- freins
api_puzzles._APPELS.clear()
statuts = [appel("POST", "/api/puzzle/publier", {"puzzle": PUZZLE, "pseudo": "r"})[0] for _ in range(12)]
cas("frein de publication : 10 passent, le reste est refusé", (statuts.count(201), statuts.count(429)), (10, 2))

# --- le reste du site n'est pas touché
cas("une route du site répond encore", appel("GET", "/pret")[0] in (200, 204, 302, 303, 404), True)

serveur.shutdown()
sys.exit(1 if echecs else 0)
