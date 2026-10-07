"""Adaptateur : le VRAI moteur et ses VRAIES routes, sans fil ni socket, dans un Worker.

Le moteur attend le fil HTTP dans `Condition.Wait` : ici, ces attentes TRAITENT le courrier de la page
(requetes fetch, WebSocket) puis re-testent leur condition. Aucune ligne du moteur n'est modifiee.
"""
import os, sys, json, time, gzip, base64, traceback, asyncio
from js import pomper, envoyer, journal
os.chdir("/eng"); sys.path.insert(0, "/eng")
os.environ["RELEASE"] = "1"
sys.argv = ["x", "-config_files", "launch.json", "-device", "web"]
T0 = time.time()
def jr(m): journal(f"[{time.time()-T0:5.1f}s] {m}")

def run_sync(coro):
    """Execute une coroutine qui ne se suspend jamais vraiment (aucun fil, aucune boucle)."""
    try:
        while True:
            coro.send(None)
    except StopIteration as e:
        return e.value

STATS = {"req": 0, "frames": 0, "erreurs": {}}
PERSIST = "/eng/persist"
SYNC = {"t": 0.0, "vu": {}}

def scanner():
    out = {}
    for dp, dn, fn in os.walk(PERSIST):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                st = os.stat(p)
                out[p] = (st.st_mtime_ns, st.st_size)
            except OSError:
                pass
    return out

def sync_persist(force=False):
    """Ce que le moteur ecrit dans /persist part vers la page, qui le garde dans IndexedDB.
    (IDBFS est inutilisable ici : le Worker est presque toujours bloque, sa boucle d'evenements ne tourne pas.)"""
    now = time.time()
    if not force and now - SYNC["t"] < 1.5:
        return
    SYNC["t"] = now
    cur = scanner()
    for p, v in cur.items():
        if SYNC["vu"].get(p) != v:
            with open(p, "rb") as f:
                envoyer("persist", json.dumps({"path": p, "b64": base64.b64encode(f.read()).decode()}))
    for p in list(SYNC["vu"]):
        if p not in cur:
            envoyer("persist", json.dumps({"path": p, "del": True}))
    SYNC["vu"] = cur
SERVER = {}
CLIENTS = []

# ------------------------------------------------------------------ courrier
def pump(timeout_s):
    for brut in json.loads(pomper(int(max(0.0, timeout_s) * 1000))):
        try:
            traiter(json.loads(brut))
        except Exception:
            STATS["erreurs"]["traiter"] = STATS["erreurs"].get("traiter", 0) + 1
            jr("ERREUR traiter: " + traceback.format_exc()[-600:])

def repondre(id_, status, ctype, corps):
    envoyer("rep", json.dumps({"id": id_, "status": status, "ctype": ctype,
                               "b64": base64.b64encode(corps).decode()}))

def traiter(m):
    t = m["type"]
    if t == "req":
        STATS["req"] += 1
        servir(m)
    elif t == "ws_open":
        ouvrir_ws(m["url"])
    elif t == "ws_msg":
        if m["text"].startswith("Connected") and CLIENTS:
            from engine import Engine
            ids = CLIENTS[-1].player_ids
            if ids:
                SERVER["srv"].WebSendRender(ids[0], "websocket_handler")
            Engine.device_manager.notify.connect.NotifyAll()
    elif t == "fichier":                 # import d'une sauvegarde par le joueur (voir navigateur.html)
        p = os.path.normpath(m["path"])
        if p.startswith(PERSIST + "/") and p.endswith(".json"):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(base64.b64decode(m["b64"]))
    elif t == "sync":                    # export : tout ce que le moteur a ecrit doit etre chez la page
        sync_persist(force=True)
    elif t == "ws_close":
        CLIENTS.clear()
        from engine import Engine
        Engine.device_manager.client_manager.connected_clients.clear()

class FauxWS:
    closed = False
    async def send_json(self, d):
        STATS["frames"] += 1
        envoyer("frame", json.dumps(d))

def ouvrir_ws(url):
    from engine import Engine
    from urllib.parse import urlparse, parse_qs
    q = parse_qs(urlparse(url).query, keep_blank_values=True)
    dm = Engine.device_manager
    if "hot_seat" in q:
        ids = list(range(Engine.game.controller_manager.total_players))
    else:
        p = (q.get("p") or ["0"])[0]
        ids = [int(x) for x in p.split(",")] if p else [0]
    dm.client_manager.Add(FauxWS(), ids, urlparse(url).query)
    CLIENTS.append(dm.client_manager.connected_clients[-1])
    jr(f"plateau connecte (sieges {ids})")

def faire_requete(method, chemin, corps, app):
    """Fausse requete aiohttp 3.9 (le paquet Pyodide n'embarque pas aiohttp.test_utils)."""
    from unittest import mock
    from aiohttp import web
    from aiohttp.http import HttpVersion, RawRequestMessage
    from aiohttp.streams import StreamReader, EMPTY_PAYLOAD
    from aiohttp.base_protocol import BaseProtocol
    from yarl import URL
    from multidict import CIMultiDict, CIMultiDictProxy
    loop = SERVER["loop"]
    hd = CIMultiDictProxy(CIMultiDict({"Host": "localhost"}))
    raw = tuple((k.encode(), v.encode()) for k, v in hd.items())
    message = RawRequestMessage(method, chemin, HttpVersion(1, 1), hd, raw, False, None, False, False, URL(chemin))
    transport = mock.Mock()
    transport.get_extra_info.side_effect = lambda k, d=None: ("127.0.0.1", 80) if k in ("peername", "sockname") else d
    protocol = mock.Mock(); protocol.transport = transport
    if corps:
        payload = StreamReader(BaseProtocol(loop), 2 ** 20, loop=loop)
        payload.feed_data(corps.encode("utf-8")); payload.feed_eof()
    else:
        payload = EMPTY_PAYLOAD
    return web.Request(message, payload, protocol, mock.Mock(), mock.Mock(), loop, client_max_size=8 * 1024 ** 2)

def servir(m):
    srv = SERVER["srv"]; id_ = m["id"]
    chemin = m["path"] + (("?" + m["query"]) if m["query"] else "")
    req = faire_requete(m["method"], chemin, m["body"] if m["method"] == "POST" else "", srv.web_app)
    try:
        match = run_sync(srv.web_app.router.resolve(req))
        if match.http_exception is not None:
            repondre(id_, match.http_exception.status, "text/plain", b"")
            jr(f"404 {m['method']} {m['path']}")
            return
        req._match_info = match
        resp = run_sync(match.handler(req))
    except Exception:
        jr(f"ERREUR route {m['method']} {m['path']}: " + traceback.format_exc()[-500:])
        repondre(id_, 500, "text/plain", b"")
        return
    corps = getattr(resp, "body", None)
    if corps is None and hasattr(resp, "_path"):
        corps = open(resp._path, "rb").read()
    if isinstance(corps, str):
        corps = corps.encode("utf-8")
    corps = corps or b""
    if resp.headers.get("Content-Encoding") == "gzip":
        corps = gzip.decompress(corps)
    repondre(id_, resp.status, resp.content_type, corps)
    sync_persist()

# ------------------------------------------------- remplacements (hors moteur)
import engine.task.condition as _cond
def _wait(self, check, timeout=None):
    """Comme `Condition.wait_for` : le predicat est teste d'abord, puis SEULEMENT apres une notification
    (ack de trame, reponse, connexion, sortie d'attente), jamais a chaque message recu."""
    fin = None if timeout is None else time.time() + timeout
    if check():
        return True
    while True:
        reste = 1.0 if fin is None else fin - time.time()
        if reste <= 0:
            return check()
        self._reveil = False
        pump(min(reste, 1.0))
        sync_persist()
        if getattr(self, "_reveil", False) and check():
            return True
def _notify(self):
    self._reveil = True
_cond.Condition.Wait = _wait
_cond.Condition.NotifyAll = _notify

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

from engine.task import TaskManager
def _run_await(process, objects, wait_finished=True):
    for o in objects:
        run_sync(process(o))
TaskManager.RunAwaitProcesses = staticmethod(_run_await)
async def _to_thread(process, *a, **k):
    return process(*a, **k)
TaskManager.ToThread = staticmethod(_to_thread)

import engine.device.manager.web.manager as _wm
from engine.device.manager.base import DeviceManager
from engine.device.manager.web.client import ClientManager
def _init_web(self):
    from engine.device.web.server.server import GameServer
    DeviceManager.__init__(self)
    self.client_manager = ClientManager()
    srv = GameServer(self)            # les vraies routes ; Run() n'est JAMAIS appele : aucun port
    self.httpds = [srv]
    self.stat_sent_size = {}
    SERVER["srv"] = srv
    SERVER["loop"] = asyncio.new_event_loop()
_wm.WebDeviceManager.__init__ = _init_web

# ------------------------------------------------------------------ partie
from engine import Engine
Engine.Initialize(); jr("moteur initialise (device web, sans socket)")
SYNC["vu"] = scanner()           # l'etat restaure par la page n'est pas a renvoyer
envoyer("pret", "")
# La VRAIE boucle du moteur : attend une partie (/new), la joue, recommence. Les attentes sont les notres.
Engine.EngineRun()
jr(f"FIN requetes={STATS['req']} trames={STATS['frames']}")
