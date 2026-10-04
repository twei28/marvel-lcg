"""Les routes /get_preferences et /save_preferences (preferences du compte).

Ne demarre AUCUN moteur, comme tools/test_arts_heros_serveur.py.

Usage: python3 tools/test_preferences_serveur.py
"""
import asyncio
import hashlib
import json
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

from engine.device.web.server.server_base import SEAT_PASSWORDS, SITE_URL
from engine.device.web.server.server_get import ARTS_HEROS_FILE, GameServerGet

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), str(detail)))


class Requete:
    def __init__(self, cookies=None, corps=None):
        self.cookies = cookies or {}
        self._corps = corps

    async def json(self):
        return self._corps


def appeler(route, requete):
    reponse = asyncio.run(route(requete))
    return reponse.status, json.loads(reponse.text)


serveur = GameServerGet.__new__(GameServerGet)
dossier = tempfile.mkdtemp(prefix="test-preferences-")
ancien_arts = ARTS_HEROS_FILE.value
ARTS_HEROS_FILE.value = os.path.join(dossier, "arts-heros-serveur-3.json")
attendu = os.path.join(dossier, "preferences-serveur-3.json")
mot_de_passe = "secret-siege-0"
cookie = {"seat_token_0": hashlib.md5(mot_de_passe.encode()).hexdigest()}
anciens = (list(SEAT_PASSWORDS.value), SITE_URL.value)
try:
    SITE_URL.value = "https://exemple.test"
    SEAT_PASSWORDS.value = [mot_de_passe, "", "", ""]

    verifier("le fichier suit celui des arts de la meme table",
             serveur._chemin_preferences() == attendu, serveur._chemin_preferences())

    statut, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("titulaire sans fichier : compte vrai, existe faux",
             statut == 200 and corps == {"compte": True, "existe": False, "preferences": {}}, corps)

    statut, _ = appeler(serveur.save_preferences, Requete(cookie, {"changements": {"affichage": "sobre"}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("ecriture puis relecture du mode sobre",
             statut == 200 and corps["existe"] and corps["preferences"] == {"affichage": "sobre"}, corps)
    verifier("ecrit a cote du fichier d'arts", os.path.isfile(attendu), os.listdir(dossier))

    appeler(serveur.save_preferences, Requete(cookie, {"changements": {
        "affichage": "fluo", "../x": "sobre", "langue": "en"}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("valeurs et cles inconnues ignorees, choix valide garde",
             corps["preferences"] == {"affichage": "sobre"}, corps["preferences"])

    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"affichage": None}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("null efface la cle", corps["preferences"] == {}, corps["preferences"])

    # La TEINTE du fond (04/10/2026) : trois entiers bornes « h,s,l ». Rien
    # d'autre n'est ecrit (bornes partagees avec board/teinte.ts et
    # public/js/prepare/teinte-choix.js : h 0-359, s 0-18, l 6-62).
    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"teinte": "210,12,18"}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("teinte valide ecrite et relue", corps["preferences"].get("teinte") == "210,12,18", corps["preferences"])
    for mauvaise in ("210,40,18", "400,10,18", "210,10,90", "rouge", "210,10", "210,10,18,1", 12, "-1,0,10", "1e2,1,10"):
        appeler(serveur.save_preferences, Requete(cookie, {"changements": {"teinte": mauvaise}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("teintes hors bornes ou mal formees ignorees, la valide gardee",
             corps["preferences"].get("teinte") == "210,12,18", corps["preferences"])
    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"teinte": None}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("null efface la teinte (couleur d'origine)", "teinte" not in corps["preferences"], corps["preferences"])

    # LA TABLE PERSONNALISABLE (04/10/2026) : une disposition par nombre de
    # joueurs (`table-1` a `table-4`), grille 12x8, neuf zones dans l'ordre fixe
    # de board/disposition.ts (« col,ligne,largeur,hauteur,taille% »), bornee et
    # SANS chevauchement. Rien d'autre n'est ecrit.
    TABLE = ("12x8|1,1,2,2,100;3,1,2,2,100;5,1,3,2,100;8,1,5,2,100;3,3,10,2,100;"
             "3,5,10,2,100;1,5,2,2,100;1,7,2,2,100;3,7,10,2,130")
    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"table-1": TABLE, "table-4": TABLE}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("table valide ecrite et relue (solo et 4 joueurs)",
             corps["preferences"].get("table-1") == TABLE and corps["preferences"].get("table-4") == TABLE,
             corps["preferences"])
    mauvaises = [
        TABLE.replace("12x8", "10x8"),                       # autre grille
        TABLE.rsplit(";", 1)[0],                             # huit zones
        TABLE.replace("3,7,10,2,130", "3,6,10,2,130"),       # la main chevauche le heros
        TABLE.replace("3,7,10,2,130", "4,7,10,2,130"),       # sort de la grille
        TABLE.replace("3,7,10,2,130", "3,7,10,2,170"),       # taille hors bornes
        TABLE.replace("3,7,10,2,130", "3,7,0,2,130"),        # zone vide
        TABLE.replace("3,7,10,2,130", "3,7,10,2,1e2"),       # pas un entier
        TABLE + ";" + "1,1,1,1,100",                         # zone de trop
        42,
    ]
    for mauvaise in mauvaises:
        appeler(serveur.save_preferences, Requete(cookie, {"changements": {"table-2": mauvaise}}))
    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"table-5": TABLE, "table-0": TABLE}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("tables mal formees, chevauchantes ou hors bornes ignorees ; table-0 et table-5 refusees",
             "table-2" not in corps["preferences"] and "table-5" not in corps["preferences"]
             and "table-0" not in corps["preferences"], corps["preferences"])
    appeler(serveur.save_preferences, Requete(cookie, {"changements": {"table-1": None, "table-4": None}}))
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("null efface la table (disposition d'origine)",
             not any(c.startswith("table-") for c in corps["preferences"]), corps["preferences"])

    statut, _ = appeler(serveur.save_preferences, Requete(cookie, {"changements": ["sobre"]}))
    verifier("corps invalide refuse (400)", statut == 400, statut)

    statut, corps = appeler(serveur.get_preferences, Requete({}))
    verifier("invite : le navigateur reste la reference",
             corps == {"compte": False, "existe": False, "preferences": {}}, corps)
    statut, _ = appeler(serveur.save_preferences, Requete({}, {"changements": {"affichage": "sobre"}}))
    verifier("invite : ecriture refusee (403)", statut == 403, statut)

    SITE_URL.value = ""
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("sans site : pas de compte", corps["compte"] is False, corps)

    SITE_URL.value = "https://exemple.test"
    with open(attendu, "w", encoding="utf-8") as f:
        f.write("{abime")
    _, corps = appeler(serveur.get_preferences, Requete(cookie))
    verifier("fichier illisible : existe faux", corps["existe"] is False, corps)
finally:
    SEAT_PASSWORDS.value, SITE_URL.value = anciens
    ARTS_HEROS_FILE.value = ancien_arts
    for f in os.listdir(dossier):
        os.remove(os.path.join(dossier, f))
    os.rmdir(dossier)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
