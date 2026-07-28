"""Serveur de developpement du jeu, sur un port choisi, sans authentification.

    ~/marvel-work/python/bin/python3.10 \
      "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/ui-check/scripts/serveur-dev.py" --port 2346

POURQUOI CE SCRIPT EXISTE
-------------------------
Le port 2345 n'est pas toujours disponible : `JOUER-EN-MULTI.bat` y demarre une
partie multijoueur depuis `Fusion/marvel-lcg-src`, qui est un codebase de
DISTRIBUTION, perime, et protege par un mot de passe. Tant qu'une partie tourne,
le harnais n'a aucun moyen d'atteindre le codebase de TRAVAIL
(`~/marvel-work/fusion/marvel-lcg-src`), le seul que `ui-app/deployer.sh`
alimente et que les plans modifient.

Ce script ouvre un second moteur, sur un autre port, depuis le codebase de
travail, sans toucher a la partie en cours.

CE QU'IL FAIT, ET RIEN D'AUTRE
------------------------------
1. `launcher_fast.py --build-only` : compilation incrementale et liens
   symboliques (`.game/public` -> `public/`), moteur NON demarre.
2. Reecrit `.game/launch.json` (un artefact de build, jamais une source) avec le
   port demande et un mot de passe vide.
3. Demarre le moteur, comme le fait l'etape 3 de `launcher_fast.py`, mais sans
   ouvrir de navigateur : le poste est peut-etre en train de jouer.

`launch.json` a la racine du jeu n'est jamais modifie. Un lancement normal par
`launcher_fast.py` recopie `launch.json` par-dessus et rend son port au jeu.
"""
import argparse
import json
import os
import subprocess
import sys
import types

JEU_PAR_DEFAUT = os.path.expanduser("~/marvel-work/fusion/marvel-lcg-src")

# Comme launcher_fast.py, et AVANT tout import du moteur : sans cette variable le
# moteur demarre en mode debug (version `0.5.9.200d`) et cherche `editor.editor`,
# qui n'est pas distribue. Les references du harnais ont ete prises en mode
# release (`0.5.9.200r`).
os.environ["RELEASE"] = "1"


def main() -> None:
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--port", type=int, default=2346, help="port d'ecoute (defaut : 2346)")
    arg.add_argument("--jeu", default=JEU_PAR_DEFAUT, help="racine du codebase de travail")
    options = arg.parse_args()

    if sys.version_info[:2] != (3, 10):
        raise SystemExit(
            f"Python 3.10 obligatoire (le moteur ne compile pas ailleurs), detecte {sys.version.split()[0]}"
        )

    racine = os.path.abspath(options.jeu)
    launcher = os.path.join(racine, "launcher_fast.py")
    if not os.path.isfile(launcher):
        raise SystemExit(f"Introuvable : {launcher}. Mauvaise racine de jeu ?")

    # 1. Construction seule. On reutilise le lanceur du jeu au lieu de refaire sa
    #    compilation incrementale : c'est lui qui a raison, pas ce script.
    subprocess.run([sys.executable, launcher, "--build-only"], cwd=racine, check=True)

    jeu_compile = os.path.join(racine, ".game")
    config = os.path.join(jeu_compile, "launch.json")
    with open(config, encoding="utf-8") as f:
        reglages = json.load(f)
    reglages["server_addresses"] = [f"127.0.0.1:{options.port}"]
    reglages["password"] = ""  # serveur de dev local : jamais de mot de passe, jamais de tunnel.
    with open(config, "w", encoding="utf-8") as f:
        json.dump(reglages, f, indent=2)

    # 2. Demarrage (copie de l'etape 3 de launcher_fast.py, sans le navigateur).
    os.chdir(jeu_compile)
    sys.path.insert(0, jeu_compile)

    try:
        import winsound  # noqa: F401
    except ModuleNotFoundError:
        # Le moteur est un portage Windows : il importe winsound sans condition.
        faux = types.ModuleType("winsound")
        for nom in ("Beep", "PlaySound", "MessageBeep"):
            setattr(faux, nom, lambda *a, **k: None)
        for nom in (
            "SND_FILENAME", "SND_ALIAS", "SND_LOOP", "SND_MEMORY", "SND_PURGE",
            "SND_ASYNC", "SND_NODEFAULT", "SND_NOSTOP", "SND_NOWAIT", "SND_APPLICATION",
            "MB_ICONASTERISK", "MB_ICONEXCLAMATION", "MB_ICONHAND", "MB_ICONQUESTION", "MB_OK",
        ):
            setattr(faux, nom, 0)
        sys.modules["winsound"] = faux

    from engine.network.web_server import WebServer

    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine import Engine

    print("Engine.Initialize() ->", Engine.Initialize())
    print(f"Serveur de developpement sur http://127.0.0.1:{options.port} (codebase : {racine})")
    Engine.EngineRun()


if __name__ == "__main__":
    main()
