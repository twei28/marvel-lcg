"""« Decks des joueurs » : consultation et import par l'administrateur.

    python3 site/test_decks_admin.py

Donnees SYNTHETIQUES, base jetable, serveur HTTP local (voir
serveur_essai_decks_admin.py). Verifie, par HTTP :
  - un non-admin et un visiteur sans session sont refuses (403) ;
  - l'admin lit les decks d'un autre compte, sans e-mail ni mot de passe ;
  - l'import copie sous `de-<compte>-<deck>`, sans toucher l'original ;
  - un second import ne ecrase pas la premiere copie ;
  - la traversee de repertoire, les liens et les noms exotiques sont refuses ;
  - le plafond d'imports, la taille et l'en-tete obligatoire ;
  - le journal est ecrit (consultation, import, refus).
"""
import hashlib
import http.client
import json
import os
import sys
import threading
import urllib.parse
from http.server import ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import serveur_essai_decks_admin as essai  # noqa: E402

o, dossier, ctx = essai.monter()
echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + ("" if condition else " | " + str(detail)))
    if not condition:
        echecs.append(nom)


serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
port = serveur.server_address[1]
threading.Thread(target=serveur.serve_forever, daemon=True).start()


def appeler(methode, chemin, session=None, corps=None, entetes=None):
    h = dict(entetes or {})
    if session:
        h["Cookie"] = "nc_session=" + session
    cx = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    cx.request(methode, chemin, body=corps, headers=h)
    r = cx.getresponse()
    brut = r.read()
    cx.close()
    return r.status, brut


def importer(session, compte, deck, avec_entete=True):
    corps = urllib.parse.urlencode({"compte": compte, "deck": deck})
    h = {"Content-Type": "application/x-www-form-urlencoded"}
    if avec_entete:
        h["X-Importer-Deck"] = "1"
    return appeler("POST", "/api/admin/decks-joueurs/importer", session, corps, h)


def empreintes(chemin):
    return {n: hashlib.sha256(open(os.path.join(chemin, n), "rb").read()).hexdigest()
            for n in sorted(os.listdir(chemin))}


s_admin = o.ouvrir_session("arnaud")
s_alice = o.ouvrir_session("alice")
dossier_alice = os.path.join(ctx["jeu"], ".game", "deck", "serveur-%d" % ctx["places"]["alice"])
dossier_admin = os.path.join(ctx["jeu"], ".game", "deck", "serveur-%d" % ctx["places"]["arnaud"])
avant_alice = empreintes(dossier_alice)

print("Lecture")
verifier("visiteur sans session : 403", appeler("GET", "/api/admin/decks-joueurs")[0] == 403)
verifier("joueur ordinaire : 403", appeler("GET", "/api/admin/decks-joueurs", s_alice)[0] == 403)
code, brut = appeler("GET", "/api/admin/decks-joueurs", s_admin)
verifier("admin : 200", code == 200, code)
donnees = json.loads(brut)
par_compte = {c["compte"]: c["decks"] for c in donnees["comptes"]}
verifier("l'admin lit les decks d'un autre compte", {d["id"] for d in par_compte.get("alice", [])} == {"mcdb-Equilibre", "Agressif"}, par_compte)
verifier("ses propres decks ne sont pas listes", "arnaud" not in par_compte)
equilibre = next(d for d in par_compte["alice"] if d["id"] == "mcdb-Equilibre")
verifier("nom, cartes, date presents", equilibre["cartes"] == 40 and equilibre["nom"] and equilibre["date"], equilibre)
verifier("ni e-mail ni mot de passe dans la reponse",
         b"essai.invalid" not in brut and b"empreinte" not in brut and b"essai-mdp" not in brut)

print("Import")
verifier("joueur ordinaire : 403", importer(s_alice, "bob", "Protection")[0] == 403)
verifier("visiteur : 403", importer(None, "bob", "Protection")[0] == 403)
verifier("sans l'en-tete obligatoire : 400", importer(s_admin, "alice", "Agressif", avec_entete=False)[0] == 400)
verifier("aucune copie apres ces refus", not any(n.startswith("de-") for n in os.listdir(dossier_admin)))
code, brut = importer(s_admin, "alice", "Agressif")
verifier("import : 200", code == 200, (code, brut))
copie = os.path.join(dossier_admin, "de-alice-Agressif.json")
verifier("copie dans le dossier de l'admin", os.path.isfile(copie))
verifier("original intact (octet pour octet)", empreintes(dossier_alice) == avant_alice)
cartes_copie = json.load(open(copie, encoding="utf-8"))
verifier("le contenu est celui du deck", len(cartes_copie["player_deck"]) == 36 and "alice" in cartes_copie["name"])
premiere = open(copie, "rb").read()
code, brut = importer(s_admin, "alice", "Agressif")
verifier("second import : 200, nouveau nom", code == 200 and json.loads(brut)["fichier"] == "de-alice-Agressif-2", brut)
verifier("la premiere copie n'est pas ecrasee", open(copie, "rb").read() == premiere)
verifier("le deck existant de l'admin est intact", os.path.isfile(os.path.join(dossier_admin, "Deja-la.json")))

print("Chemins refuses")
avant_admin = empreintes(dossier_admin)
for deck in ("../serveur-%d/Deja-la" % ctx["places"]["arnaud"], "..", "../../data/cards", "a/b",
             "%2e%2e%2f", "Agressif.json", "", "x" * 200, "Agressif\x00"):
    code, _ = importer(s_admin, "alice", deck)
    verifier("deck %r refuse" % deck[:30], code == 404, code)
for compte in ("../alice", "arnaud", "inconnu", "alice/..", "ALICE", ""):
    code, _ = importer(s_admin, compte, "Agressif")
    verifier("compte %r refuse" % compte, code == 404, code)
# Un lien symbolique dans le dossier d'un joueur, vers un fichier hors de deck/.
secret = os.path.join(dossier, "secret.json")
open(secret, "w").write(json.dumps({"hero": ["x"]}))
os.symlink(secret, os.path.join(dossier_alice, "Lien.json"))
code, _ = importer(s_admin, "alice", "Lien")
verifier("fichier-lien refuse", code == 404, code)
liste = json.loads(appeler("GET", "/api/admin/decks-joueurs", s_admin)[1])
verifier("le lien n'est pas liste", all(d["id"] != "Lien" for c in liste["comptes"] for d in c["decks"]))
os.remove(os.path.join(dossier_alice, "Lien.json"))
verifier("rien n'a ete ecrit par ces refus", empreintes(dossier_admin) == avant_admin)

print("Taille et plafond")
gros = os.path.join(dossier_alice, "Gros.json")
with open(gros, "w") as f:
    f.write(json.dumps({"hero": ["x"], "pad": "a" * (o.DECK_ADMIN_MAX_OCTETS + 10)}))
verifier("deck trop gros : 422", importer(s_admin, "alice", "Gros")[0] == 422)
os.remove(gros)
o.DECK_ADMIN_IMPORTS_PAR_HEURE = 3
o._IMPORTS_ADMIN.clear()
codes = [importer(s_admin, "bob", "Protection")[0] for _ in range(5)]
verifier("plafond d'imports par heure : 429", codes == [200, 200, 200, 429, 429], codes)

print("Journal")
lignes = [json.loads(l) for l in open(o.JOURNAL_DECKS_ADMIN, encoding="utf-8")]
verifier("consultations journalisees", any(l["action"] == "consultation" and l["qui"] == "arnaud" for l in lignes))
imports_ok = [l for l in lignes if l["action"] == "import" and l["resultat"] == "ok"]
verifier("import journalise : qui, compte, deck, quand",
         any(l["compte"] == "alice" and l["deck"] == "Agressif" and l["qui"] == "arnaud" and l["quand"] for l in imports_ok), lignes[:3])
verifier("refus journalises", any(l["action"] == "import" and l["resultat"].startswith("refuse") for l in lignes))
verifier("le journal ne contient ni e-mail ni mot de passe", "essai.invalid" not in open(o.JOURNAL_DECKS_ADMIN).read())

serveur.shutdown()
print("\n%s" % ("TOUT PASSE" if not echecs else "ECHECS : " + ", ".join(echecs)))
sys.exit(1 if echecs else 0)
