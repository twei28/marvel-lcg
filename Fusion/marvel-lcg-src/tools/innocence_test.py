import os, json, py_compile, shutil, subprocess, sys
SRC = os.path.expanduser("~/marvel-work/marvel-lcg-independent/source_recovered")
BOOT = os.path.expanduser("~/marvel-work/boot")
DST = os.path.expanduser("~/marvel-work/boot_sub")
PY = os.path.expanduser("~/marvel-work/python/bin/python3.10")
reverted = json.load(open("/tmp/reverted_list.json"))
port = 5600
innocents, defectives = [], []
def newgame_ok(p):
    subprocess.run([PY, "-c", f"""
import json, os
cp = os.path.join({DST!r}, 'launch.json')
cfg = json.load(open(cp)); cfg['server_addresses'] = ['127.0.0.1:{p}']
json.dump(cfg, open(cp, 'w'), indent=2)"""])
    subprocess.run(["timeout", "120", PY, os.path.expanduser("~/marvel-work/tools/test_newgame.py"), DST],
                   env={**os.environ, "RELEASE": "1"}, cwd=DST, capture_output=True)
    try:
        return "PLAYERS:" in open("/tmp/game_stdout.log").read()
    except FileNotFoundError:
        return False
for rel in reverted:
    port += 1
    pyc = os.path.join(DST, rel[:-3] + ".pyc")
    py_compile.compile(os.path.join(SRC, rel), cfile=pyc, doraise=True)
    if newgame_ok(port):
        innocents.append(rel)
        print("INNOCENT", rel, flush=True)
    else:
        shutil.copy(os.path.join(BOOT, rel[:-3] + ".pyc"), pyc)
        defectives.append(rel)
        print("DEFECTUEUX", rel, flush=True)
json.dump({"innocents": innocents, "defectives": defectives}, open("/tmp/innocence_report.json", "w"), indent=1)
print(f"BILAN: {len(innocents)} innocents, {len(defectives)} défectueux")
