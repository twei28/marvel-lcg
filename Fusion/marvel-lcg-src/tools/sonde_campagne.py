"""Sonde : monte une partie, execute des commandes Puzzle, et rend le
DESCRIPTEUR DE MONDE tel que le plateau le recoit.

C'est ce descripteur que les detecteurs de recompenses vont lire : il faut donc
constater ce qu'il contient reellement (nom des compteurs, ou atterrissent les
cartes posees sous un complot, ou sont les allies secourus) plutot que de le
deduire du code du moteur.

Usage : python3.10 sonde_descripteur.py <racine> <scenario> <heros> [port]
  <heros> accepte PLUSIEURS noms separes par des virgules : certaines regles ne
  se mesurent qu'a plusieurs joueurs (« any player's deck », « each player »).
  PUZZLE   : liste JSON de commandes Puzzle a executer apres la mise en place
  RAPPORT  : chemin du descripteur rendu (defaut /tmp/descripteur.json)
  FIN_DE_PARTIE : "1" pour declencher WhenGameOver apres la mise en place et
                  capturer le carnet SORTANT dans la cle `carnet_sortant`
  CHOIX    : index de l'option retenue a CHAQUE question, dans la liste des
             options legales (defaut 0, la premiere). Les index negatifs
             comptent depuis la fin, comme en Python : -1 prend la derniere.
             Sert a prouver qu'une question offre VRAIMENT plusieurs reponses —
             avec le seul premier choix, un menu a une branche et un menu a
             quatre se mesurent pareil.
"""
import json
import os
import sys

os.environ.setdefault("RELEASE", "1")

ROOT = os.path.abspath(sys.argv[1])
SCENARIO = sys.argv[2]
HEROS = [x for x in sys.argv[3].split(',') if x]
PORT = int(sys.argv[4]) if len(sys.argv) > 4 else 4500
CAMPAIGN_LOG = json.loads(os.environ.get("CAMPAIGN_LOG", "{}"))
RULES = json.loads(os.environ.get("RULES", '["mode_campaign"]'))
PUZZLE = json.loads(os.environ.get("PUZZLE", "[]"))
RAPPORT = os.environ.get("RAPPORT", "/tmp/descripteur.json")
CHOIX = int(os.environ.get("CHOIX", "0"))
FIN_DE_PARTIE = os.environ.get("FIN_DE_PARTIE", "") == "1"

GAME = os.path.join(ROOT, ".game")
os.chdir(GAME)
sys.path.insert(0, GAME)

# Le carnet sortant est CLOISONNE PAR PLACE depuis le commit 89a1193 : son nom
# vient de la cle de configuration `campaign_log_last_file`, comme
# `campagne_folder` et `achievements_file`. Le lire en dur marchait tant qu'on
# sondait la configuration par defaut, ou les deux chemins coincident ; sur une
# configuration de place (place 2, 3 ou 4 d'un serveur multi), la sonde
# effacait puis relisait le fichier d'une AUTRE place, et rendait un faux
# positif ou un faux negatif selon ce que la partie precedente y avait laisse.
#
# On lit la meme source que le moteur : le launch.json du dossier de jeu, que
# `launcher_fast.py` y recopie a chaque lancement.
def _carnet_sortant():
    try:
        with open(os.path.join(GAME, "launch.json"), encoding="utf-8") as f:
            return json.load(f).get("campaign_log_last_file") or "campaign_log_last.json"
    except Exception:
        return "campaign_log_last.json"


CARNET_SORTANT = _carnet_sortant()

# On efface le temoin AVANT la partie : sans cela on relirait le rapport de
# l'execution precedente et on croirait le scenario cable alors qu'il ne l'est
# pas.

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
    legales_options = [o for o in options
                       if isinstance(o, dict) and not o.get("failure_reason")]
    if legales_options:
        try:
            o = legales_options[CHOIX]
        except IndexError:
            # Moins d'options que demande : on retombe sur la premiere plutot
            # que de planter, sinon une seule question courte ferait echouer
            # toute une mesure.
            o = legales_options[0]
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
decks = []
for heros in HEROS:
    chemin_deck = None
    for base in ("deck/starter", "deck/custom"):
        p = os.path.join(GAME, base, heros + ".json")
        if os.path.exists(p):
            chemin_deck = p
            break
    assert chemin_deck, f"deck introuvable : {heros}"
    decks.append(open(chemin_deck).read())

scene = SceneLoader.NewFromJson(campaign_json, None, decks,
                                42, RULES, CAMPAIGN_LOG)
jeu = Engine.game
jeu.session.SetScene(scene, "Load")

sortie = {"scenario": SCENARIO, "heros": HEROS, "puzzle": PUZZLE, "erreurs": []}
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
