"""Un PUZZLE monte puis CAPTURE, sans plateau. MEME fichier pour le moteur normal (Python 3.10) et pour Pyodide (3.12) :
on compare ce qu'ils racontent (controle d'equivalence des puzzles, E10). Entrees : PUZZLE_JSON (le puzzle, PuzzleData en JSON),
ENG_DIR, SANS_FILS=1 sous Pyodide. Le pilote capture l'etat a la PREMIERE question du moteur, puis arrete."""
import os, sys, json, traceback
ENG = os.environ.get("ENG_DIR", "/eng")
os.chdir(ENG); sys.path.insert(0, ENG)
os.environ["RELEASE"] = "1"
sys.argv = ["x", "-config_files", os.environ.get("CONFIG", "launch.json"), "-device", "key"]
if os.environ.get("SANS_FILS") == "1":
    import concurrent.futures as cf
    class Immediat(cf.Executor):
        def submit(self, fn, *a, **k):
            f = cf.Future()
            try: f.set_result(fn(*a, **k))
            except BaseException as e: f.set_exception(e)
            return f
        def shutdown(self, wait=True, *, cancel_futures=False): pass
    import engine.job.manager as _jm
    _jm.ThreadPoolExecutor = lambda max_workers=None: Immediat()
from engine.device.manager.base import DeviceManager
RES = {}
def pilote(self, data, player_id, check):
    from engine import Engine
    from game.puzzle.puzzle_capture import CapturePuzzle
    from game.operate.worlds import Worlds
    monde = Engine.game.world
    RES["capture"] = CapturePuzzle(monde)
    villains = Worlds.GetAllVillains(monde)
    RES["villain_pv"] = villains[0].health if villains else None
    RES["round"] = monde.round_id
    RES["phase"] = str(monde.phase.state)
    RES["objectifs"] = monde.puzzle_objectives.Status()
    raise SystemExit("capture")
DeviceManager.DoGetInput = pilote
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None
try:
    from engine import Engine
    Engine.Initialize()
    from engine.lib.json import Json
    from game.scene.scene import Scene
    from game.puzzle.puzzle_data import PuzzleData
    from game.puzzle.puzzle_scene import BuildPuzzleScene
    from game.puzzle.puzzle_validation import PUBLISHED_METHODS, validate_puzzle
    puzzle = Json.LoadsAs(os.environ["PUZZLE_JSON"], PuzzleData)
    RES["erreurs_validation"] = validate_puzzle(puzzle, PUBLISHED_METHODS)
    scene = Json.LoadsAs(Json.Dumps(BuildPuzzleScene(puzzle)), Scene)
    scene.UpdateVersion()
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    if jeu.GameSetup():
        try: jeu.GameLoop()
        except SystemExit as e: RES["arret"] = str(e)
    if "capture" not in RES:
        RES["erreur"] = "le moteur n'a jamais pose de question"
except SystemExit as e:
    RES["arret"] = str(e)
except BaseException:
    RES["erreur"] = traceback.format_exc()[-400:]
print("RESULTAT " + json.dumps(RES, sort_keys=True, ensure_ascii=False), flush=True)
