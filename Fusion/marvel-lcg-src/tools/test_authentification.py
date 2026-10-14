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


def poster(chemin, charge, cookie=None):
    """Rend le code HTTP d'un POST JSON."""
    import json as json_lib
    entetes = {"Content-Type": "application/json"}
    if cookie:
        entetes["Cookie"] = cookie
    requete = urllib.request.Request(
        BASE + chemin, data=json_lib.dumps(charge).encode("utf-8"),
        headers=entetes, method="POST")
    try:
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            return reponse.status
    except urllib.error.HTTPError as erreur:
        return erreur.code
    except Exception:
        return 0


def noms_de_cookies(entetes):
    cookies = {}
    for brut in entetes:
        morceau = http.cookies.SimpleCookie()
        morceau.load(brut)
        cookies.update({nom: valeur.value for nom, valeur in morceau.items()})
    return cookies


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

    code, corps, _ = demander("/get_heros_du_siege?p=0")
    verifier("inconnu : le heros d'un siege ne sort pas",
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
    verifier("hote V1 : son lien n'active pas la V2",
             "ui_version" not in poses or poses.get("ui_version") == "", str(poses))

    code, _, cookies = demander(
        f"/claim_seat?p=0&key={CLES[0]}&to=prepare-v2", suivre=False)
    poses = noms_de_cookies(cookies)
    verifier("hote V2 : sa cle valide active la V2",
             code == 302 and poses.get("ui_version") == "v2",
             f"code={code}, cookies={poses}")

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
    verifier("invite : son lien n'active pas la V2",
             "ui_version" not in poses or poses.get("ui_version") == "", str(poses))

    code, _, cookies = demander(
        f"/claim_seat?p=1&key={CLES[1]}&to=prepare-v2", suivre=False)
    verifier("invite : demander prepare-v2 ne lui active pas la V2",
             code == 302 and noms_de_cookies(cookies).get("ui_version") != "v2",
             f"code={code}, cookies={noms_de_cookies(cookies)}")

    cookie_invite = f"session_token={jeton}; seat_token_1={hashlib.md5(CLES[1].encode()).hexdigest()}"
    code, corps, _ = demander("/get_liens_sieges", cookie=cookie_invite)
    verifier("invite : les cles lui restent refusees", code == 403, f"code={code}")

    # ⚠ LA ROUTE QUI DIT QUI TIENT UN SIEGE (21/09/2026). Le salon s'en sert
    # pour savoir si la partie qui demarre est la SIENNE, au lieu de basculer
    # des qu'une partie tourne — ce qui expediait les invites dans la partie
    # precedente (defaut du 20/09). Elle est gardee comme `set_choix_siege` :
    # qui a le droit d'ecrire ce siege a le droit de savoir ce qu'il tient, et
    # personne ne lit le siege d'un autre.
    code, corps, _ = demander("/get_heros_du_siege?p=1", cookie=cookie_invite)
    verifier("invite : il peut interroger SON siege",
             code == 200 and corps.lstrip().startswith("{"), f"code={code} {corps[:60]}")
    code, corps, _ = demander("/get_heros_du_siege?p=2", cookie=cookie_invite)
    verifier("invite : le siege d'un AUTRE lui est refuse", code == 403, f"code={code}")

    # ⚠ ET IL N'ECRIT PAS NON PLUS LE SIEGE D'UN AUTRE. `set_choix_siege`
    # gardait encore `allowed_seats` : un invite du siege 1 posait le heros du
    # siege 2, qui partait alors avec le deck d'un autre — et, depuis que le
    # salon compare, restait bloque sans jamais se reconnaitre.
    code = poster("/set_choix_siege",
                  {"p": 1, "hero_card_id": "01001a", "deck_id": "spider_man"},
                  cookie=cookie_invite)
    verifier("invite : il pose SON choix", code == 200, f"code={code}")
    code = poster("/set_choix_siege",
                  {"p": 2, "hero_card_id": "01001a", "deck_id": "spider_man"},
                  cookie=cookie_invite)
    verifier("invite : le choix d'un AUTRE siege lui est refuse", code == 403, f"code={code}")

    # ⚠ LE SPECTATEUR, ET C'EST LA CLASSE EXACTE DE LA FUITE DU 15/09.
    # `SpectateurPeutLire` ouvre les routes par PREFIXE `/get_` : rien
    # n'arrete un spectateur sur `/get_heros_du_siege` sinon la garde de siege
    # elle-meme. Il n'a aucun `seat_token`, donc `tient_le_siege` le refuse —
    # mais c'est `tient_le_siege` qui le fait, et pas autre chose.
    cookie_spectateur = f"session_token={jeton}; spectateur=1"
    code, _, _ = demander("/get_heros_du_siege?p=0", cookie=cookie_spectateur)
    verifier("spectateur : le heros d'un siege lui est refuse", code == 403, f"code={code}")
    code, _, _ = demander("/get_heros_du_siege?p=2", cookie=cookie_spectateur)
    verifier("spectateur : aucun siege ne s'ouvre a lui", code == 403, f"code={code}")

    # ⚠ L'EQUIPE DU SALON (09/10/2026). L'hote publie les heros et le scenario
    # (jamais un deck), l'invite les lit. Seul le siege 0 ecrit ; chacun ne lit
    # que depuis son propre siege ; le spectateur n'entre pas.
    corps_equipe = {"nombre": 2, "heros": {"0": "01001a"}, "scenario": ""}
    code = poster("/set_equipe_hote", corps_equipe, cookie=cookie_invite)
    verifier("invite : il ne publie pas l'equipe de l'hote", code == 403, f"code={code}")
    code = poster("/set_equipe_hote", corps_equipe, cookie=cookie_hote)
    verifier("hote : il publie l'equipe", code == 200, f"code={code}")
    code, corps, _ = demander("/get_equipe_salon?p=1", cookie=cookie_invite)
    verifier("invite : il lit l'equipe depuis SON siege",
             code == 200 and '"01001a"' in corps and "deck" not in corps, f"code={code} {corps[:80]}")
    code, _, _ = demander("/get_equipe_salon?p=2", cookie=cookie_invite)
    verifier("invite : l'equipe lue depuis le siege d'un AUTRE lui est refusee", code == 403, f"code={code}")
    code, _, _ = demander("/get_equipe_salon?p=0", cookie=cookie_spectateur)
    verifier("spectateur : l'equipe du salon lui est refusee", code == 403, f"code={code}")

    # --- 4. Une mauvaise cle n'ouvre rien -----------------------------------
    code, _, cookies = demander("/claim_seat?p=1&key=NIMPORTEQUOI&to=salon", suivre=False)
    verifier("mauvaise cle : refusee", code == 403, f"code={code}")
    verifier("mauvaise cle : aucun jeton pose",
             "session_token" not in noms_de_cookies(cookies), str(noms_de_cookies(cookies)))
    code, _, cookies = demander(
        "/claim_seat?p=0&key=NIMPORTEQUOI&to=prepare-v2", suivre=False)
    verifier("mauvaise cle : impossible d'activer la V2",
             code == 403 and "ui_version" not in noms_de_cookies(cookies),
             f"code={code}, cookies={noms_de_cookies(cookies)}")

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
