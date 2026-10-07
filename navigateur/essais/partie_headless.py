"""Une partie complete, sans plateau, jouee par un pilote deterministe. MEME fichier pour le moteur normal
(Python 3.10) et pour Pyodide (3.12) : on compare ce qu'ils racontent. Entrees : variables HERO, VILLAIN,
SEED, MAX_ASKS, ENG_DIR (dossier du moteur), SANS_FILS=1 sous Pyodide (pas de fil d'execution)."""
import os, sys, json, random, time, traceback
ENG = os.environ.get("ENG_DIR", "/eng")
os.chdir(ENG); sys.path.insert(0, ENG)
os.environ["RELEASE"] = "1"
sys.argv = ["x", "-config_files", os.environ.get("CONFIG", "launch.json"), "-device", "key"]
HERO, VILLAIN = os.environ["HERO"], os.environ["VILLAIN"]
SEED = int(os.environ.get("SEED", "1")); MAX_ASKS = int(os.environ.get("MAX_ASKS", "700"))
# Generateur PRIVE du pilote : le moteur (ou une carte) peut reinitialiser le generateur global `random`,
# ce qui rendait les parties du pilote non reproductibles d'un lancement a l'autre (constate sur Conan).
RNG = random.Random(SEED)
T0 = time.time()
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
ST = {"asks": 0, "cartes": 0}
TRACE = os.environ.get("TRACE")
def pilote(self, data, player_id, check):
    ST["asks"] += 1
    if TRACE == "4" and ST["asks"] == 4:
        try:
            from engine import Engine as _E
            _w = _E.game.world
            _l = []
            for _k, _o in _w.object_manager.card_dict.items():
                _cid = str(getattr(getattr(getattr(_o, "face", None), "paper", None), "card_id", ""))
                if _cid.startswith("cn001"):
                    _l.append([_k, _cid])
            print("CRD " + json.dumps(_l), flush=True)
        except Exception as _e:
            print("CRD " + json.dumps({"erreur": repr(_e)}), flush=True)
    if TRACE == "3" and ST["asks"] == 4:
        print("CHG " + json.dumps(CHANGES), flush=True)
    if TRACE == "2" and ST["asks"] == 4:
        print("OBJ " + json.dumps(OBJLOG), flush=True)
    if TRACE:
        try:
            _o = json.loads(data.options_json or "[]")
        except Exception:
            _o = []
        if True:
            print("TR " + json.dumps({"n": ST["asks"], "prompt": str(getattr(data, "prompt_text", ""))[:60],
                                 "opts": [(o.get("id"), o.get("name"), o.get("bind_id"), o.get("all_legal_targets")) for o in _o if isinstance(o, dict) and not o.get("failure_reason")]}), flush=True)
    if ST["asks"] > MAX_ASKS:
        raise SystemExit("plafond")
    try: options = json.loads(data.options_json or "[]")
    except Exception: options = []
    libres = [o for o in options if isinstance(o, dict) and not o.get("failure_reason")]
    if not libres or RNG.random() < 0.25:
        return json.dumps({"id": "0", "targets": [], "resources": []})
    o = RNG.choice(libres)
    tmin = (o.get("target_num_range") or [0, 0])[0]
    legales = list(dict.fromkeys(o.get("all_legal_targets") or []))
    cibles = RNG.sample(legales, min(len(legales), max(tmin, 0))) if tmin > 0 else []
    if o.get("name") == "Play": ST["cartes"] += 1
    return json.dumps({"id": str(o.get("id", 0)), "targets": cibles, "resources": []})
DeviceManager.DoGetInput = pilote
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None
OBJLOG = []
CARDS4 = []
if os.environ.get("TRACE") == "4":
    import traceback as _tb4
    from game.object.manager import ObjectManager
    _add4 = ObjectManager.AddObject
    def _wrap4(self, category, obj):
        r = _add4(self, category, obj)
        try:
            if str(category) == "card":
                rep = repr(getattr(obj, "face", None) or obj)[:60] + "|" + str(getattr(getattr(obj, "paper", None), "card_id", ""))
                if "cn001" in rep:
                    pile = [f"{os.path.basename(f.filename)}:{f.name}:{f.lineno}" for f in _tb4.extract_stack(limit=10)[:-1]]
                    CARDS4.append({"id": r, "carte": rep, "pile": pile[-6:]})
        except Exception:
            pass
        return r
    ObjectManager.AddObject = _wrap4
CHANGES = []
if os.environ.get("TRACE") == "3":
    import traceback as _tb
    from game.object.manager import ObjectManager
    _add3 = ObjectManager.AddObject
    def _wrap3(self, category, obj):
        r = _add3(self, category, obj)
        try:
            nom = str(getattr(getattr(obj, "ability", None), "name", "") or "")
            if "Change" in nom:
                pile = [f"{os.path.basename(f.filename)}:{f.name}:{f.lineno}" for f in _tb.extract_stack(limit=9)[:-1]]
                CHANGES.append({"id": r, "cat": str(category), "nom": nom, "this": repr(getattr(obj, "this", None))[:40], "pile": pile[-6:]})
        except Exception:
            pass
        return r
    ObjectManager.AddObject = _wrap3
if os.environ.get("TRACE") == "2":
    from game.object.manager import ObjectManager
    _add = ObjectManager.AddObject
    def _wrap(self, category, obj):
        r = _add(self, category, obj)
        _d = ""
        if str(category) == "forced_effect":
            try:
                _d = repr(getattr(obj, "this", None))[:70] + " | " + str(getattr(getattr(obj, "ability", None), "name", getattr(obj, "name", "")))[:50]
            except Exception as _e:
                _d = "?" + type(_e).__name__
        OBJLOG.append((str(category), type(obj).__name__, r, _d))
        return r
    ObjectManager.AddObject = _wrap
res = {"hero": HERO, "villain": VILLAIN, "seed": SEED}
try:
    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    from engine.file.manager import FileManager
    chemin = FileManager.FindJsonPath("Hero", HERO); assert chemin, "deck introuvable"
    with FileManager.OpenFile(chemin, read=True) as f: texte_deck = f.Read()
    chemin_v = FileManager.FindJsonPath("Campaign", VILLAIN); assert chemin_v, "scenario introuvable"
    with FileManager.OpenFile(chemin_v, read=True) as f: campagne = json.loads(f.Read())
    scene = SceneLoader.NewFromJson(json.dumps(campagne), None, [texte_deck], SEED, [], {})
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    ok = jeu.GameSetup(); res["setup"] = bool(ok)
    try: jeu.GameLoop()
    except SystemExit as e: res["arret"] = str(e)
    w = Engine.game.world
    go = getattr(w, "game_over", None)
    res.update(asks=ST["asks"], cartes=ST["cartes"], round=getattr(w, "round_id", None),
               won=str(getattr(go, "players_won", None)), reason=str(getattr(go, "reason", "") or ""))
    from game.card.face.base.villain import Villain
    for obj in w.object_manager.card_dict.values():
        face = getattr(obj, "face", None)
        if face is not None and isinstance(face, Villain) and hasattr(face, "IsInPlay") and face.IsInPlay():
            res["vilain_pv"] = getattr(face, "health", None); break
except SystemExit as e:
    res.update(asks=ST["asks"], erreur="SystemExit " + str(e))
except BaseException:
    res.update(asks=ST["asks"], erreur=traceback.format_exc()[-300:])
res["secondes"] = round(time.time() - T0, 1)
print("RESULTAT " + json.dumps(res, sort_keys=True), flush=True)
