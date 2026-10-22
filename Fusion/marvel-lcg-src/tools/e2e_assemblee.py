"""Deux TABLES REELLES (deux serveurs de jeu) qui forment une assemblee Kingsfall : essai de bout en bout.

    ../../.venv-linux/bin/python tools/e2e_assemblee.py

Lance deux moteurs (ports 7751/7752, dossiers de jeu temporaires dans /tmp/claude-29999/pod), cree l'assemblee sur la table 1, refuse un mauvais code sur la
table 2, la fait rejoindre avec le bon, puis relit l'etat des deux cotes (`/get_world` et `/get_assemblee`). Les websockets « Connected » remplacent le navigateur.
Ne touche ni aux dossiers du depot ni aux tables du site. Ecrit en septembre-octobre 2026 pour la campagne MC×DC.
"""
import json, os, subprocess, sys, time, urllib.request, urllib.parse, gzip, shutil, signal, asyncio, threading
SRC = "/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
PY = "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"
RACINE = "/tmp/claude-29999/pod"
DB = f"{RACINE}/assemblees.db"
for f in (DB, DB + "-wal", DB + "-shm"):
    if os.path.exists(f): os.remove(f)
base = json.load(open(f"{SRC}/.game-src/launch.json"))

def preparer(n, port):
    d = f"{RACINE}/jeu{n}"
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for nom in ("assets", "cards", "core", "data", "deck", "editor", "engine", "game", "public", "puzzle"):
        os.symlink(f"{SRC}/.game-src/{nom}" if os.path.islink(f"{SRC}/.game-src/{nom}") else f"{SRC}/{nom}", f"{d}/{nom}")
    for nom in ("build.py", "main.py", "game_entry.py", "winsound.py"):
        shutil.copy(f"{SRC}/.game-src/{nom}", d)
    cfg = json.loads(json.dumps(base))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["table_nom"] = f"p{n}"
    cfg["detected_version"] = False
    cfg["detect_version"] = False
    cfg["assemblees_fichier"] = DB
    cfg["replay_folders"] = [f"{d}/replays/"]
    cfg["games_history_file"] = f"{d}/games_history.json"
    cfg["game_statistics_file"] = f"{d}/stats.json"
    cfg["deck_folders"] = [f"{d}/deckcustom/"]
    cfg["achievements_file"] = f"{d}/ach.json"
    json.dump(cfg, open(f"{d}/launch.json", "w"))
    journal = open(f"{d}/serveur.log", "w")
    p = subprocess.Popen([PY, "-u", "main.py", "-config_files", "launch.json"], cwd=d, env=dict(os.environ, PYTHONPATH=d, RELEASE="1"),
                         stdout=journal, stderr=subprocess.STDOUT, start_new_session=True)
    return p

def attendre(port):
    for _ in range(120):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/get_site_url", timeout=2); return True
        except Exception as e:
            if getattr(e, "code", None): return True
            time.sleep(0.5)
    return False

def descripteur(regles):
    sc = json.load(open(f"{SRC}/data/scenarios/kingsfall.json"))
    deck = json.load(open(f"{SRC}/deck/starter/spider_man.json")); deck["name"] = "Spider-Man"
    return {"campaign_json": json.dumps(sc), "encounter_set_names": sc.get("encounter_sets", []) + sc.get("modular_sets", []),
            "hero_json": [json.dumps(deck)], "seed": 7, "timeout": 0, "challenges": [], "rules": regles + ["mode_campaign", "v16_all", "v18_all"],
            "campaign_log": {"Punisher Ally": "1", "Player 1 Identity": "Spider-Man"}}

def get(port, chemin):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{chemin}", headers={"Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            corps = r.read()
            if r.headers.get("Content-Encoding") == "gzip": corps = gzip.decompress(corps)
            return r.status, corps.decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def connecter(port):
    async def boucle():
        import aiohttp
        async with aiohttp.ClientSession() as sess:
            async with sess.ws_connect(f"http://127.0.0.1:{port}/ws?p=0") as ws:
                await ws.send_str("Connected")
                for _ in range(400):
                    try:
                        await asyncio.wait_for(ws.receive(), timeout=1)
                    except asyncio.TimeoutError:
                        pass
    threading.Thread(target=lambda: asyncio.run(boucle()), daemon=True).start()

def nouvelle(port, regles):
    return get(port, "/new?data=" + urllib.parse.quote(json.dumps(descripteur(regles))))

def monde(port):
    d = {}
    for _ in range(120):
        s, c = get(port, "/get_world")
        try: d = json.loads(c)
        except Exception: d = {}
        if (d.get("assemblee") or {}).get("code"):
            return d
        time.sleep(0.5)
    print("  (pas d'assemblee dans le monde ; phase =", d.get("phase"), "round =", d.get("round_id"), "render =", d.get("render_id"), "cles =", [k for k in d][:6], ")")
    return d

procs = [preparer(1, 7751), preparer(2, 7752)]
try:
    assert attendre(7751) and attendre(7752), "les serveurs ne repondent pas"
    print("serveurs prets")
    s, c = nouvelle(7751, ["assemblee_creer"]); print("table 1 /new :", s, c[:120])
    connecter(7751)
    time.sleep(3)
    m1 = monde(7751); a1 = m1.get("assemblee") or {}
    print("table 1 assemblee :", {k: a1.get(k) for k in ("code", "table", "organisateur", "seuil", "joueurs")}, [g["tab"] for g in a1.get("groupes", [])])
    code = a1.get("code")
    s, c = nouvelle(7752, ["assemblee_rejoindre_KING-ZZZZ"]); print("table 2 /new avec un MAUVAIS code :", s, c[:160])
    s, c = nouvelle(7752, ["assemblee_rejoindre_" + code.lower()]); print("table 2 /new avec le bon code :", s, c[:80])
    connecter(7752)
    time.sleep(3)
    m2 = monde(7752); a2 = m2.get("assemblee") or {}
    print("table 2 assemblee :", {k: a2.get(k) for k in ("code", "table", "organisateur", "seuil", "joueurs")}, [g["tab"] for g in a2.get("groupes", [])])
    m1 = monde(7751); a1 = m1.get("assemblee") or {}
    print("table 1 revue (2 groupes ?) :", [g["tab"] for g in a1.get("groupes", [])], "seuil", a1.get("seuil"))
    s1, c1 = get(7751, "/get_assemblee?p=0"); live = json.loads(c1)
    print("table 1 /get_assemblee EN DIRECT :", [g["tab"] for g in live.get("groupes", [])], "seuil", live.get("seuil"), "joueurs", live.get("joueurs"))
    noms = lambda m: sorted((c.get("name", "") for k in ("area_environment",) for c in (m.get(k) or [])))
    print("environnements table 1 :", noms(m1)); print("environnements table 2 :", noms(m2))
finally:
    for p in procs:
        try: os.killpg(p.pid, signal.SIGTERM)
        except Exception: pass
