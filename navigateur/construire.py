#!/usr/bin/env python3
"""Assemble navigateur/dist : le jeu qui tourne ENTIEREMENT dans le navigateur (moteur Python via Pyodide).

    python3 navigateur/construire.py            # construit navigateur/dist (--sans-pages : moteur et scripts seulement)
    python3 navigateur/serveur-local.py 8770    # l'essaie : http://localhost:8770/navigateur.html

Rien n'est modifie hors de navigateur/ : le moteur (Fusion/marvel-lcg-src/src), le plateau construit
(Fusion/marvel-lcg-src/public/app) et le serveur restent tels quels. Le plateau n'est PAS reconstruit ici :
lancer `bash ui-app/deployer.sh` avant si ui-app a change.

Hebergement : n'importe quel serveur statique, avec ces deux en-tetes sur TOUTES les reponses :
    Cross-Origin-Opener-Policy: same-origin
    Cross-Origin-Embedder-Policy: credentialless      (ou require-corp si tout est de meme origine)
et les scans servis sous /scan/<id> (voir serveur-local.py pour la resolution : pics-fr, pics, textures,
cache ; .webp, .jpg, .png).
"""
import hashlib, json, os, re, shutil, subprocess, sys, time, urllib.request, zipfile

PYODIDE = "0.27.8"
CDN = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE}/full/"
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
CACHE = os.path.join(ICI, ".cache", f"pyodide-{PYODIDE}")
DIST = os.path.join(ICI, "dist")
SRC = os.path.join(ICI, "src")
COLORAMA = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl"
PAQUETS = ["aiohttp", "typing-extensions", "requests", "packaging", "numpy", "pillow"]
CORE = ["pyodide.mjs", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]

def telecharger(url, dest):
    if os.path.isfile(dest) and os.path.getsize(dest) > 0:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print("  telechargement", os.path.basename(dest))
    urllib.request.urlretrieve(url, dest)

def roues_pyodide():
    lock = json.load(open(os.path.join(CACHE, "pyodide-lock.json"), encoding="utf-8"))["packages"]
    vus, out = set(), []
    def vers(n):
        n = n.lower().replace("_", "-")
        if n in vus or n not in lock:
            return
        vus.add(n); out.append(lock[n]["file_name"])
        for d in lock[n]["depends"]:
            vers(d)
    for p in PAQUETS:
        vers(p)
    return out

def config_navigateur():
    """launch.json du moteur dans le navigateur : tout ce qui s'ecrit va sous /eng/persist (garde par la page). Chemins RELATIFS : le moteur ne sait pas rechercher un chemin absolu POSIX.."""
    c = json.load(open(os.path.join(MOTEUR, "launch.json"), encoding="utf-8"))
    c.update({
        "detected_version": False, "password": "", "server_addresses": ["127.0.0.1:2345"],
        "game_statistics_file": "./persist/statistics.json", "games_history_file": "./persist/games_history.json",
        "legacy_file": "./persist/legacy.json", "achievements_file": "./persist/achievements.json",
        "arts_heros_file": "./persist/arts-heros.json", "campaign_log_last_file": "./persist/campaign_log_last.json",
        "campagne_folder": "./persist/campagnes/", "replay_folders": ["./persist/replays/"],
        "deck_folders": ["./persist/deck/custom/", "./deck/custom/"],
        "image_servers": [], "image_folders": [], "sound_folders": [],
    })
    return c

def construire_moteur(zip_path):
    stage = os.path.join(ICI, ".cache", "stage")
    shutil.rmtree(stage, ignore_errors=True); os.makedirs(stage)
    ignore = shutil.ignore_patterns("__pycache__", "*.bak*", "marvelcdb")
    for d in ("cards", "core", "engine", "game", "editor"):
        shutil.copytree(os.path.join(MOTEUR, "src", d), os.path.join(stage, d), ignore=ignore)
    for f in ("build.py", "game_entry.py", "main.py"):
        shutil.copy(os.path.join(MOTEUR, "src", f), stage)
    for d in ("data", "deck", "puzzle"):
        shutil.copytree(os.path.join(MOTEUR, d), os.path.join(stage, d), ignore=ignore)
    os.makedirs(os.path.join(stage, "deck", "custom"), exist_ok=True)
    json.dump(config_navigateur(), open(os.path.join(stage, "launch.json"), "w", encoding="utf-8"), indent=1)
    # colorama (pur Python) : le moteur l'importe, Pyodide ne l'embarque pas
    wheel = os.path.join(CACHE, "colorama-0.4.6-py2.py3-none-any.whl"); telecharger(COLORAMA, wheel)
    zipfile.ZipFile(wheel).extractall(stage)
    # Bytecode precompile (Python 3.12, comme Pyodide) : demarrage plus court et sources non servies.
    py312 = shutil.which("python3.12")
    if py312:
        for d in ("cards", "core", "engine", "game", "editor"):
            subprocess.run([py312, "-m", "compileall", "-q", "-b", "-j", "8", os.path.join(stage, d)], check=True)
            for dp, dn, fn in os.walk(os.path.join(stage, d)):
                for f in fn:
                    if f.endswith(".py"):
                        os.remove(os.path.join(dp, f))
        subprocess.run([py312, "-m", "compileall", "-q", "-b", os.path.join(stage, "build.py")], check=False)
    else:
        print("  ATTENTION : python3.12 absent, sources non compilees (demarrage plus lent)")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dp, dn, fn in os.walk(stage):
            dn[:] = [d for d in dn if d != "__pycache__"]
            for f in fn:
                p = os.path.join(dp, f); z.write(p, os.path.relpath(p, stage))

def pages_publiques():
    """public/ tel quel, avec le script de redirection injecte en tete de chaque page HTML."""
    src = os.path.join(MOTEUR, "public")
    for dp, dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        os.makedirs(os.path.join(DIST, rel), exist_ok=True)
        for f in fn:
            s, d = os.path.join(dp, f), os.path.join(DIST, rel, f)
            if f.endswith((".html", ".js", ".mjs", ".css")):
                t = open(s, encoding="utf-8").read()
                # Le moteur sert public/ sous /public/ ET a la racine ; ici l'hebergeur statique n'a que la racine.
                t = re.sub(r"([\"'`(])/public/", r"\1/", t)
                if f.endswith(".html"):
                    m = re.search(r"<head[^>]*>", t, re.I)
                    t = t[:m.end()] + '\n<script src="/shim.js"></script>' + t[m.end():] if m else '<script src="/shim.js"></script>' + t
                open(d, "w", encoding="utf-8").write(t)
            else:
                shutil.copy(s, d)

def empreintes():
    """Chaque adresse de code (js, css) des pages porte l'empreinte de la publication.

    ⚠ SANS ELLE, UN JOUEUR GARDAIT L'ANCIEN ECRAN (constat du 07/10/2026). Beaucoup
    de modules sont importes sans numero de version (« ./repliques-heros.js ») et
    le navigateur les garde en cache : apres une publication, il melangeait du
    code neuf et du code de la veille sans que rien ne le dise au joueur. Une
    adresse qui change a chaque publication l'oblige a tout reprendre, tout seul.

    Une seule empreinte pour toutes les pages : un module qui change change aussi
    l'adresse de ceux qui l'importent, sans calcul de dependances. `app/` (le
    plateau) est laisse tel quel : Vite nomme deja ses fichiers par leur contenu,
    et y ajouter un parametre dedoublerait ses modules charges par d'autres chemins.
    """
    fichiers = []
    for dp, dn, fn in os.walk(DIST):
        rel = os.path.relpath(dp, DIST)
        if rel == "app" or rel.startswith("app" + os.sep):
            continue
        fichiers += [os.path.join(dp, f) for f in fn if f.endswith((".html", ".js", ".mjs", ".css"))]
    h = hashlib.sha1()
    for chemin in sorted(fichiers):
        h.update(open(chemin, "rb").read())
    v = h.hexdigest()[:10]
    motif = re.compile(r"([\"'`])((?:\.{1,2}/|/)[^\"'`?\s]+?\.(?:m?js|css))(?:\?v=[^\"'`]*)?\1")
    for chemin in fichiers:
        t = open(chemin, encoding="utf-8").read()
        def remplacer(m):
            cible = m.group(2)
            base = DIST if cible.startswith("/") else os.path.dirname(chemin)
            if cible.startswith("/app/") or not os.path.exists(os.path.normpath(os.path.join(base, cible.lstrip("/")))):
                return m.group(0)
            return f"{m.group(1)}{cible}?v={v}{m.group(1)}"
        neuf = motif.sub(remplacer, t)
        if neuf != t:
            open(chemin, "w", encoding="utf-8").write(neuf)
    print("  empreinte des pages", v)

def main():
    print("Pyodide", PYODIDE)
    for f in CORE:
        telecharger(CDN + f, os.path.join(CACHE, f))
    wheels = roues_pyodide()
    for w in wheels:
        telecharger(CDN + w, os.path.join(CACHE, w))
    rapide = "--sans-pages" in sys.argv      # ne refait que le moteur et les scripts (les pages copiees restent)
    if not rapide:
        shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
        print("Pages et plateau"); pages_publiques(); empreintes()
    print("Moteur"); construire_moteur(os.path.join(DIST, "moteur.zip"))
    for f in CORE + wheels:
        shutil.copy(os.path.join(CACHE, f), DIST)
    for f in ("shim.js", "moteur-worker.js", "boot_navigateur.py", "navigateur.html"):
        shutil.copy(os.path.join(SRC, f), DIST)
    # Numero de version = empreinte du contenu : il change a chaque publication utile, jamais sinon.
    h = hashlib.sha1()
    for f in ("moteur.zip", "boot_navigateur.py", "shim.js", "moteur-worker.js", "navigateur.html"):
        h.update(open(os.path.join(DIST, f), "rb").read())
    version = h.hexdigest()[:10]
    chemin = os.path.join(DIST, "navigateur.html")
    t = open(chemin, encoding="utf-8").read().replace("__VERSION__", version)
    open(chemin, "w", encoding="utf-8").write(t)
    json.dump({"version": version, "date": time.strftime("%Y-%m-%dT%H:%M:%S")}, open(os.path.join(DIST, "version.json"), "w"))
    print("  version", version)
    taille = lambda p: os.path.getsize(os.path.join(DIST, p)) / 1e6
    print(f"OK : {DIST}\n  moteur.zip {taille('moteur.zip'):.1f} Mo, pyodide.asm.wasm {taille('pyodide.asm.wasm'):.1f} Mo")

if __name__ == "__main__":
    main()
