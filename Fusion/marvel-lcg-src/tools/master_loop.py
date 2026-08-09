"""Boucle maîtresse : substitution totale du moteur, test NewGame, réparation
automatique des annotations dé-quotées (NameError), revert sinon.

Usage: python3.10 master_loop.py [max_iters]
"""
import os, re, json, shutil, subprocess, sys, py_compile

SRC = os.path.expanduser("~/marvel-work/marvel-lcg-independent/source_recovered")
BOOT = os.path.expanduser("~/marvel-work/boot")
DST = os.path.expanduser("~/marvel-work/boot_sub")
PY = os.path.expanduser("~/marvel-work/python/bin/python3.10")
LOG = "/tmp/game_stdout.log"
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300

def engine_files():
    out = []
    for pkg in ("core", "engine", "game"):
        for root, dirs, files in os.walk(os.path.join(BOOT, pkg)):
            for f in files:
                if f.endswith(".pyc"):
                    rel = os.path.relpath(os.path.join(root, f), BOOT)[:-4] + ".py"
                    if os.path.exists(os.path.join(SRC, rel)):
                        out.append(rel)
    return sorted(out)

def substitute(rel):
    py_compile.compile(os.path.join(SRC, rel), cfile=os.path.join(DST, rel[:-3] + ".pyc"), doraise=True)

def revert(rel):
    shutil.copy(os.path.join(BOOT, rel[:-3] + ".pyc"), os.path.join(DST, rel[:-3] + ".pyc"))

def run_test(port):
    subprocess.run([PY, "-c", f"""
import json, os
cp = os.path.join({DST!r}, 'launch.json')
cfg = json.load(open(cp)); cfg['server_addresses'] = ['127.0.0.1:{port}']
json.dump(cfg, open(cp, 'w'), indent=2)"""], check=True)
    subprocess.run(["timeout", "150", PY, os.path.expanduser("~/marvel-work/tools/test_newgame.py"), DST],
                   env={**os.environ, "RELEASE": "1"}, cwd=DST, capture_output=True)
    try:
        return open(LOG).read()
    except FileNotFoundError:
        return ""

def annotation_spans(line):
    """Rend les (début, fin) des expressions d'annotation après ': ' ou '-> '.
    Fin de span : ',' ')' '=' ':' au niveau de crochets 0."""
    spans = []
    i = 0
    while i < len(line):
        m = re.match(r"(:\s*|->\s*)", line[i:])
        if not m or (line[i] == ':' and i + len(m.group(0)) >= len(line.rstrip('\n'))):
            i += 1
            continue
        start = i + len(m.group(0))
        j, depth = start, 0
        while j < len(line):
            c = line[j]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif depth == 0 and c in ",=:":
                break
            j += 1
        if j > start:
            spans.append((start, j))
        i = j if j > i else i + 1
    return spans

def try_quote_fix(rel, line_no, name):
    """Requote dans TOUT le fichier les expressions d'annotation contenant le
    nom fautif. True si au moins une modification."""
    p = os.path.join(SRC, rel)
    lines = open(p).readlines()
    changed = False
    for idx, line in enumerate(lines):
        for start, end in reversed(annotation_spans(line)):
            expr = line[start:end]
            if re.search(rf"\b{re.escape(name)}\b", expr) and "'" not in expr and '"' not in expr:
                stripped = expr.strip()
                line = line[:start] + f"'{stripped}'" + line[end:]
                changed = True
        lines[idx] = line
    if changed:
        open(p, "w").writelines(lines)
    return changed

# 1. substitution totale (sauf mode reprise)
if "--resume" not in sys.argv:
    files = engine_files()
    for rel in files:
        substitute(rel)
    print(f"substitution totale: {len(files)} fichiers", flush=True)
else:
    print("reprise: état boot_sub conservé", flush=True)

actions = []
port = 5000
for i in range(1, MAX + 1):
    port += 1
    log = run_test(port)
    if "PLAYERS:" in log:
        print(f"NEWGAME OK après {i-1} itérations", flush=True)
        break
    m_files = re.findall(r'source_recovered/([A-Za-z0-9_/]+\.py)", line (\d+)', log)
    m_name = re.search(r"NameError: name '(\w+)' is not defined", log)
    if not m_files:
        print(f"ERREUR NON LOCALISABLE (iter {i}):", flush=True)
        print("\n".join(log.splitlines()[-12:]), flush=True)
        break
    rel, line_no = m_files[-1][0], int(m_files[-1][1])
    if m_name and try_quote_fix(rel, line_no, m_name.group(1)):
        substitute(rel)
        actions.append(("quote", rel, line_no, m_name.group(1)))
        print(f"quote[{i}]: {rel}:{line_no} ({m_name.group(1)})", flush=True)
    else:
        revert(rel)
        actions.append(("revert", rel, line_no, ""))
        print(f"revert[{i}]: {rel}", flush=True)

json.dump(actions, open("/tmp/master_actions.json", "w"), indent=1)
n_rev = sum(1 for a in actions if a[0] == "revert")
n_quote = sum(1 for a in actions if a[0] == "quote")
print(f"BILAN: {n_quote} annotations requotées, {n_rev} fichiers rebasculés", flush=True)
