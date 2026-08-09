"""Répare les cartes en échec : requotage d'annotations, sinon version Claude,
sinon marquage défectueux. Un seul boot, reload par module.

Usage: python3.10 card_fix_loop.py <report_regressions.json>
"""
import sys, os, json, re, importlib, py_compile, traceback

GAME_DIR = os.path.expanduser("~/marvel-work/boot_sub")
SRC = os.path.expanduser("~/marvel-work/marvel-lcg-independent/source_recovered")
CLAUDE = os.path.expanduser("~/marvel-work/marvel-lcg-rebuilt/backend")
REPORT_IN = sys.argv[1]

os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
cfg = json.load(open("launch.json"))
cfg["server_addresses"] = ["127.0.0.1:5810"]
json.dump(cfg, open("launch.json", "w"), indent=2)
sys.stdout = open("/tmp/cardfix_stdout.log", "w", buffering=1)
sys.stderr = sys.stdout

def annotation_spans(line):
    """Rend les (début, fin) des expressions d'annotation après ': ' ou '-> '."""
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

def try_quote_fix(path, name):
    lines = open(path).readlines()
    changed = False
    for idx, line in enumerate(lines):
        for start, end in reversed(annotation_spans(line)):
            expr = line[start:end]
            if re.search(rf"\b{re.escape(name)}\b", expr) and "'" not in expr and '"' not in expr:
                line = line[:start] + f"'{expr.strip()}'" + line[end:]
                changed = True
        lines[idx] = line
    if changed:
        open(path, "w").writelines(lines)
    return changed

from engine import Engine
print("INIT:", Engine.Initialize(), flush=True)

base = json.load(open("/tmp/cards_report_original.json"))
rep = json.load(open(REPORT_IN))
targets = sorted(set(rep["failures"]) - set(base["failures"]))
print(len(targets), "cartes à réparer", flush=True)

def rel_of(modname):
    return modname.replace(".", "/") + ".py"

def attempt(modname):
    """Rend None si OK, sinon (exception, fichier_source_fautif|None)."""
    try:
        m = importlib.import_module(modname)
        importlib.reload(m)
        if hasattr(m, "GetAbilities"):
            m.GetAbilities()
        return None
    except Exception as e:
        tb = e.__traceback__
        bad = None
        while tb:
            fn = tb.tb_frame.f_code.co_filename
            if "source_recovered" in fn:
                bad = fn
            tb = tb.tb_next
        return (e, bad)

provenance = {}
for modname in targets:
    rel = rel_of(modname)
    src = os.path.join(SRC, rel)
    pyc = os.path.join(GAME_DIR, rel[:-3] + ".pyc")
    fixed = False
    # 1. requotage itératif (max 8 noms), sur le fichier fautif de la traceback
    for _ in range(8):
        r = attempt(modname)
        if r is None:
            provenance[modname] = "chatgpt_quote"
            fixed = True
            break
        e, bad_file = r
        m_name = re.search(r"name '(\w+)' is not defined", str(e))
        target_src = bad_file if bad_file else src
        if not (isinstance(e, NameError) and m_name and target_src
                and os.path.exists(target_src) and try_quote_fix(target_src, m_name.group(1))):
            break
        bad_rel = os.path.relpath(target_src, SRC)
        py_compile.compile(target_src, cfile=os.path.join(GAME_DIR, bad_rel[:-3] + ".pyc"), doraise=True)
        # invalider les modules chargés depuis ce fichier
        for mn, mod in list(sys.modules.items()):
            if getattr(mod, "__file__", None) == target_src or (mn.startswith("cards.") and bad_rel[:-3].replace("/", ".") in mn):
                del sys.modules[mn]
    if fixed:
        print("QUOTE", modname, flush=True)
        continue
    # 2. version Claude
    csrc = os.path.join(CLAUDE, rel)
    if os.path.exists(csrc):
        try:
            py_compile.compile(csrc, cfile=pyc, doraise=True)
            for mn in list(sys.modules):
                if mn == modname:
                    del sys.modules[mn]
            if attempt(modname) is None:
                provenance[modname] = "claude"
                print("CLAUDE", modname, flush=True)
                continue
        except Exception:
            pass
    # 3. rien ne marche : marquer défectueux, remettre ChatGPT si compile
    provenance[modname] = "defectueux"
    r = attempt(modname)
    detail = "" if r is None else f"{type(r[0]).__name__}: {r[0]} @ {r[1]}"
    print("DEFECTUEUX", modname, "|", detail[:140], flush=True)

json.dump(provenance, open("/tmp/card_provenance.json", "w"), indent=1)
from collections import Counter
print("BILAN:", dict(Counter(provenance.values())), flush=True)
os._exit(0)
