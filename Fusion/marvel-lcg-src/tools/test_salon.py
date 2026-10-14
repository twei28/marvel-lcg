"""Teste les routes du SALON multijoueur (choix de heros/deck par siege).

Le serveur web repond des `Engine.Initialize()`, sans boucle de jeu : ce test
n'a donc pas besoin de creer une partie. Il tape les routes en HTTP, comme le
ferait un navigateur.

Il ACTIVE temporairement la protection des sieges (`seat_passwords`) dans le
launch.json du dossier de jeu, puis le REMET COMME AVANT en sortant : sans
cela, tous les tests suivants tourneraient avec des sieges proteges.

Usage: python3.10 tools/test_salon.py <game_dir> <port> [solo]
Avec « solo », la protection des sieges reste COUPEE : on verifie alors que le
salon se declare hors multi, ce qui rend tout le bloc salon du wizard inerte.
Viser .game-src, jamais .game (voir GUIDE-CREATION-CONTENU.md §8).
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

os.environ.setdefault("RELEASE", "1")

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
BASE = f"http://127.0.0.1:{PORT}"

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

MOTS_DE_PASSE = ["h0", "j1", "j2", "j3"]
MODE_SOLO = len(sys.argv) > 3 and sys.argv[3] == "solo"


def restaurer_config():
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)


os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["seat_passwords"] = [] if MODE_SOLO else MOTS_DE_PASSE
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

# Le moteur est bavard : on l'envoie dans un journal et on garde la sortie
# standard pour le compte rendu.
SORTIE = sys.stdout
sys.stdout = open("/tmp/test_salon_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def poster(corps, cookie=None):
    entetes = {"Content-Type": "application/json"}
    if cookie:
        entetes["Cookie"] = cookie
    requete = urllib.request.Request(
        BASE + "/set_choix_siege", data=json.dumps(corps).encode(), headers=entetes)
    try:
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            return reponse.status, json.load(reponse)
    except urllib.error.HTTPError as erreur:
        return erreur.code, {}


def lire():
    # Tolerante par construction : tant que la route n'existe pas, le serveur
    # repond autre chose que du JSON (il retombe sur son routage de fichiers).
    # Rendre {} laisse alors les verifications echouer proprement, au lieu de
    # faire exploser le script avant son compte rendu.
    try:
        with urllib.request.urlopen(BASE + "/get_choix_sieges", timeout=5) as reponse:
            return json.loads(reponse.read().decode("utf-8"))
    except Exception:
        return {}


def lire_liens(cookie=None):
    """GET /get_liens_sieges, avec ou sans jeton de siege.

    Rend (code, corps). Le corps est {} quand la reponse n'est pas du JSON :
    tant que la route n'existe pas, le serveur retombe sur son routage de
    fichiers, et on veut un echec lisible plutot qu'une exception.
    """
    entetes = {"Cookie": cookie} if cookie else {}
    requete = urllib.request.Request(BASE + "/get_liens_sieges", headers=entetes)
    try:
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            return reponse.status, json.loads(reponse.read().decode("utf-8"))
    except urllib.error.HTTPError as erreur:
        return erreur.code, {}
    except Exception:
        return 0, {}


def preparation(post=False, cookie=None):
    """/annoncer_preparation (POST) ou /get_preparation (GET) : rend (code, n)."""
    entetes = {"Cookie": cookie} if cookie else {}
    chemin = "/annoncer_preparation" if post else "/get_preparation"
    requete = urllib.request.Request(BASE + chemin, data=b"" if post else None, headers=entetes)
    try:
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            return reponse.status, json.loads(reponse.read().decode("utf-8")).get("n")
    except urllib.error.HTTPError as erreur:
        return erreur.code, None
    except Exception:
        return 0, None


def creer_partie():
    # Un VRAI descripteur, sur le modele de ce que construit le wizard
    # (public/js/prepare/launcher.js, buildDescriptor). Un descripteur invalide
    # ne conviendrait pas : /new echoue alors AVANT le vidage du salon, et c'est
    # voulu — on ne veut pas perdre les choix de tout le monde sur une requete
    # malformee.
    scenario = json.load(open("data/scenarios/rhino.json", encoding="utf-8"))
    deck = json.load(open("deck/starter/madame_web.json", encoding="utf-8"))
    descripteur = {
        "campaign_json": json.dumps(scenario),
        "encounter_set_names": scenario.get("encounter_sets", []),
        "hero_json": [json.dumps(deck)],
        "seed": 42,
        "timeout": 0,
        "challenges": [],
        "rules": [],
        "campaign_log": {},
    }
    url = BASE + "/new?data=" + urllib.parse.quote(json.dumps(descripteur))
    try:
        urllib.request.urlopen(url, timeout=30)
    except Exception:
        pass


try:
    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine import Engine
    Engine.Initialize()
    time.sleep(3)


    if MODE_SOLO:
        # Sans mot de passe de siege, le salon doit se declarer HORS multi :
        # c'est ce drapeau qui neutralise tout le bloc salon du wizard, et donc
        # qui garantit que le chemin SOLO n'a pas bouge.
        etat = lire()
        verifier("solo : le salon se declare hors multi",
                 etat.get("multi") is False, str(etat.get("multi")))
        code, _ = poster({"p": 1, "hero_card_id": "mw001a", "deck_id": "madame_web"})
        verifier("solo : aucune protection de siege, l'ecriture passe",
                 code == 200, f"code={code}")
        code, n = preparation(post=True)
        verifier("solo : annoncer la preparation ne fait rien", code == 200 and n == 0,
                 f"code={code} n={n}")
        code, corps = lire_liens()
        verifier("solo : aucun lien a distribuer",
                 code == 200 and corps.get("multi") is False and corps.get("cles") == [],
                 f"code={code} {corps}")
        raise SystemExit

    jeton_j1 = hashlib.md5(b"j1").hexdigest()
    cookie_j1 = f"seat_token_1={jeton_j1}"
    choix = {"p": 1, "hero_card_id": "mw001a", "deck_id": "madame_web",
             "deck_source": "base"}

    code, _ = poster(choix)
    verifier("sans jeton de siege -> 403", code == 403, f"code={code}")

    code, _ = poster(choix, cookie=f"seat_token_1={hashlib.md5(b'faux').hexdigest()}")
    verifier("avec un mauvais jeton -> 403", code == 403, f"code={code}")

    code, _ = poster(choix, cookie=cookie_j1)
    verifier("avec le bon jeton -> 200", code == 200, f"code={code}")

    etat = lire()
    verifier("multi detecte", etat.get("multi") is True, str(etat.get("multi")))
    siege1 = etat.get("sieges", {}).get("1", {})
    verifier("choix relu", siege1.get("hero_card_id") == "mw001a",
             json.dumps(etat.get("sieges")))
    verifier("deck relu", siege1.get("deck_id") == "madame_web",
             json.dumps(etat.get("sieges")))

    code, _ = poster({"p": 1, "hero_card_id": "", "deck_id": ""}, cookie=cookie_j1)
    verifier("choix incomplet -> 400", code == 400, f"code={code}")

    code, _ = poster({"p": 2, "hero_card_id": "mw001a", "deck_id": "madame_web"},
                     cookie=cookie_j1)
    verifier("le jeton du siege 1 ne vaut pas pour le siege 2 -> 403",
             code == 403, f"code={code}")

    # Changement d'avis : le dernier choix ecrase le precedent.
    poster({"p": 1, "hero_card_id": "01001a", "deck_id": "spider_man",
            "deck_source": "base"}, cookie=cookie_j1)
    verifier("changement d'avis pris en compte",
             lire().get("sieges", {}).get("1", {}).get("hero_card_id") == "01001a",
             json.dumps(lire().get("sieges")))

    # --- Les cles de siege ne sortent que pour l'HOTE ----------------------
    # Une cle OUVRE un siege : la rendre a qui la demande laisserait n'importe
    # quel visiteur de la partie s'asseoir a la place d'un invite. Ces trois cas
    # sont la raison d'etre de la route, pas un ornement.
    jeton_h0 = hashlib.md5(b"h0").hexdigest()
    cookie_h0 = f"seat_token_0={jeton_h0}"

    code, corps = lire_liens()
    verifier("liens : sans jeton -> 403", code == 403, f"code={code} {corps}")

    code, corps = lire_liens(cookie=cookie_j1)
    verifier("liens : le jeton d'un INVITE ne suffit pas -> 403",
             code == 403, f"code={code} {corps}")

    code, corps = lire_liens(cookie=f"seat_token_0={hashlib.md5(b'faux').hexdigest()}")
    verifier("liens : un mauvais jeton d'hote -> 403", code == 403, f"code={code}")

    code, corps = lire_liens(cookie=cookie_h0)
    verifier("liens : l'hote recoit les quatre cles",
             code == 200 and corps.get("multi") is True
             and corps.get("cles") == MOTS_DE_PASSE, f"code={code} {corps}")

    # --- L'equipe reste ensemble (13/10/2026) -------------------------------
    # L'hote qui rouvre la preparation fait avancer un compteur ; les invites
    # restes sur l'ecran de fin le lisent et reviennent au salon. Un invite ne
    # doit pas pouvoir l'avancer : il expedierait les autres au salon.
    code, avant = preparation()
    verifier("preparation : compteur lisible par tous", code == 200 and avant == 0,
             f"code={code} n={avant}")
    code, _ = preparation(post=True)
    verifier("preparation : sans jeton -> 403", code == 403, f"code={code}")
    code, _ = preparation(post=True, cookie=cookie_j1)
    verifier("preparation : un invite n'annonce rien -> 403", code == 403, f"code={code}")
    code, n = preparation(post=True, cookie=cookie_h0)
    verifier("preparation : l'hote annonce, le compteur avance",
             code == 200 and n == 1 and preparation()[1] == 1, f"code={code} n={n}")

    # --- La page du salon est-elle servie, et le lien y mene-t-il ? ---------
    # Le RENDU (grille de heros, liste de decks) demande un navigateur : il est
    # couvert par le test a deux de la tache 5. Ici on verifie seulement que le
    # routage et le service des fichiers sont en place.
    def texte(chemin):
        try:
            with urllib.request.urlopen(BASE + chemin, timeout=5) as reponse:
                return reponse.status, reponse.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as erreur:
            return erreur.code, ""

    code, page = texte("/salon.html")
    verifier("/salon.html est servie", code == 200 and "salon-choix" in page,
             f"code={code}")

    code, script = texte("/public/js/salon/app.js")
    verifier("le script du salon est servi",
             code == 200 and "set_choix_siege" in script, f"code={code}")

    # public/js/prepare/app.js IMPORTE ce module : s'il n'est pas servi, c'est
    # TOUT le wizard qui casse, y compris en solo. C'est le risque le plus
    # serieux de ce chantier, il merite sa verification.
    code, module = texte("/public/js/prepare/salon-etat.js")
    verifier("le module de decision est servi au wizard",
             code == 200 and "export function etatSalon" in module, f"code={code}")

    class SansRedirection(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None

    ouvreur = urllib.request.build_opener(SansRedirection)
    try:
        ouvreur.open(BASE + "/claim_seat?p=1&key=j1&to=salon", timeout=5)
        code, cible = 0, ""
    except urllib.error.HTTPError as erreur:
        code, cible = erreur.code, erreur.headers.get("Location", "")
    verifier("le lien invite mene au salon",
             code == 302 and cible == "/salon.html?p=1", f"code={code} -> {cible}")

    # --- La roue de « Partie au hasard » (08/10/2026) ----------------------
    # L'hote lance tout et relance le scenario ; chacun ne relance que SON
    # heros (decision 8 de .planning/todos/2026-10-08-roue-du-hasard.md).
    def poster_roue(corps, cookie=None):
        entetes = {"Content-Type": "application/json"}
        if cookie:
            entetes["Cookie"] = cookie
        requete = urllib.request.Request(
            BASE + "/set_roue", data=json.dumps(corps).encode(), headers=entetes)
        try:
            with urllib.request.urlopen(requete, timeout=5) as reponse:
                return reponse.status, json.load(reponse)
        except urllib.error.HTTPError as erreur:
            return erreur.code, {}

    def lire_roue():
        try:
            with urllib.request.urlopen(BASE + "/get_roue", timeout=5) as reponse:
                return json.loads(reponse.read().decode("utf-8")).get("roue")
        except Exception:
            return "illisible"

    verifier("roue : aucune avant le premier lancer", lire_roue() is None, str(lire_roue()))
    tirage = {"quoi": "tout", "nombre": 2, "fanmade": False,
              "heros": {"0": "spider_man", "1": "iron_man"}, "scenario": "rhino"}
    code, _ = poster_roue(tirage, cookie=cookie_j1)
    verifier("roue : un invite ne lance pas tout -> 403", code == 403, f"code={code}")
    code, _ = poster_roue(tirage, cookie=cookie_h0)
    roue = lire_roue() or {}
    verifier("roue : l'hote lance, tout le monde relit le meme tirage",
             code == 200 and roue.get("heros", {}).get("1", {}).get("id") == "iron_man"
             and roue.get("scenario", {}).get("id") == "rhino", f"code={code} {roue}")
    code, _ = poster_roue({"quoi": "heros", "p": 1, "id": "she_hulk"}, cookie=cookie_j1)
    roue = lire_roue() or {}
    verifier("roue : l'invite relance SON heros, le compteur avance",
             code == 200 and roue.get("heros", {}).get("1") == {"id": "she_hulk", "n": 2},
             f"code={code} {roue}")
    code, _ = poster_roue({"quoi": "heros", "p": 0, "id": "she_hulk"}, cookie=cookie_j1)
    verifier("roue : l'invite ne relance pas le heros de l'hote -> 403", code == 403, f"code={code}")
    code, _ = poster_roue({"quoi": "scenario", "id": "klaw"}, cookie=cookie_j1)
    verifier("roue : l'invite ne relance pas le scenario -> 403", code == 403, f"code={code}")
    code, _ = poster_roue({"quoi": "heros", "p": 3, "id": "zeus"}, cookie=cookie_h0)
    verifier("roue : un siege hors de la partie -> 400", code == 400, f"code={code}")
    code, _ = poster_roue({"quoi": "scenario", "id": "klaw"}, cookie=cookie_h0)
    verifier("roue : l'hote relance le scenario",
             code == 200 and (lire_roue() or {}).get("scenario", {}).get("n") == 2, f"code={code}")

    creer_partie()
    verifier("le salon est vide apres /new", lire().get("sieges") == {},
             json.dumps(lire().get("sieges")))
    verifier("roue : effacee au lancement de la partie", lire_roue() is None, str(lire_roue()))

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
