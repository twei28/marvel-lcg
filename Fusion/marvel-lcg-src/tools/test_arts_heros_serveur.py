"""Les routes /get_arts_heros et /save_arts_heros (arts alternatifs du compte).

Ne demarre AUCUN moteur : on instancie `GameServerGet` sans le construire et on
l'appelle avec des requetes factices. Le fichier d'arts est un fichier
temporaire.

Usage: python3 tools/test_arts_heros_serveur.py
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
dossier = tempfile.mkdtemp(prefix="test-arts-heros-")
fichier = os.path.join(dossier, "arts-heros-serveur-1.json")
ARTS_HEROS_FILE.value = fichier
mot_de_passe = "secret-siege-0"
cookie_titulaire = {"seat_token_0": hashlib.md5(mot_de_passe.encode()).hexdigest()}
anciens = (list(SEAT_PASSWORDS.value), SITE_URL.value)
try:
    SITE_URL.value = "https://exemple.test"
    SEAT_PASSWORDS.value = [mot_de_passe, "", "", ""]

    # Premier passage : compte reconnu, mais aucun fichier.
    statut, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("titulaire sans fichier : compte vrai, existe faux",
             statut == 200 and corps == {"compte": True, "existe": False, "arts": {}}, corps)

    # Ecriture, puis relecture.
    statut, _ = appeler(serveur.save_arts_heros, Requete(
        cookie_titulaire, {"changements": {"38001": "rog", "38001b": "cb", "01001": "m3t"}}))
    verifier("ecriture acceptee", statut == 200, statut)
    statut, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("relecture : trois choix, fichier existant",
             corps["existe"] and corps["arts"] == {"38001": "rog", "38001b": "cb", "01001": "m3t"}, corps)

    # Effacer une cle (null) sans toucher aux autres ; deux appareils ne s'ecrasent pas.
    appeler(serveur.save_arts_heros, Requete(cookie_titulaire, {"changements": {"38001b": None}}))
    appeler(serveur.save_arts_heros, Requete(cookie_titulaire, {"changements": {"05001": "rog2"}}))
    _, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("null efface la cle, les autres changements restent",
             corps["arts"] == {"38001": "rog", "01001": "m3t", "05001": "rog2"}, corps["arts"])

    # Entrees mal formees : ignorees, jamais ecrites.
    appeler(serveur.save_arts_heros, Requete(cookie_titulaire, {"changements": {
        "../etc": "x", "38001": "ROG!", "12345": "a" * 40, "gp001": "cb", "06001": 7}}))
    _, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("cles et codes mal formes ignores, choix valides gardes",
             corps["arts"] == {"38001": "rog", "01001": "m3t", "05001": "rog2", "gp001": "cb"}, corps["arts"])

    # Corps invalide.
    statut, _ = appeler(serveur.save_arts_heros, Requete(cookie_titulaire, {"changements": [1]}))
    verifier("corps invalide refuse (400)", statut == 400, statut)

    # Un invite (aucun cookie de siege) : ni lecture ni ecriture.
    statut, corps = appeler(serveur.get_arts_heros, Requete({}))
    verifier("invite : le navigateur reste la reference",
             statut == 200 and corps == {"compte": False, "existe": False, "arts": {}}, corps)
    statut, _ = appeler(serveur.save_arts_heros, Requete({}, {"changements": {"38001": "cb"}}))
    verifier("invite : ecriture refusee (403)", statut == 403, statut)
    _, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("l'ecriture refusee n'a rien change", "cb" != corps["arts"].get("38001"), corps["arts"])

    # Moteur lance a la main (pas de site) : pas de compte, meme avec le siege.
    SITE_URL.value = ""
    statut, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("sans site : pas de compte", corps["compte"] is False, corps)
    statut, _ = appeler(serveur.save_arts_heros, Requete(cookie_titulaire, {"changements": {"38001": "cb"}}))
    verifier("sans site : ecriture refusee", statut == 403, statut)

    # Fichier abime : traite comme absent, le client le reecrit.
    SITE_URL.value = "https://exemple.test"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write("{pas du json")
    _, corps = appeler(serveur.get_arts_heros, Requete(cookie_titulaire))
    verifier("fichier illisible : existe faux", corps["existe"] is False and corps["arts"] == {}, corps)
finally:
    SEAT_PASSWORDS.value, SITE_URL.value = anciens
    for f in os.listdir(dossier):
        os.remove(os.path.join(dossier, f))
    os.rmdir(dossier)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
