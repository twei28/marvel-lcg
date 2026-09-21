"""« Quitter la partie » : le moteur demande au SITE de fermer la table.

Pourquoi cette route existe (21/09/2026). Le bouton « Menu » du plateau ne
faisait que naviguer vers `/prepare.html` : le moteur gardait son monde
charge, l'emplacement restait pris, et le salon des invites, qui bascule des
que la table porte une partie, expediait tout le monde sur l'ANCIENNE. Deux
soirees perdues. `/quitter_la_table` rend la table a son neant.

Ce que ce test verifie, et que rien d'autre ne voit :

  — un INVITE ne ferme pas la table de l'hote (c'est le seul garde-fou :
    cote site, le jeton dit de quelle TABLE vient l'appel, pas qui a clique) ;
  — l'appel part bien vers `/api/eteindre`, avec le jeton de la partie, en
    127.0.0.1 : le navigateur ne peut pas le faire lui-meme, le site est sur
    un autre domaine que le moteur ;
  — l'adresse d'atterrissage vient du SITE et ressort telle quelle. Sans
    elle, le plateau resterait sur une page du moteur qu'on vient de tuer ;
  — sans site derriere (partie locale), la route ne PROMET rien : elle dit
    qu'il n'y avait rien a fermer, et le plateau reste sur l'ecran des heros ;
  — ⚠ ET LE CAS QUI AFFIRMERAIT LE FAUX : un site SOLLICITE qui ne confirme
    pas. `/api/eteindre` revoque le mot de passe et lance l'extinction AVANT
    de repondre : passe le plafond de dix secondes, la table disparait quand
    meme. Dire « rien n'a ete detruit » serait un mensonge, et proposer de
    rester sur la partie, une impasse. La route dit donc « inconnue », et rend
    l'adresse du site pour aller voir.

Usage: python3.10 tools/test_quitter_la_table.py <game_dir> <port>
                                                 [sans_site|site_muet]
Viser un dossier jetable, jamais .game ni .game-src.
"""
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

os.environ.setdefault("RELEASE", "1")

# ⚠ ABSOLU AVANT TOUT. On fait `os.chdir(GAME_DIR)` plus bas : un chemin
# relatif ne designerait plus le meme dossier une fois la config relue.
GAME_DIR = os.path.abspath(os.path.expanduser(sys.argv[1]))
PORT = int(sys.argv[2])
BASE = f"http://127.0.0.1:{PORT}"
MODE = sys.argv[3] if len(sys.argv) > 3 else ""
SANS_SITE = MODE == "sans_site"
# Le site repond, mais pas ce qu'il faut : c'est le cas du site trop lent, du
# deploiement en cours, du 502 de passage.
SITE_MUET = MODE == "site_muet"

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

MOTS_DE_PASSE = ["h0", "j1", "j2", "j3"]
JETON_SITE = "jeton-de-la-table"
SITE_PUBLIC = "https://exemple.test"

# --- Le faux SITE ----------------------------------------------------------
# ⚠ IL FAUT UN VRAI SERVEUR. `_appeler_site` passe par aiohttp, en 127.0.0.1,
# avec un corps urlencode : le remplacer par un bouchon ne prouverait ni le
# chemin appele, ni le jeton envoye, c'est-a-dire rien de ce qui casse.
recu = []


class FauxSite(BaseHTTPRequestHandler):
    def do_POST(self):
        taille = int(self.headers.get("Content-Length") or 0)
        corps = self.rfile.read(taille).decode("utf-8", "replace")
        recu.append((self.path, corps))
        if SITE_MUET:
            # ⚠ IL A RECU L'APPEL. C'est tout le piege : cote site, la
            # revocation et le fil d'extinction sont deja partis.
            self.send_response(503)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        reponse = json.dumps({"ok": True, "url": SITE_PUBLIC + "/arret"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reponse)))
        self.end_headers()
        self.wfile.write(reponse)

    def log_message(self, *args):
        pass


_site = HTTPServer(("127.0.0.1", 0), FauxSite)
PORT_SITE = _site.server_address[1]
threading.Thread(target=_site.serve_forever, daemon=True).start()


def restaurer_config():
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)


os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["seat_passwords"] = MOTS_DE_PASSE
# Partie LOCALE : aucun site derriere. C'est le cas du joueur qui lance
# JOUER-SOLO.bat, et la route ne doit alors rien promettre.
cfg["site_interne"] = "" if SANS_SITE else f"http://127.0.0.1:{PORT_SITE}"
cfg["site_jeton"] = "" if SANS_SITE else JETON_SITE
# L'adresse PUBLIQUE, celle que le moteur rend quand il ne sait pas si la
# table s'est fermee : le joueur doit pouvoir aller le constater lui-meme.
cfg["site_url"] = SITE_PUBLIC
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

SORTIE = sys.stdout
sys.stdout = open("/tmp/test_quitter_la_table_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def quitter(cookie=None):
    """POST /quitter_la_table. Rend (code, corps), corps vide si ce n'est pas du JSON.

    Tolerante par construction : tant que la route n'existe pas, le moteur
    retombe sur son routage de fichiers et repond autre chose que du JSON. On
    veut alors un echec lisible, pas une exception avant le compte rendu.
    """
    entetes = {"Content-Type": "application/json"}
    if cookie:
        entetes["Cookie"] = cookie
    requete = urllib.request.Request(BASE + "/quitter_la_table", data=b"{}",
                                     headers=entetes)
    try:
        with urllib.request.urlopen(requete, timeout=15) as reponse:
            return reponse.status, json.loads(reponse.read().decode("utf-8"))
    except urllib.error.HTTPError as erreur:
        return erreur.code, {}
    except Exception:
        return 0, {}


try:
    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine import Engine
    Engine.Initialize()
    time.sleep(3)

    cookie_h0 = "seat_token_0=" + hashlib.md5(b"h0").hexdigest()
    cookie_j1 = "seat_token_1=" + hashlib.md5(b"j1").hexdigest()

    if SANS_SITE:
        # ⚠ AUCUNE PROMESSE SANS SITE. Repondre « fermee » ici enverrait le
        # joueur solo sur une adresse qui n'existe pas, apres lui avoir
        # annonce que sa table allait disparaitre.
        code, corps = quitter(cookie=cookie_h0)
        verifier("sans site : la route le DIT, au lieu de rester vague",
                 code == 200 and corps.get("issue") == "sans-site", f"code={code} {corps}")
        verifier("sans site : aucune adresse d'atterrissage",
                 corps.get("url") == "", str(corps.get("url")))
        verifier("sans site : personne n'a ete appele", recu == [], str(recu))
        raise SystemExit

    if SITE_MUET:
        # ⚠ LE CAS QUI AFFIRMERAIT LE FAUX. Le site a RECU l'appel : il a
        # revoque le mot de passe et lance l'extinction avant de repondre. Le
        # moteur ne sait pas si la table s'est fermee, et il ne doit pretendre
        # ni l'un ni l'autre.
        code, corps = quitter(cookie=cookie_h0)
        verifier("site muet : l'issue est INCONNUE, ni fermee ni sans-site",
                 code == 200 and corps.get("issue") == "inconnue", f"code={code} {corps}")
        verifier("site muet : le site a pourtant bien ete sollicite",
                 len(recu) == 1 and recu[0][0] == "/api/eteindre", str(recu))
        # Ne rien affirmer, mais donner de quoi aller voir : c'est la seule
        # chose honnete a offrir ici.
        verifier("site muet : l'adresse du site est quand meme donnee",
                 corps.get("url") == SITE_PUBLIC, str(corps.get("url")))
        raise SystemExit

    # --- Fermer la table est le geste de l'HOTE, et de lui seul ------------
    code, corps = quitter()
    verifier("sans jeton de siege -> 403", code == 403, f"code={code} {corps}")
    verifier("et rien n'est parti vers le site", recu == [], str(recu))

    code, corps = quitter(cookie=cookie_j1)
    verifier("un INVITE ne ferme pas la table de l'hote -> 403",
             code == 403, f"code={code} {corps}")
    verifier("et la encore, rien n'est parti vers le site", recu == [], str(recu))

    code, corps = quitter(cookie="seat_token_0=" + hashlib.md5(b"faux").hexdigest())
    verifier("un mauvais jeton d'hote -> 403", code == 403, f"code={code}")

    # ⚠ LE DOUBLE VERROU DU SPECTATEUR. `SpectateurPeutEcrire` refuse par
    # defaut toute ECRITURE a qui porte le cookie `spectateur`, avant meme la
    # garde de siege. Le temoin vaut d'etre ecrit parce qu'il combine les
    # deux : un spectateur qui aurait AUSSI la cle de l'hote ne doit pas
    # fermer la table. Sans lui, ajouter un jour ce chemin a la liste
    # nommement ouverte passerait inapercu.
    code, corps = quitter(cookie=f"spectateur=1; {cookie_h0}")
    verifier("un SPECTATEUR ne ferme rien, meme avec la cle de l'hote",
             code == 403, f"code={code} {corps}")
    verifier("et rien n'est parti vers le site pour lui non plus",
             recu == [], str(recu))

    # --- L'hote, lui, ferme bien la table ----------------------------------
    code, corps = quitter(cookie=cookie_h0)
    verifier("l'hote obtient la fermeture",
             code == 200 and corps.get("issue") == "fermee", f"code={code} {corps}")
    # ⚠ L'ADRESSE VIENT DU SITE, ET RESSORT TELLE QUELLE. Le moteur ne connait
    # pas le domaine public place devant lui, et il n'aura plus de page a
    # offrir une seconde apres cette reponse.
    verifier("et l'adresse ou atterrir, celle que le site a donnee",
             corps.get("url") == SITE_PUBLIC + "/arret", str(corps.get("url")))
    verifier("le site a bien ete appele sur /api/eteindre",
             len(recu) == 1 and recu[0][0] == "/api/eteindre", str(recu))
    verifier("avec le jeton de la partie, et lui seul",
             len(recu) == 1 and ("jeton=" + JETON_SITE) in recu[0][1], str(recu))

except SystemExit:
    pass
except Exception as exc:
    import traceback
    traceback.print_exc()
    verifier("le test lui-meme a plante", False, f"{type(exc).__name__}: {exc}")
finally:
    restaurer_config()

for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"   [{detail}]"),
          file=SORTIE)
rates = [nom for nom, ok, _ in resultats if not ok]
print(("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)"), file=SORTIE)
SORTIE.flush()
# os._exit et pas sys.exit : le serveur web laisse des threads vivants, un
# arret propre attendrait indefiniment.
os._exit(0 if not rates else 1)
