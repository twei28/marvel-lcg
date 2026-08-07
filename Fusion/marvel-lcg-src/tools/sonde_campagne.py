"""Sonde : monte une partie, execute des commandes Puzzle, et rend le
DESCRIPTEUR DE MONDE tel que le plateau le recoit.

C'est ce descripteur que les detecteurs de recompenses vont lire : il faut donc
constater ce qu'il contient reellement (nom des compteurs, ou atterrissent les
cartes posees sous un complot, ou sont les allies secourus) plutot que de le
deduire du code du moteur.

Usage : python3.10 sonde_descripteur.py <racine> <scenario> <heros> [port]
  PUZZLE   : liste JSON de commandes Puzzle a executer apres la mise en place
  RAPPORT  : chemin du descripteur rendu (defaut /tmp/descripteur.json)
  FIN_DE_PARTIE : "1" pour declencher WhenGameOver apres la mise en place et
                  capturer le carnet SORTANT dans la cle `carnet_sortant`
"""
import json
import os
import sys

os.environ.setdefault("RELEASE", "1")

ROOT = os.path.abspath(sys.argv[1])
SCENARIO = sys.argv[2]
HERO = sys.argv[3]
PORT = int(sys.argv[4]) if len(sys.argv) > 4 else 4500
CAMPAIGN_LOG = json.loads(os.environ.get("CAMPAIGN_LOG", "{}"))
RULES = json.loads(os.environ.get("RULES", '["mode_campaign"]'))
PUZZLE = json.loads(os.environ.get("PUZZLE", "[]"))
RAPPORT = os.environ.get("RAPPORT", "/tmp/descripteur.json")
FIN_DE_PARTIE = os.environ.get("FIN_DE_PARTIE", "") == "1"

# Le moteur ecrit toujours dans le repertoire courant, soit .game. On efface
# le temoin AVANT la partie : sans cela on relirait le rapport de l'execution
# precedente et on croirait le scenario cable alors qu'il ne l'est pas.
CARNET_SORTANT = "campaign_log_last.json"

GAME = os.path.join(ROOT, ".game")
os.chdir(GAME)
sys.path.insert(0, GAME)

if FIN_DE_PARTIE and os.path.exists(CARNET_SORTANT):
    os.remove(CARNET_SORTANT)

try:
    import winsound  # noqa: F401
except ModuleNotFoundError:
    import types
    ws = types.ModuleType("winsound")
    for nom in ("Beep", "PlaySound", "MessageBeep"):
        setattr(ws, nom, lambda *a, **k: None)
    for nom in ("SND_FILENAME", "SND_ALIAS", "SND_LOOP", "SND_MEMORY", "SND_PURGE",
                "SND_ASYNC", "SND_NODEFAULT", "SND_NOSTOP", "SND_NOWAIT",
                "SND_APPLICATION", "MB_ICONASTERISK", "MB_ICONEXCLAMATION",
                "MB_ICONHAND", "MB_ICONQUESTION", "MB_OK"):
        setattr(ws, nom, 0)
    sys.modules["winsound"] = ws

cfg = json.load(open("launch.json"))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open("launch.json", "w"), indent=2)

from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True

from engine.device.manager.base import DeviceManager

etat = {"asks": 0}


def pilote(self, data, player_id, check):
    etat["asks"] += 1
    if etat["asks"] > 4000:
        raise SystemExit("trop de questions")
    try:
        options = json.loads(data.options_json or "[]")
    except Exception:
        options = []
    for o in options:
        if isinstance(o, dict) and not o.get("failure_reason"):
            legales = [str(x) for x in (o.get("all_legal_targets") or [])]
            mini = (o.get("target_num_range") or [0, 0])[0]
            return json.dumps({"id": str(o.get("id", 0)),
                               "targets": legales[:mini] if mini else [],
                               "resources": []})
    return json.dumps({"id": "0", "targets": [], "resources": []})


DeviceManager.DoGetInput = pilote
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None

from engine import Engine
Engine.Initialize()

from game.scene.loader import SceneLoader

campaign_json = open(os.path.join(GAME, "data", "scenarios", SCENARIO + ".json")).read()
chemin_deck = None
for base in ("deck/starter", "deck/custom"):
    p = os.path.join(GAME, base, HERO + ".json")
    if os.path.exists(p):
        chemin_deck = p
        break
assert chemin_deck, f"deck introuvable : {HERO}"

scene = SceneLoader.NewFromJson(campaign_json, None, [open(chemin_deck).read()],
                                42, RULES, CAMPAIGN_LOG)
jeu = Engine.game
jeu.session.SetScene(scene, "Load")

sortie = {"scenario": SCENARIO, "puzzle": PUZZLE, "erreurs": []}
try:
    jeu.GameSetup()
except BaseException as exc:
    sortie["erreurs"].append(f"setup : {type(exc).__name__}: {exc}")

# Commandes Puzzle : elles s'executent ici, en direct, pas dans une file.
if PUZZLE:
    try:
        from game.puzzle.puzzle import PuzzleHelper
        for commande in PUZZLE:
            try:
                PuzzleHelper.Exec([commande], Engine.game.world)
            except BaseException as exc:
                sortie["erreurs"].append(f"{commande} : {type(exc).__name__}: {exc}")
    except BaseException as exc:
        sortie["erreurs"].append(f"puzzle indisponible : {type(exc).__name__}: {exc}")

# Fin de partie : c'est le seul moment ou WriteCampaignLogAtGameOver s'execute.
# On passe par SetGameOverByRule, qui construit lui-meme l'Effect a partir de
# la manigance principale : rien a fabriquer a la main.
if FIN_DE_PARTIE:
    try:
        Engine.game.world.game_over.SetGameOverByRule(
            "The Final Stage of the Villain was Defeated"
        )
    except BaseException as exc:
        sortie["erreurs"].append(f"fin de partie : {type(exc).__name__}: {exc}")
    if os.path.exists(CARNET_SORTANT):
        try:
            with open(CARNET_SORTANT, encoding="utf-8") as f:
                sortie["carnet_sortant"] = json.load(f)
        except BaseException as exc:
            sortie["erreurs"].append(f"carnet sortant : {type(exc).__name__}: {exc}")
    else:
        sortie["carnet_sortant"] = None

try:
    from game.render.to_descriptor import ToDescriptor
    from engine.lib import Json
    descripteur = ToDescriptor.World(Engine.game.world, "sonde", "")
    sortie["monde"] = json.loads(Json.Dumps(descripteur))
except BaseException as exc:
    import traceback
    sortie["erreurs"].append(f"descripteur : {type(exc).__name__}: {exc}\n{traceback.format_exc()}")

with open(RAPPORT, "w", encoding="utf-8") as f:
    json.dump(sortie, f, ensure_ascii=False)
os._exit(0)
