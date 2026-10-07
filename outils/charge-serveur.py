#!/usr/bin/env python3
"""Banc de charge : N tables, chacune jouee EN VRAI par un bot via WebSocket.

A lancer SUR LE SERVEUR, en tant que `narwhal` (jamais root : les fichiers du
jeu passeraient a root et bloqueraient toutes les tables) :

    sudo -u narwhal /opt/narwhal/venv310/bin/python charge_serveur.py \
        --tables 100 --palier 10 --palier-s 90 --tenue-s 300

Places 101 et suivantes (ports 2451+) : jamais des places de comptes (1..30).
Le bot fait ce que fait le navigateur : WebSocket /ws, lecture du monde
(/get_partie_en_cours), de la question (/get_ask), accuse (/client_updated),
reponse (POST /post). Il joue vraiment : options au hasard, cibles legales,
paiement par les ressources proposees, repli sur « passer ».
"""
import argparse, asyncio, json, os, random, shutil, signal, subprocess, sys, time, statistics, urllib.request
from collections import defaultdict

RACINE = os.environ.get("RACINE_JEU", "/opt/narwhal/Fusion/marvel-lcg-src")
PYTHON = "/opt/narwhal/venv310/bin/python"
PORT_BASE = 2350
PLACE_DEPART = int(os.environ.get("PLACE_DEPART", "101"))
sys.path.insert(0, os.path.join(RACINE, "tools"))
import config_serveur  # noqa: E402
config_serveur.PLACES_MAX = 400

LAT = defaultdict(list)       # endpoint -> [(t, ms)]
ERR = defaultdict(int)
ACTIONS = [0]
VIDES = [0]
PARTIES = [0]
FINIES = [0]
DERNIER_MONDE = {}
REGLES = ["v16_all", "no_crisis_of_infinite_deadpools", "no_encounter_cards_ignore_crisis"]
COMBOS = [("rhino","spider_man"),("klaw","captain_marvel"),("rhino","she_hulk"),("klaw","iron_man"),("rhino","black_panther")]


def lire_meminfo():
    m = {}
    for l in open("/proc/meminfo"):
        k, v = l.split(":")
        m[k] = int(v.split()[0]) // 1024
    return m


def pss_mo(pid):
    try:
        for l in open(f"/proc/{pid}/smaps_rollup"):
            if l.startswith("Pss:"):
                return int(l.split()[1]) / 1024
    except OSError:
        pass
    return 0.0


def rss_mo(pid):
    try:
        for l in open(f"/proc/{pid}/status"):
            if l.startswith("VmRSS:"):
                return int(l.split()[1]) / 1024
    except OSError:
        pass
    return 0.0


class Table:
    def __init__(self, place):
        self.place = place
        self.port = PORT_BASE + place
        self.proc = None
        self.base = f"http://127.0.0.1:{self.port}"
        self.cfg = os.path.join(RACINE, ".site", f"launch-{place}.json")
        self.journal = f"/tmp/charge-{place}.log"
        self.tache = None
        self.reponses = 0
        self.parties = 0
        self.mort = False

    def demarrer(self):
        base = json.load(open(os.path.join(RACINE, "launch.json"), encoding="utf-8"))
        cfg = config_serveur.construire_config(base, self.place)
        for rel in cfg["replay_folders"] + [cfg["deck_folders"][0], cfg["campagne_folder"]]:
            os.makedirs(os.path.normpath(os.path.join(RACINE, ".game", rel)), exist_ok=True)
        os.makedirs(os.path.dirname(self.cfg), exist_ok=True)
        json.dump(cfg, open(self.cfg, "w", encoding="utf-8"), ensure_ascii=False)
        j = open(self.journal, "w")
        self.proc = subprocess.Popen(
            [PYTHON, "-u", "launcher_fast.py", "--config", self.cfg, "--no-browser"],
            cwd=RACINE, stdout=j, stderr=subprocess.STDOUT, env={**os.environ, "PYTHONUNBUFFERED": "1"})
        try:  # le tueur de memoire vise NOS tables d'abord, jamais le site
            open(f"/proc/{self.proc.pid}/oom_score_adj", "w").write("1000")
        except OSError:
            pass

    def nettoyer(self):
        for rel in (f"../replays/serveur-{self.place}/", f"../campagnes-serveur-{self.place}/",
                    f"./deck/serveur-{self.place}/"):
            shutil.rmtree(os.path.normpath(os.path.join(RACINE, ".game", rel)), ignore_errors=True)
        for rel in (f"../games_history-serveur-{self.place}.json", f"../statistics-serveur-{self.place}.json",
                    f"../achievements-serveur-{self.place}.json", f"../legacy-serveur-{self.place}.json",
                    f"../arts-heros-serveur-{self.place}.json", f"./campaign-log-last-serveur-{self.place}.json"):
            try:
                os.remove(os.path.normpath(os.path.join(RACINE, ".game", rel)))
            except OSError:
                pass
        for f in ((self.cfg,) if self.mort else (self.cfg, self.journal)):
            try:
                os.remove(f)
            except OSError:
                pass


async def appel(session, methode, url, ep, **kw):
    t = time.perf_counter()
    try:
        async with session.request(methode, url, **kw) as r:
            corps = await r.text()
            ok = r.status < 400
    except Exception:
        ERR[ep] += 1
        return None
    LAT[ep].append((time.time(), (time.perf_counter() - t) * 1000))
    if not ok:
        ERR[ep] += 1
        return None
    return corps


def choisir(demande, serie):
    """La reponse du bot a une question du moteur. `serie` : coups deja joues ce tour."""
    options = demande.get("options") or demande.get("options_json") or []
    if isinstance(options, str):
        try:
            options = json.loads(options)
        except ValueError:
            options = []
    jouables = [o for o in options if isinstance(o, dict) and not o.get("failure_reason")]
    # Un humain joue quelques coups puis termine son tour : {} = passer.
    if not jouables or random.random() < min(0.8, 0.12 + 0.12 * serie):
        return {}
    o = random.choice(jouables)
    tmin = (o.get("target_num_range") or [0, 0])[0]
    legales = list(dict.fromkeys(o.get("all_legal_targets") or []))
    cibles = random.sample(legales, min(len(legales), max(tmin, 0))) if tmin > 0 else []
    paiements = o.get("target_payment") or {}
    p = paiements.get(str(cibles[0])) if cibles and str(cibles[0]) in paiements else paiements.get("0")
    ressources = []
    if p:
        try:
            n = int(p.get("cost") or 0)
        except ValueError:
            n = 0
        total = 0
        for m in p.get("payment") or []:
            if total >= n:
                break
            if not isinstance(m, dict):
                continue
            if "effect_id" in m:
                e, txt = m["effect_id"], str(m.get("res_text", "X"))
            elif len(m) == 1:
                k, v = next(iter(m.items()))
                e, txt = int(k), str(v)
            else:
                continue
            ressources.append(e)
            total += len(txt)
    return {"id": o["id"], "targets": cibles, "resources": ressources}


async def nouvelle_partie(s, t):
    scen, hero = COMBOS[(t.place + t.parties) % len(COMBOS)]
    t.parties += 1
    sj = json.loads(await appel(s, "GET", f"{t.base}/get_scenario_json?{scen}", "init") or "{}")
    hj = json.loads(await appel(s, "GET", f"{t.base}/get_hero_json?{hero}", "init") or "{}")
    charge = {"campaign_json": json.dumps(sj), "campaign_log": {}, "challenges": sj.get("challenges", []),
              "encounter_set_names": sorted(set(sj.get("encounter_sets", [])) | set(sj.get("modular_sets", []))),
              "hero_json": [json.dumps(hj)], "rules": REGLES, "seed": random.randint(1, 10**6), "timeout": 0}
    PARTIES[0] += 1
    return await appel(s, "GET", t.base + "/new?data=" + urllib.request.quote(json.dumps(charge)), "new") is not None


async def bot(table, args, charge):
    import aiohttp
    t = table
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as s:
        # attendre le moteur
        for _ in range(240):
            if await appel(s, "GET", t.base + "/get_max_timeout", "attente") is not None:
                break
            await asyncio.sleep(1)
        else:
            t.mort = True
            return
        if not await nouvelle_partie(s, t):
            t.mort = True
            return
        serie = 0
        while True:
            try:
                async with s.ws_connect(t.base + "/ws?hot_seat&p=0", heartbeat=None) as ws:
                    await ws.send_str("Connected http://127.0.0.1/")
                    async for msg in ws:
                        try:
                            trame = json.loads(msg.data)
                        except ValueError:
                            continue
                        rid, gid = trame.get("render_id"), trame.get("game_id")
                        await appel(s, "GET", t.base + "/get_world?hot_seat&p=0", "monde")   # LA route du plateau (monde complet, gzip)
                        # Fiche de suivi (petite) : sert UNIQUEMENT a detecter la fin de partie.
                        mtxt = await appel(s, "GET", t.base + "/get_partie_en_cours?p=0", "suivi")
                        if mtxt and t.place == PLACE_DEPART:
                            DERNIER_MONDE["m"] = mtxt
                        if mtxt and '"en_cours": false' in mtxt.replace('"en_cours":false', '"en_cours": false'):
                            FINIES[0] += 1
                            await asyncio.sleep(random.uniform(4, 12))
                            if not await nouvelle_partie(s, t):
                                t.mort = True
                                return
                            serie = 0
                            break
                        asks = trame.get("ask_players") or []
                        demande = None
                        if asks:
                            c = await appel(s, "GET", f"{t.base}/get_ask?p={asks[0]}", "ask")
                            if c and c.strip():
                                if t.place == PLACE_DEPART and ACTIONS[0] in (3, 12, 25):
                                    open(f"/tmp/charge-ask-{ACTIONS[0]}.json", "w").write(c[:6000])
                                try:
                                    demande = json.loads(c)
                                except ValueError:
                                    demande = None
                        await appel(s, "GET", f"{t.base}/client_updated?hot_seat&p=0&r={rid}&g={gid}", "accuse")
                        if demande is not None and asks:
                            await asyncio.sleep(random.uniform(args.pense_min, args.pense_max))
                            rep = choisir(demande, serie)
                            serie = 0 if not rep else serie + 1
                            await appel(s, "POST", f"{t.base}/post?p={asks[0]}", "post",
                                        data=json.dumps(rep),
                                        headers={"Content-type": "application/x-www-form-urlencoded"})
                            ACTIONS[0] += 1
                            if not rep:
                                VIDES[0] += 1
                            if t.place == PLACE_DEPART and ACTIONS[0] % 5 == 0:
                                open("/tmp/charge-echantillon.txt", "a").write(
                                    json.dumps({"opts": [o.get("name") for o in (demande.get("options") or [])][:8],
                                                "prompt": demande.get("prompt_text"), "rep": rep})[:600] + "\n")
                            t.reponses += 1
            except asyncio.CancelledError:
                raise
            except Exception:
                ERR["ws"] += 1
            await asyncio.sleep(2)


def pcts(valeurs):
    if not valeurs:
        return (0, 0, 0, 0)
    v = sorted(valeurs)
    return (len(v), statistics.median(v), v[int(len(v) * 0.95) - 1 if len(v) > 1 else 0], v[-1])


def instantane(tables, t0, niveau):
    m = lire_meminfo()
    vivantes = [x for x in tables if x.proc and x.proc.poll() is None and not x.mort]
    maintenant = time.time()
    fenetre = lambda ep: [ms for (ts, ms) in LAT[ep] if ts > maintenant - 30]
    ligne = {
        "t": round(maintenant - t0), "tables": len(vivantes), "niveau": niveau,
        "charge1": os.getloadavg()[0], "dispo_mo": m["MemAvailable"], "swap_utilise_mo": m["SwapTotal"] - m["SwapFree"],
        "pss_tables_mo": round(sum(pss_mo(x.proc.pid) for x in vivantes)),
        "rss_tables_mo": round(sum(rss_mo(x.proc.pid) for x in vivantes)),
        "actions": ACTIONS[0], "passes": VIDES[0], "parties": PARTIES[0], "finies": FINIES[0], "erreurs": dict(ERR),
    }
    for ep in ("post", "ask", "monde", "accuse"):
        n, med, p95, mx = pcts(fenetre(ep))
        ligne[ep] = {"n": n, "med": round(med, 1), "p95": round(p95, 1)}
    return ligne


def ping_site():
    t = time.perf_counter()
    try:
        urllib.request.urlopen("http://127.0.0.1:8080/", timeout=10).read(100)
    except Exception:
        return 10000.0
    return (time.perf_counter() - t) * 1000


async def principal(args):
    tables = []
    taches = []
    t0 = time.time()
    sortie = open(args.sortie, "w")
    charge = None
    abandon = None
    try:
        niveau = 0
        while niveau < args.tables and abandon is None:
            niveau = min(args.tables, niveau + args.palier)
            while len(tables) < niveau:
                t = Table(PLACE_DEPART + len(tables))
                t.demarrer()
                tables.append(t)
                taches.append(asyncio.create_task(bot(t, args, charge)))
                await asyncio.sleep(args.decalage_s)
            fin = time.time() + args.palier_s
            while time.time() < fin and abandon is None:
                await asyncio.sleep(5)
                l = instantane(tables, t0, niveau)
                l["site_ms"] = round(ping_site())
                print(json.dumps(l), file=sortie, flush=True)
                print(f"[{l['t']:>5}s] tables={l['tables']:>3} dispo={l['dispo_mo']:>5}Mo swap={l['swap_utilise_mo']:>5}Mo "
                      f"pss={l['pss_tables_mo']:>5}Mo charge={l['charge1']:.1f} site={l['site_ms']}ms "
                      f"post p95={l['post']['p95']}ms monde p95={l['monde']['p95']}ms parties={l['parties']} act={l['actions']} err={sum(ERR.values())}",
                      flush=True)
                if l["dispo_mo"] + (4095 - l["swap_utilise_mo"]) < args.plancher_mo:
                    abandon = f"memoire + swap libre sous {args.plancher_mo} Mo"
                elif l["site_ms"] > args.site_max_ms:
                    abandon = f"le site repond en {l['site_ms']} ms (> {args.site_max_ms})"
        if abandon:
            print("ABANDON :", abandon, flush=True)
        else:
            print(f"Palier final {niveau} tables atteint, tenue {args.tenue_s}s", flush=True)
            fin = time.time() + args.tenue_s
            while time.time() < fin and abandon is None:
                await asyncio.sleep(5)
                l = instantane(tables, t0, niveau)
                l["site_ms"] = round(ping_site())
                print(json.dumps(l), file=sortie, flush=True)
                print(f"[{l['t']:>5}s] tables={l['tables']:>3} dispo={l['dispo_mo']:>5}Mo swap={l['swap_utilise_mo']:>5}Mo "
                      f"charge={l['charge1']:.1f} site={l['site_ms']}ms post p95={l['post']['p95']}ms act={l['actions']}", flush=True)
                if l["dispo_mo"] + (4095 - l["swap_utilise_mo"]) < args.plancher_mo or l["site_ms"] > args.site_max_ms:
                    abandon = "garde-fou pendant la tenue"
    finally:
        for tk in taches:
            tk.cancel()
        for t in tables:
            if t.proc and t.proc.poll() is None:
                t.proc.terminate()
        await asyncio.sleep(3)
        for t in tables:
            if t.proc and t.proc.poll() is None:
                t.proc.kill()
            t.nettoyer()
        if DERNIER_MONDE:
            open("/tmp/charge-monde.json", "w").write(DERNIER_MONDE["m"][:200000])
        print("Tables arretees et nettoyees.", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", type=int, default=100)
    ap.add_argument("--palier", type=int, default=10)
    ap.add_argument("--palier-s", dest="palier_s", type=int, default=90)
    ap.add_argument("--tenue-s", dest="tenue_s", type=int, default=300)
    ap.add_argument("--decalage-s", dest="decalage_s", type=float, default=1.5)
    ap.add_argument("--pense-min", dest="pense_min", type=float, default=0.8)
    ap.add_argument("--pense-max", dest="pense_max", type=float, default=3.0)
    ap.add_argument("--plancher-mo", dest="plancher_mo", type=int, default=300)
    ap.add_argument("--site-max-ms", dest="site_max_ms", type=int, default=3000)
    ap.add_argument("--charge", default="/tmp/charge-partie.json")
    ap.add_argument("--sortie", default="/tmp/charge-resultats.jsonl")
    a = ap.parse_args()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tache = loop.create_task(principal(a))
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, tache.cancel)
    try:
        loop.run_until_complete(tache)
    except asyncio.CancelledError:
        pass
