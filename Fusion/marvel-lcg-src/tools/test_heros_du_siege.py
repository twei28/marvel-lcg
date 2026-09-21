"""La route `/get_heros_du_siege` dit-elle QUI tient un siege, et rien de plus ?

Ce test existe a cause d'un defaut precis, constate deux fois dans la soiree du
20/09/2026. Le salon basculait vers le plateau des que `/get_play_scene_name`
rendait autre chose qu'une chaine vide, en supposant que la table est VIDE avant
que l'hote lance. Elle ne l'est pas : le moteur rend le nom de scene des qu'un
MONDE existe, et il en existe un jusqu'au redemarrage. Des invites ont donc ete
expedies dans la partie PRECEDENTE avant d'avoir choisi leur heros.

La route mesuree ici est la reponse : elle dit quel heros tient UN siege dans la
partie EN COURS, pour que le salon puisse se demander « cette partie est-elle la
MIENNE ? » au lieu de « une partie tourne-t-elle ? ».

Ce que ce fichier prouve, et qu'aucune lecture de code ne prouve :
  1. Aucune partie chargee -> `en_jeu` faux (donc personne n'est envoye nulle part).
  2. Une partie chargee -> le siege rend l'identifiant de sa carte HEROS, sous la
     forme EXACTE que le salon compare (`01001a`, le deck portant '01001a,01001b').
  3. Chaque siege rend le SIEN, pas celui du voisin.
  4. Un siege que la partie n'a pas -> `en_jeu` vrai et `heros` vide : c'est
     ainsi que le salon distingue « l'hote a lance sans moi » d'une attente.
  5. Un `p` absent, illisible ou negatif -> 400, pas une reponse au hasard.
  6. ⚠ `debut` CHANGE d'une partie a l'autre MEME QUAND LE HEROS NE CHANGE PAS.
     C'est le coeur de la ronde de correction du 21/09 : rejouer une manche
     avec le meme heros rouvrait le defaut en grand, et seul ce repere de
     fraicheur le ferme. Il vaut "" quand aucune partie ne tourne.
  7. ⚠ ... ET IL NE BOUGE PAS quand la MEME scene est reposee (une annulation
     de geste, un rejeu sur place). Sans quoi tout tenant de siege — et pas
     seulement l'hote — ferait basculer les invites du salon a volonte.

Usage: python3.10 tools/test_heros_du_siege.py <game_dir> <port>
Viser un dossier de jeu JETABLE, jamais `.game` ni `.game-src` : ce test
reecrit `launch.json` (il le restaure, mais une interruption ne le ferait pas).
"""
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

os.environ.setdefault("RELEASE", "1")

GAME_DIR = os.path.abspath(os.path.expanduser(sys.argv[1]))
PORT = int(sys.argv[2])
BASE = f"http://127.0.0.1:{PORT}"

# Deux heros, pour que « chaque siege rend le SIEN » ait un sens. Les decks de
# depart portent leurs identites sous la forme '01001a,01001b' : c'est ce
# decoupage sur la virgule que la route doit refaire, sinon la comparaison avec
# le `heroCardId` du salon echouerait sur toute carte a variantes.
HEROS = ["spider_man", "she_hulk"]
ATTENDU = ["01001a", "01019a"]
SCENARIO = "rhino"

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["password"] = ""
cfg["seat_passwords"] = []
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

# Le moteur est bavard : on le range dans un journal et on garde la sortie
# propre pour les verdicts.
SORTIE = sys.stdout
sys.stdout = open("/tmp/test_heros_du_siege_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def demander(chemin):
    """Rend (code, objet JSON ou None)."""
    try:
        with urllib.request.urlopen(BASE + chemin, timeout=5) as reponse:
            corps = reponse.read().decode("utf-8", "replace")
            try:
                return reponse.status, json.loads(corps)
            except Exception:
                return reponse.status, None
    except urllib.error.HTTPError as erreur:
        return erreur.code, None
    except Exception as exc:
        return 0, {"exception": str(exc)}


def restaurer_config():
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)


try:
    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine.device.manager.base import DeviceManager

    # Le pilote ne joue RIEN : ce test ne mesure pas une partie, il mesure une
    # route. Il suffit que le monde existe. Ne jamais repondre laisse le fil du
    # jeu « en attente d'entree », ce qui est exactement l'etat d'une table dont
    # les joueurs n'ont pas encore agi — et il rend le GIL a chaque tranche,
    # sans quoi le fil principal serait affame (lecon du 18/09/2026, voir
    # tools/test_mode_manuel.py).
    def pilote(self, data, player_id=None, check=None):
        while True:
            time.sleep(0.5)

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    time.sleep(3)

    # --- 1. Aucune partie : personne ne part nulle part ---------------------
    code, corps = demander("/get_heros_du_siege?p=0")
    verifier("table neuve : la route repond", code == 200 and corps is not None, f"code={code}")
    verifier("table neuve : aucune partie en cours",
             bool(corps) and corps.get("en_jeu") is False, str(corps))
    verifier("table neuve : aucun heros a annoncer",
             bool(corps) and corps.get("heros") == "", str(corps))
    verifier("table neuve : aucun repere de partie",
             bool(corps) and corps.get("debut") == "", str(corps))

    # --- 2. Une vraie partie, deux heros ------------------------------------
    from engine.file import FileManager
    from game.scene.loader import SceneLoader

    def lire(genre, nom):
        chemin = FileManager.FindJsonPath(genre, nom)
        assert chemin, f"{genre} {nom} introuvable"
        with open(chemin, encoding="utf-8") as f:
            return f.read()

    scene = SceneLoader.NewFromJson(
        lire("Campaign", SCENARIO), None, [lire("Hero", h) for h in HEROS], 42, [], {})
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        while True:
            jeu.GameSetup()
            jeu.GameLoop()
            if jeu.SetGameOver():
                break

    threading.Thread(target=run, daemon=True).start()

    # Le monde n'est pas pose a l'instant ou la scene l'est : on attend qu'il
    # apparaisse, borne, plutot que de dormir au hasard.
    limite = time.time() + 60
    while jeu.world is None and time.time() < limite:
        time.sleep(0.5)
    verifier("le monde est bien monte", jeu.world is not None, "monde absent apres 60s")

    code, corps = demander("/get_heros_du_siege?p=0")
    verifier("partie en cours : le siege 0 est annonce en jeu",
             bool(corps) and corps.get("en_jeu") is True, str(corps))
    # ⚠ LE COEUR DU TEST. Le deck de depart porte '01001a,01001b' : la route doit
    # rendre '01001a', la forme meme que le salon a envoyee a /set_choix_siege.
    # Sans le decoupage sur la virgule, la comparaison echouerait en silence et
    # l'invite attendrait pour toujours.
    verifier("partie en cours : le siege 0 rend l'identifiant de SA carte heros",
             bool(corps) and corps.get("heros") == ATTENDU[0], str(corps))

    code, corps = demander("/get_heros_du_siege?p=1")
    verifier("partie en cours : le siege 1 rend le SIEN, pas celui du voisin",
             bool(corps) and corps.get("heros") == ATTENDU[1], str(corps))
    repere_manche_1 = corps.get("debut") if corps else ""
    verifier("partie en cours : un repere de partie est annonce",
             bool(repere_manche_1), str(corps))

    # --- 3. Un siege que la partie n'a pas ----------------------------------
    # ⚠ LE CAS QUI EVITE UNE ATTENTE MUETTE : l'hote a envoye trois liens et
    # n'a lance qu'a deux. Le salon doit pouvoir le DIRE, donc la route doit
    # distinguer « pas de partie » de « partie sans ce siege ».
    code, corps = demander("/get_heros_du_siege?p=3")
    verifier("siege absent de la partie : la partie est quand meme annoncee en cours",
             bool(corps) and corps.get("en_jeu") is True, str(corps))
    verifier("siege absent de la partie : aucun heros",
             bool(corps) and corps.get("heros") == "", str(corps))

    # --- 4. ⚠ LA MANCHE REJOUEE AVEC LE MEME HEROS -------------------------
    # LE cas de la ronde de correction du 21/09. On rejoue la MEME equipe : le
    # heros du siege 0 ne bouge pas d'un caractere, et une regle qui ne
    # regarderait que lui prendrait la manche precedente pour la nouvelle (et
    # reciproquement). Seul `debut` distingue les deux.
    scene_2 = SceneLoader.NewFromJson(
        lire("Campaign", SCENARIO), None, [lire("Hero", h) for h in HEROS], 43, [], {})
    jeu.session.SetScene(scene_2, "Load")
    limite = time.time() + 60
    while (jeu.world is None or jeu.world.scene is not scene_2) and time.time() < limite:
        time.sleep(0.5)

    code, corps = demander("/get_heros_du_siege?p=0")
    verifier("manche 2 : le heros du siege est le MEME qu'a la manche 1",
             bool(corps) and corps.get("heros") == ATTENDU[0], str(corps))
    verifier("manche 2 : le repere, lui, a CHANGE",
             bool(corps) and corps.get("debut") and corps.get("debut") != repere_manche_1,
             f"manche 1 = {repere_manche_1} / manche 2 = {corps.get('debut') if corps else None}")

    repere_manche_2 = corps.get("debut") if corps else ""

    # --- 5. ⚠ MAIS UNE ANNULATION N'EST PAS UNE NOUVELLE PARTIE ------------
    # `AnnulerDernierGeste` repasse LA MEME scene a `SetScene`, comme le fait
    # `load_replay_data` d'un rejeu sur place. Et `/annuler_dernier_geste` est
    # ouverte a TOUT tenant de siege, pas au seul hote : si le repere bougeait
    # la, n'importe quel joueur de la manche precedente expedierait les invites
    # du salon dans sa partie — immediatement en campagne, ou aucun heros ne
    # vient les retenir.
    jeu.session.SetScene(scene_2, "Load")
    time.sleep(1)
    code, corps = demander("/get_heros_du_siege?p=0")
    verifier("meme scene reposee (annulation) : le repere NE bouge PAS",
             bool(corps) and corps.get("debut") == repere_manche_2,
             f"avant = {repere_manche_2} / apres = {corps.get('debut') if corps else None}")

    # --- 6. Une demande mal formee n'invente rien ---------------------------
    code, _ = demander("/get_heros_du_siege")
    verifier("siege non precise : refuse", code == 400, f"code={code}")
    code, _ = demander("/get_heros_du_siege?p=abc")
    verifier("siege illisible : refuse", code == 400, f"code={code}")
    code, _ = demander("/get_heros_du_siege?p=-1")
    verifier("siege negatif : refuse", code == 400, f"code={code}")

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
# os._exit() et jamais un retour normal : le fil du jeu est un daemon PARQUE
# dans `pilote`, et l'arret normal de Python resterait bloque a le joindre
# (lecon du 18/09/2026, tools/test_mode_manuel.py).
os._exit(0 if not rates else 1)
