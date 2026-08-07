"""Verifie l'ISOLEMENT du mode serveur, avec deux vrais moteurs.

Ce que ce test prouve :
  1. les deux moteurs repondent, chacun sur son port ;
  2. une sauvegarde de la place 1 n'apparait PAS chez la place 2 ;
  3. un deck de l'hote apparait chez les DEUX ;
  4. un deck enregistre depuis la place 1 atterrit chez elle, pas chez l'hote.

Les fichiers temoins sont crees AVANT le demarrage des moteurs : le moteur
sert des listes avec un cache, et un fichier depose apres coup pourrait ne pas
apparaitre tout de suite.

Le chemin de la sauvegarde temoin est derive avec la MEME logique que
tools/config_serveur.py (ecrire_configs) : les chemins de la configuration
sont relatifs a .game/, pas a la racine, car le moteur fait os.chdir(.game)
avant de les resoudre. "../replays/serveur-1/" designe donc
<RACINE>/replays/serveur-1/, pas <RACINE>/../replays/serveur-1/.

Usage: python3.10 tools/test_serveur_multi.py
"""
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTS = {1: 2351, 2: 2352}
# Meme derivation que ecrire_configs : depuis .game/, "../replays/serveur-1/"
# retombe sur <RACINE>/replays/serveur-1/.
TEMOIN_SAUVEGARDE = os.path.normpath(
    os.path.join(RACINE, ".game", "..", "replays", "serveur-1", "zzz-temoin-partie.json"))
TEMOIN_DECK_HOTE = os.path.join(RACINE, "deck", "custom", "zzz-temoin-hote.json")
DECK_ECRIT = os.path.join(RACINE, "deck", "serveur-1", "zzz-temoin-ecriture.json")
DECK_ECRIT_CHEZ_HOTE = os.path.join(RACINE, "deck", "custom", "zzz-temoin-ecriture.json")

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), str(detail)))


def lire(port, route):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{route}", timeout=20) as reponse:
        return json.loads(reponse.read().decode())


def poster(port, route, corps):
    requete = urllib.request.Request(
        f"http://127.0.0.1:{port}{route}",
        data=json.dumps(corps).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(requete, timeout=20) as reponse:
        return reponse.status, json.loads(reponse.read().decode())


def attendre(port, secondes=240):
    for _ in range(secondes):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2).read()
            return True
        except Exception:
            time.sleep(1)
    return False


def nettoyer_temoins():
    for chemin in (TEMOIN_SAUVEGARDE, TEMOIN_DECK_HOTE, DECK_ECRIT, DECK_ECRIT_CHEZ_HOTE):
        if os.path.exists(chemin):
            os.remove(chemin)


# --- Preparation : les configurations, puis les fichiers temoins ---
subprocess.run([sys.executable, os.path.join(RACINE, "tools", "config_serveur.py"), "2"],
               cwd=RACINE, check=True, capture_output=True)
nettoyer_temoins()
os.makedirs(os.path.dirname(TEMOIN_SAUVEGARDE), exist_ok=True)
with open(TEMOIN_SAUVEGARDE, "w", encoding="utf-8") as f:
    json.dump({"temoin": "partie de la place 1"}, f)
with open(TEMOIN_DECK_HOTE, "w", encoding="utf-8") as f:
    json.dump({"name": "temoin de l'hote", "hero": "Spider-Man"}, f)

serveur = subprocess.Popen(
    ["bash", "./launcher-serveur.sh", "2"],
    cwd=RACINE,
    env=dict(os.environ, SANS_TUNNEL="1"),
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    preexec_fn=os.setsid)

try:
    # 1. Les deux moteurs repondent (launcher_fast.py --build-only tourne
    # d'abord : prevoir large avant que les ports repondent).
    for place, port in PORTS.items():
        verifier(f"place {place} : le moteur repond sur {port}", attendre(port))

    if all(ok for _, ok, _ in resultats):
        # 2. Sauvegardes cloisonnees
        sauvegardes_1 = lire(PORTS[1], "/list_replay_files")
        sauvegardes_2 = lire(PORTS[2], "/list_replay_files")
        verifier("la place 1 voit sa sauvegarde",
                 any("zzz-temoin-partie" in c for c in sauvegardes_1), sauvegardes_1)
        verifier("la place 2 ne voit PAS la sauvegarde de la place 1",
                 not any("zzz-temoin-partie" in c for c in sauvegardes_2), sauvegardes_2)

        # 3. Decks de l'hote partages en lecture
        decks_1 = lire(PORTS[1], "/list_deck")
        decks_2 = lire(PORTS[2], "/list_deck")
        verifier("la place 1 voit les decks de l'hote",
                 any("zzz-temoin-hote" in c for c in decks_1), decks_1)
        verifier("la place 2 voit les decks de l'hote",
                 any("zzz-temoin-hote" in c for c in decks_2), decks_2)

        # 4. Ecriture confinee au dossier de la place
        statut, reponse = poster(PORTS[1], "/save_deck", {
            "file_name": "zzz-temoin-ecriture",
            "deck": {"name": "temoin ecriture", "hero": "Spider-Man"}})
        verifier("la place 1 peut enregistrer un deck", statut == 200, reponse)
        verifier("le deck atterrit chez la place 1", os.path.exists(DECK_ECRIT))
        verifier("le deck n'atterrit PAS chez l'hote", not os.path.exists(DECK_ECRIT_CHEZ_HOTE))
finally:
    os.killpg(os.getpgid(serveur.pid), signal.SIGTERM)
    serveur.wait(timeout=30)
    nettoyer_temoins()

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
