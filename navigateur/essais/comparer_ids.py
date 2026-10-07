#!/usr/bin/env python3
"""Compare, pour CHAQUE heros de depart, les options proposees au premier tour entre le code AVANT et APRES le
correctif de player_setup.py (ordre des formes). Sert a mesurer l'effet du tri sur les identifiants d'options,
donc sur la reprise de sauvegardes anciennes."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
ICI = os.path.dirname(os.path.abspath(__file__)); NAV = os.path.dirname(ICI)
PY = os.path.expanduser("~/marvel-work/python/bin/python3.10")
MOTEUR = os.path.join(os.path.dirname(NAV), "Fusion", "marvel-lcg-src")
heros = sorted(f[:-5] for f in os.listdir(os.path.join(MOTEUR, "deck", "starter")) if f.endswith(".json"))
def premier_tour(dossier, h):
    env = {**os.environ, "HERO": h, "VILLAIN": "rhino", "SEED": "11", "MAX_ASKS": "6", "ENG_DIR": dossier, "TRACE": "1",
           "CONFIG": "launch-cmp.json"}
    cfg = json.load(open(os.path.join(dossier, "launch.json"))); txt = json.dumps(cfg).replace("./persist/", f"./persist/cmp-{h}/")
    os.makedirs(os.path.join(dossier, "persist", f"cmp-{h}", "replays"), exist_ok=True)
    os.makedirs(os.path.join(dossier, "persist", f"cmp-{h}", "campagnes"), exist_ok=True)
    os.makedirs(os.path.join(dossier, "persist", f"cmp-{h}", "deck", "custom"), exist_ok=True)
    nom = f"launch-cmp-{h}.json"; open(os.path.join(dossier, nom), "w").write(txt); env["CONFIG"] = nom
    try:
        p = subprocess.run([PY, os.path.join(ICI, "partie_headless.py")], env=env, cwd=dossier, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "delai"
    for l in p.stdout.splitlines():
        if l.startswith("TR "):
            q = json.loads(l[3:])
            if "Tour de" in q["prompt"]:
                return [(o[0], o[1]) for o in q["opts"]]
    return "pas de tour"
def un(h):
    return h, premier_tour(os.path.join(NAV, ".cache", "natif_old"), h), premier_tour(os.path.join(NAV, ".cache", "natif"), h)
diff = []
with ThreadPoolExecutor(4) as ex:
    for h, a, b in ex.map(un, heros):
        if a != b: diff.append((h, a, b))
print(f"{len(heros)} heros ; options du premier tour DIFFERENTES avant/apres : {len(diff)}")
for h, a, b in diff[:40]:
    print(f"  {h:24} avant={a if isinstance(a,str) else [x[1][:14]+'#'+str(x[0]) for x in a][:6]}  apres={b if isinstance(b,str) else [x[1][:14]+'#'+str(x[0]) for x in b][:6]}")
