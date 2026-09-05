"""Le moteur exige-t-il son mot de passe, et le lien de siege l'en dispense-t-il ?

Ce test existe a cause d'un defaut precis : `launcher.py` et `launcher_fast.py`
debranchaient `WebServer.IsAuthenticate` en dur. Sans consequence tant que le
jeu tournait sur la machine de son proprietaire, desastreux des qu'il est servi
sur un domaine public — n'importe qui trouvant l'adresse entrait dans la partie.

⚠ CE TEST N'A DE SENS QUE S'IL NE DEBRANCHE RIEN. Les autres outils du dossier
posent `WebServer.IsAuthenticate = lambda ...: True` pour aller droit au but ;
le faire ici viderait le test de tout contenu. Il ne neutralise donc que
`IsVersionMatch`, comme les lanceurs, parce qu'elle reclame un cookie
`app_version` qu'aucun premier visiteur ne possede.

Usage: python3.10 tools/test_authentification.py <game_dir> <port> [ouvert]
Avec « ouvert », aucun mot de passe n'est configure : on verifie alors que le
jeu LOCAL reste entierement accessible, ce qui est le vrai risque de regression.
Viser .game-src, jamais .game (voir GUIDE-CREATION-CONTENU.md §8).
"""
import hashlib
import http.cookies
import json
import os
import sys
import time
import urllib.error
import urllib.request

os.environ.setdefault("RELEASE", "1")

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
BASE = f"http://127.0.0.1:{PORT}"
MODE_OUVERT = len(sys.argv) > 3 and sys.argv[3] == "ouvert"

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

MOT_DE_PASSE = "secret-de-la-partie"
CLES = ["h0", "j1", "j2", "j3"]


def restaurer_config():
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)


os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["password"] = "" if MODE_OUVERT else MOT_DE_PASSE
cfg["seat_passwords"] = [] if MODE_OUVERT else CLES
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

SORTIE = sys.stdout
sys.stdout = open("/tmp/test_authentification_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


class SansRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def demander(chemin, cookie=None, suivre=True):
    """Rend (code, corps, cookies_poses)."""
    entetes = {"Cookie": cookie} if cookie else {}
    requete = urllib.request.Request(BASE + chemin, headers=entetes)
    ouvreur = urllib.request.build_opener() if suivre else \
        urllib.request.build_opener(SansRedirection)
    try:
        with ouvreur.open(requete, timeout=5) as reponse:
            return reponse.status, reponse.read().decode("utf-8", "replace"), \
                reponse.headers.get_all("Set-Cookie") or []
    except urllib.error.HTTPError as erreur:
        return erreur.code, "", erreur.headers.get_all("Set-Cookie") or []
    except Exception as exc:
        return 0, str(exc), []


def noms_de_cookies(entetes):
    noms = []
    for brut in entetes:
        morceau = http.cookies.SimpleCookie()
        morceau.load(brut)
        noms.extend(morceau.keys())
    return noms


try:
    from engine.network.web_server import WebServer
    # ⚠ On ne touche PAS a IsAuthenticate : c'est precisement l'objet du test.
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine import Engine
    Engine.Initialize()
    time.sleep(3)

    if MODE_OUVERT:
        # Sans mot de passe configure, le jeu local doit rester grand ouvert :
        # c'est le seul usage quotidien, et la regression la plus couteuse.
        code, page, _ = demander("/prepare.html")
        verifier("ouvert : l'ecran de preparation s'affiche",
                 code == 200 and "Authenticate" not in page, f"code={code}")
        code, corps, _ = demander("/get_choix_sieges")
        verifier("ouvert : les donnees repondent en JSON",
                 code == 200 and corps.lstrip().startswith("{"), corps[:60])
        code, _, _ = demander("/galerie.html")
        verifier("ouvert : la galerie est joignable", code == 200, f"code={code}")
        raise SystemExit

    # --- 1. L'inconnu est arrete -------------------------------------------
    code, page, _ = demander("/prepare.html")
    verifier("inconnu : l'ecran de preparation est remplace par le mot de passe",
             code == 200 and "Authenticate" in page and "Prepare a game" not in page,
             f"code={code} {page[:80]}")

    code, corps, _ = demander("/get_choix_sieges")
    verifier("inconnu : les donnees ne sortent pas",
             not corps.lstrip().startswith("{"), corps[:60])

    code, corps, _ = demander("/get_liens_sieges")
    verifier("inconnu : les cles de siege ne sortent pas",
             not corps.lstrip().startswith("{"), corps[:60])

    # --- 2. Le lien de siege ouvre la porte ---------------------------------
    code, _, cookies = demander(f"/claim_seat?p=0&key={CLES[0]}&to=prepare", suivre=False)
    poses = noms_de_cookies(cookies)
    verifier("hote : son lien redirige vers l'ecran de preparation",
             code == 302, f"code={code}")
    verifier("hote : son lien pose le jeton de session",
             "session_token" in poses, str(poses))
    verifier("hote : son lien pose aussi le jeton de son siege",
             "seat_token_0" in poses, str(poses))

    jeton = hashlib.md5(MOT_DE_PASSE.encode()).hexdigest()
    cookie_hote = f"session_token={jeton}; seat_token_0={hashlib.md5(CLES[0].encode()).hexdigest()}"
    code, page, _ = demander("/prepare.html", cookie=cookie_hote)
    verifier("hote : avec ses jetons, il entre",
             "Prepare a game" in page and "Authenticate" not in page, page[:80])

    # --- 3. L'invite entre aussi, mais n'a pas les cles ---------------------
    code, _, cookies = demander(f"/claim_seat?p=1&key={CLES[1]}&to=salon", suivre=False)
    poses = noms_de_cookies(cookies)
    verifier("invite : son lien mene au salon", code == 302, f"code={code}")
    verifier("invite : son lien lui ouvre aussi la porte",
             "session_token" in poses, str(poses))

    cookie_invite = f"session_token={jeton}; seat_token_1={hashlib.md5(CLES[1].encode()).hexdigest()}"
    code, corps, _ = demander("/get_liens_sieges", cookie=cookie_invite)
    verifier("invite : les cles lui restent refusees", code == 403, f"code={code}")

    # --- 4. Une mauvaise cle n'ouvre rien -----------------------------------
    code, _, cookies = demander("/claim_seat?p=1&key=NIMPORTEQUOI&to=salon", suivre=False)
    verifier("mauvaise cle : refusee", code == 403, f"code={code}")
    verifier("mauvaise cle : aucun jeton pose",
             "session_token" not in noms_de_cookies(cookies), str(noms_de_cookies(cookies)))

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
os._exit(0 if not rates else 1)
