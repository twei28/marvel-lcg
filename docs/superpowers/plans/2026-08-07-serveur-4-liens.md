# Serveur 4 liens : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permettre à quatre amis de jouer chacun leur partie Marvel Champions classique, par un lien, tant que le PC hôte fait tourner un lanceur.

**Architecture:** Le moteur est mono-partie, donc une place égale un processus. Un générateur Python dérive quatre configurations de `launch.json` (ports 2351 à 2354, dossiers de sauvegarde et de decks séparés), un script bash démarre les moteurs et un tunnel Cloudflare par moteur, et un `.bat` sert d'entrée Windows. Aucun fichier du moteur n'est modifié.

**Tech Stack:** Python 3.10 (`~/marvel-work/python/bin/python3.10`), bash, cloudflared, aiohttp côté moteur.

**Spec:** `docs/superpowers/specs/2026-08-07-serveur-4-liens-design.md`

## Global Constraints

- Racine du jeu : `Fusion/marvel-lcg-src/`. Tous les chemins relatifs des configurations se résolvent depuis ce dossier, c'est le répertoire courant du moteur.
- Python à utiliser : `~/marvel-work/python/bin/python3.10`. Jamais le `python3` du système.
- cloudflared : `~/marvel-work/tools/cloudflared`.
- Ports imposés : place N égale port `2350 + N`, soit 2351 à 2354. Ne jamais toucher à 2345 (solo) ni à 2347 (multi).
- Aucun fichier sous `Fusion/marvel-lcg-src/src/` ne doit être modifié. Si une tâche semble l'exiger, c'est que la tâche est mal comprise : s'arrêter et le signaler.
- Les commentaires et messages sont en français, sans accents dans les scripts shell (le reste du dépôt fait ainsi, pour éviter les soucis d'encodage sous Windows).
- Les tests sont des scripts autonomes lancés à la main, sur le modèle de `Fusion/marvel-lcg-src/tools/test_salon.py`. Pas de pytest dans ce dépôt.

## Structure des fichiers

| Fichier | Responsabilité |
|---|---|
| `Fusion/marvel-lcg-src/tools/config_serveur.py` | Dériver une configuration par place depuis `launch.json`, créer les dossiers. Seul endroit qui connaît les ports et les chemins. |
| `Fusion/marvel-lcg-src/tools/test_config_serveur.py` | Tester le générateur, sans démarrer aucun moteur. |
| `Fusion/marvel-lcg-src/launcher-serveur.sh` | Démarrer les moteurs et les tunnels, afficher les liens, tout couper à la sortie. Ne connaît aucun chemin de configuration : il appelle le générateur. |
| `Fusion/marvel-lcg-src/tools/test_serveur_multi.py` | Vérifier l'isolement pour de vrai, deux moteurs démarrés par le lanceur. |
| `JOUER-SERVEUR.bat` | Entrée Windows, sur le modèle de `JOUER-EN-MULTI.bat`. |
| `.gitignore` | Ignorer les dossiers et fichiers engendrés par le mode serveur. |

---

### Task 1: Générateur de configurations

**Files:**
- Create: `Fusion/marvel-lcg-src/tools/config_serveur.py`
- Test: `Fusion/marvel-lcg-src/tools/test_config_serveur.py`

**Interfaces:**
- Consumes: rien.
- Produces:
  - `construire_config(base: dict, place: int) -> dict` : rend une NOUVELLE configuration pour la place donnée (1 à 4), sans modifier `base`. Lève `ValueError` si `place` sort de 1 à 4.
  - `ecrire_configs(racine: str, nb_places: int) -> list[str]` : lit `<racine>/launch.json`, crée les dossiers nécessaires, écrit `<racine>/.serveur/launch-N.json` pour N de 1 à `nb_places`, et rend la liste des chemins écrits dans l'ordre. Lève `ValueError` si `nb_places` sort de 1 à 4.
  - `PORT_BASE = 2350` : la place N écoute sur `PORT_BASE + N`.

- [ ] **Step 1: Écrire le test qui échoue**

Créer `Fusion/marvel-lcg-src/tools/test_config_serveur.py` :

```python
"""Verifie la generation des configurations du mode serveur.

Ne demarre AUCUN moteur : ce test lit launch.json, appelle le generateur et
regarde ce qui sort. Il ecrit dans un dossier temporaire, jamais dans le
dossier de jeu.

Usage: python3.10 tools/test_config_serveur.py
"""
import json
import os
import shutil
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "tools"))

from config_serveur import PORT_BASE, construire_config, ecrire_configs

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), str(detail)))


BASE = json.load(open(os.path.join(RACINE, "launch.json"), encoding="utf-8"))

# --- Cas nominal : ce qui change, place par place ---
for place in (1, 2, 3, 4):
    cfg = construire_config(BASE, place)
    port = PORT_BASE + place
    verifier(f"place {place} : port {port}",
             cfg["server_addresses"] == [f"127.0.0.1:{port}"],
             cfg["server_addresses"])
    verifier(f"place {place} : sauvegardes separees",
             cfg["replay_folders"] == [f"../replays/serveur-{place}/"],
             cfg["replay_folders"])
    verifier(f"place {place} : historique separe",
             cfg["games_history_file"] == f"../games_history-serveur-{place}.json",
             cfg["games_history_file"])
    verifier(f"place {place} : statistiques separees",
             cfg["game_statistics_file"] == f"../statistics-serveur-{place}.json",
             cfg["game_statistics_file"])
    verifier(f"place {place} : ecrit ses decks chez lui, lit ceux de l'hote",
             cfg["deck_folders"] == [f"./deck/serveur-{place}/", "./deck/custom/"],
             cfg["deck_folders"])
    verifier(f"place {place} : aucun mot de passe d'entree",
             cfg["password"] == "", cfg["password"])
    verifier(f"place {place} : aucun siege reserve",
             cfg["seat_passwords"] == [], cfg["seat_passwords"])

# --- Ce qui doit rester herite de launch.json ---
cfg = construire_config(BASE, 1)
verifier("images heritees", cfg["image_folders"] == BASE["image_folders"], cfg["image_folders"])
verifier("catalogue herite",
         cfg["cards_json_custom_file"] == BASE["cards_json_custom_file"],
         cfg["cards_json_custom_file"])
verifier("decks de depart herites",
         cfg["starter_deck_folder"] == BASE["starter_deck_folder"],
         cfg["starter_deck_folder"])

# --- La base ne doit pas etre abimee au passage ---
verifier("launch.json d'origine intact",
         BASE["server_addresses"] == ["127.0.0.1:2345"],
         BASE["server_addresses"])

# --- Cas limites : places hors bornes ---
for mauvaise in (0, 5, -1):
    try:
        construire_config(BASE, mauvaise)
        verifier(f"place {mauvaise} refusee", False, "aucune erreur levee")
    except ValueError:
        verifier(f"place {mauvaise} refusee", True)

# --- Ecriture reelle, dans un bac a sable ---
bac = tempfile.mkdtemp(prefix="test-config-serveur-")
try:
    shutil.copy(os.path.join(RACINE, "launch.json"), os.path.join(bac, "launch.json"))
    chemins = ecrire_configs(bac, 2)
    verifier("deux configurations ecrites", len(chemins) == 2, chemins)
    verifier("chemin attendu pour la place 1",
             chemins[0] == os.path.join(bac, ".serveur", "launch-1.json"), chemins[0])
    verifier("configuration relisible",
             json.load(open(chemins[1], encoding="utf-8"))["server_addresses"] == ["127.0.0.1:2352"])
    verifier("dossier de decks de la place 1 cree",
             os.path.isdir(os.path.join(bac, "deck", "serveur-1")))
    verifier("dossier de sauvegardes de la place 2 cree",
             os.path.isdir(os.path.join(bac, "..", "replays", "serveur-2")))
    verifier("place 3 non demandee, donc non creee",
             not os.path.exists(os.path.join(bac, ".serveur", "launch-3.json")))
    try:
        ecrire_configs(bac, 9)
        verifier("nb_places 9 refuse", False, "aucune erreur levee")
    except ValueError:
        verifier("nb_places 9 refuse", True)
finally:
    shutil.rmtree(bac, ignore_errors=True)
    shutil.rmtree(os.path.join(os.path.dirname(bac), "replays", "serveur-1"), ignore_errors=True)
    shutil.rmtree(os.path.join(os.path.dirname(bac), "replays", "serveur-2"), ignore_errors=True)

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
```

- [ ] **Step 2: Lancer le test pour le voir échouer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_config_serveur.py
```

Attendu : `ModuleNotFoundError: No module named 'config_serveur'`.

- [ ] **Step 3: Écrire le générateur**

Créer `Fusion/marvel-lcg-src/tools/config_serveur.py` :

```python
"""Genere une configuration de moteur par place, pour le mode serveur.

Le moteur est mono-partie : une place egale un processus, donc un port et des
dossiers a lui. Tout ce qui distingue les places est ICI, nulle part ailleurs.

Ce qui est SEPARE par place : le port, les sauvegardes, l'historique, les
statistiques, et le dossier ou l'ami enregistre ses decks.
Ce qui reste COMMUN : les images, les sons, le catalogue de cartes, les decks
de depart, et les decks de l'hote (lus, jamais ecrits).

Usage: python3.10 tools/config_serveur.py <nb_places>
"""
import json
import os
import sys

PORT_BASE = 2350
PLACES_MAX = 4


def construire_config(base: dict, place: int) -> dict:
    if not isinstance(place, int) or place < 1 or place > PLACES_MAX:
        raise ValueError(f"Place hors bornes : {place} (attendu 1 a {PLACES_MAX})")
    cfg = json.loads(json.dumps(base))  # copie profonde, la base reste intacte
    cfg["server_addresses"] = [f"127.0.0.1:{PORT_BASE + place}"]
    cfg["replay_folders"] = [f"../replays/serveur-{place}/"]
    cfg["games_history_file"] = f"../games_history-serveur-{place}.json"
    cfg["game_statistics_file"] = f"../statistics-serveur-{place}.json"
    # L'ordre compte : le moteur ECRIT dans deck_folders[0] et LIT toute la
    # liste (server_get.py, save_deck et list_deck). L'ami construit donc ses
    # decks chez lui et voit ceux de l'hote, sans pouvoir les abimer.
    cfg["deck_folders"] = [f"./deck/serveur-{place}/", "./deck/custom/"]
    cfg["password"] = ""
    cfg["seat_passwords"] = []
    return cfg


def ecrire_configs(racine: str, nb_places: int) -> list:
    if not isinstance(nb_places, int) or nb_places < 1 or nb_places > PLACES_MAX:
        raise ValueError(f"Nombre de places hors bornes : {nb_places} (attendu 1 a {PLACES_MAX})")
    base = json.load(open(os.path.join(racine, "launch.json"), encoding="utf-8"))
    dossier_configs = os.path.join(racine, ".serveur")
    os.makedirs(dossier_configs, exist_ok=True)
    chemins = []
    for place in range(1, nb_places + 1):
        cfg = construire_config(base, place)
        # Les chemins de la configuration sont relatifs a la racine du jeu :
        # c'est de la que le moteur tourne.
        for relatif in cfg["replay_folders"] + [cfg["deck_folders"][0]]:
            os.makedirs(os.path.normpath(os.path.join(racine, relatif)), exist_ok=True)
        chemin = os.path.join(dossier_configs, f"launch-{place}.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        chemins.append(chemin)
    return chemins


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        nb = int(sys.argv[1]) if len(sys.argv) > 1 else PLACES_MAX
    except ValueError:
        print(f"Nombre de places invalide : {sys.argv[1]}", file=sys.stderr)
        sys.exit(2)
    try:
        for chemin in ecrire_configs(racine, nb):
            print(chemin)
    except ValueError as erreur:
        print(str(erreur), file=sys.stderr)
        sys.exit(2)
```

- [ ] **Step 4: Lancer le test et le voir passer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_config_serveur.py
```

Attendu : `N/N verifications passees` et code de sortie 0.

- [ ] **Step 5: Vérifier à la main que la sortie est lisible**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/config_serveur.py 2
cat .serveur/launch-1.json
~/marvel-work/python/bin/python3.10 tools/config_serveur.py 9 ; echo "code de sortie : $?"
```

Attendu : deux chemins affichés, un JSON avec le port 2351, puis un message d'erreur clair et le code 2.

- [ ] **Step 6: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add -f Fusion/marvel-lcg-src/tools/config_serveur.py Fusion/marvel-lcg-src/tools/test_config_serveur.py
git commit -m "feat(serveur): deriver une configuration de moteur par place"
```

---

### Task 2: Lanceur des moteurs et des tunnels

**Files:**
- Create: `Fusion/marvel-lcg-src/launcher-serveur.sh`
- Read for reference: `Fusion/marvel-lcg-src/launcher-multi.sh`

**Interfaces:**
- Consumes: `tools/config_serveur.py` en ligne de commande, `python3.10 tools/config_serveur.py <nb>`, qui écrit `.serveur/launch-N.json`.
- Produces:
  - `./launcher-serveur.sh [nb_places]` avec `nb_places` de 1 à 4, 4 par défaut. Code de sortie 2 si l'argument est invalide, 1 si aucune place n'a pu s'ouvrir, 0 sinon.
  - Variable d'environnement `SANS_TUNNEL=1` : démarre les moteurs sans ouvrir de tunnel et affiche les adresses locales. C'est ce que la Task 3 utilise pour tester.
  - Journaux : `/tmp/marvel-serveur-N.log` par moteur.

- [ ] **Step 1: Écrire le lanceur**

Créer `Fusion/marvel-lcg-src/launcher-serveur.sh` :

```bash
#!/usr/bin/env bash
# Lanceur "serveur" : N moteurs INDEPENDANTS derriere N tunnels, pour que des
# amis jouent CHACUN leur partie classique tant que ce script tourne.
# Rien a voir avec launcher-multi.sh : ici, aucune partie n'est partagee.
# Ctrl+C ferme tout : les liens ne fonctionnent plus.
set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$HOME/marvel-work/python/bin/python3.10}"
CLOUDFLARED="${CLOUDFLARED:-$HOME/marvel-work/tools/cloudflared}"
# SANS_TUNNEL=1 : moteurs seuls, adresses locales. Sert aux tests.
SANS_TUNNEL="${SANS_TUNNEL:-0}"
PORT_BASE=2350

NB_PLACES="${1:-4}"
case "$NB_PLACES" in
  1|2|3|4) ;;
  *) echo "Nombre de places invalide : '$NB_PLACES'. Attendu 1, 2, 3 ou 4." >&2; exit 2 ;;
esac

[ -x "$PYTHON" ] || { echo "Introuvable ou non executable : $PYTHON" >&2; exit 1; }
if [ "$SANS_TUNNEL" != "1" ]; then
  [ -x "$CLOUDFLARED" ] || { echo "Introuvable ou non executable : $CLOUDFLARED" >&2; exit 1; }
fi

cd "$RACINE"
"$PYTHON" tools/config_serveur.py "$NB_PLACES" >/dev/null || {
  echo "Generation des configurations impossible." >&2; exit 1; }

PIDS=()
JOURNAUX_TUNNEL=()
LIENS=()

nettoyer() {
  echo
  echo "Fermeture du serveur..."
  for pid in "${PIDS[@]:-}"; do
    [ -n "$pid" ] && kill "$pid" 2>/dev/null
  done
  wait 2>/dev/null
  for journal in "${JOURNAUX_TUNNEL[@]:-}"; do
    [ -n "$journal" ] && rm -f "$journal"
  done
  echo "Moteurs arretes, tunnels fermes. Les liens ne fonctionnent plus."
}
trap nettoyer EXIT INT TERM

for place in $(seq 1 "$NB_PLACES"); do
  port=$((PORT_BASE + place))
  journal_jeu="/tmp/marvel-serveur-$place.log"
  echo "Place $place : demarrage du moteur sur le port $port..."
  # PYTHONUNBUFFERED : sans lui, Python tamponne sa sortie des qu'elle n'est
  # plus un terminal, et le journal reste vide au moment ou l'on en a besoin.
  PYTHONUNBUFFERED=1 "$PYTHON" -u launcher_fast.py --config ".serveur/launch-$place.json" \
    >"$journal_jeu" 2>&1 &
  pid_jeu=$!
  PIDS+=("$pid_jeu")

  pret=0
  for _ in $(seq 1 240); do
    curl -s -o /dev/null "http://127.0.0.1:$port/" && { pret=1; break; }
    kill -0 "$pid_jeu" 2>/dev/null || break
    sleep 1
  done
  if [ "$pret" != "1" ]; then
    echo "Place $place : le moteur n'a pas demarre. Voir $journal_jeu" >&2
    continue
  fi

  if [ "$SANS_TUNNEL" = "1" ]; then
    LIENS+=("Place $place : http://127.0.0.1:$port/prepare.html")
    continue
  fi

  journal_tunnel="$(mktemp)"
  JOURNAUX_TUNNEL+=("$journal_tunnel")
  "$CLOUDFLARED" tunnel --url "http://127.0.0.1:$port" --no-autoupdate \
    >"$journal_tunnel" 2>&1 &
  PIDS+=("$!")
  url=""
  for _ in $(seq 1 60); do
    url="$(grep -oE 'https://[-a-z0-9]+\.trycloudflare\.com' "$journal_tunnel" | head -1)"
    [ -n "$url" ] && break
    sleep 1
  done
  if [ -z "$url" ]; then
    echo "Place $place : tunnel non etabli, cette place restera locale." >&2
    continue
  fi
  LIENS+=("Place $place : $url/prepare.html")
done

# Degradation choisie : trois liens valent mieux que zero. On ne s'arrete que
# si AUCUNE place n'a pu s'ouvrir.
if [ "${#LIENS[@]}" -eq 0 ]; then
  echo "Aucune place n'a pu s'ouvrir. Rien a partager." >&2
  exit 1
fi

MESSAGE="Marvel Champions, sers-toi !
Ouvre TON lien, cree ta partie, joue quand tu veux.
$(printf '%s\n' "${LIENS[@]}")
(le lien ne marche que tant que mon PC tourne)"

COPIE=""
if command -v clip.exe >/dev/null 2>&1; then
  printf '%s' "$MESSAGE" | clip.exe 2>/dev/null && \
    COPIE="   (message deja copie : Ctrl+V dans Discord ou WhatsApp)"
fi

cat <<INFOS

==============================================================
   SERVEUR PRET  (${#LIENS[@]} place(s) sur $NB_PLACES)
==============================================================

$(printf '   %s\n' "${LIENS[@]}")

$COPIE

   Un lien par personne : deux personnes sur le meme lien
   jouent la MEME partie et se genent.

   Journaux des moteurs : /tmp/marvel-serveur-N.log
   Ctrl+C ici = fin pour tout le monde.
==============================================================

INFOS

wait
```

- [ ] **Step 2: Rendre le script exécutable et vérifier les cas limites**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
chmod +x launcher-serveur.sh
bash -n launcher-serveur.sh && echo "syntaxe OK"
./launcher-serveur.sh 5 ; echo "code de sortie : $?"
./launcher-serveur.sh 0 ; echo "code de sortie : $?"
./launcher-serveur.sh deux ; echo "code de sortie : $?"
```

Attendu : `syntaxe OK`, puis trois fois un message `Nombre de places invalide` et le code 2.

- [ ] **Step 3: Fumée sur une seule place, sans tunnel**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
SANS_TUNNEL=1 ./launcher-serveur.sh 1 &
sleep 45
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:2351/prepare.html
kill %1
```

Attendu : `200`. Si le code est autre chose, lire `/tmp/marvel-serveur-1.log` avant toute autre action : c'est le moteur qui parle, pas le lanceur.

- [ ] **Step 4: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add -f Fusion/marvel-lcg-src/launcher-serveur.sh
git commit -m "feat(serveur): lancer N moteurs independants et leurs tunnels"
```

---

### Task 3: Test d'isolement réel

**Files:**
- Create: `Fusion/marvel-lcg-src/tools/test_serveur_multi.py`

**Interfaces:**
- Consumes: `./launcher-serveur.sh 2` avec `SANS_TUNNEL=1`, les ports 2351 et 2352, et les routes HTTP du moteur : `GET /list_replay_files`, `GET /list_deck`, `POST /save_deck`.
- Produces: rien que d'autres tâches consomment.

C'est le test qui compte. Une configuration approximative donnerait deux moteurs partageant le même dossier de sauvegardes, sans que personne ne s'en aperçoive avant qu'une partie soit écrasée.

- [ ] **Step 1: Écrire le test**

Créer `Fusion/marvel-lcg-src/tools/test_serveur_multi.py` :

```python
"""Verifie l'ISOLEMENT du mode serveur, avec deux vrais moteurs.

Ce que ce test prouve :
  1. les deux moteurs repondent, chacun sur son port ;
  2. une sauvegarde de la place 1 n'apparait PAS chez la place 2 ;
  3. un deck de l'hote apparait chez les DEUX ;
  4. un deck enregistre depuis la place 1 atterrit chez elle, pas chez l'hote.

Les fichiers temoins sont crees AVANT le demarrage des moteurs : le moteur
sert des listes avec un cache, et un fichier depose apres coup pourrait ne pas
apparaitre tout de suite.

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
TEMOIN_SAUVEGARDE = os.path.normpath(
    os.path.join(RACINE, "..", "replays", "serveur-1", "zzz-temoin-partie.json"))
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
    ["./launcher-serveur.sh", "2"],
    cwd=RACINE,
    env=dict(os.environ, SANS_TUNNEL="1"),
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    preexec_fn=os.setsid)

try:
    # 1. Les deux moteurs repondent
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
```

- [ ] **Step 2: Lancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_serveur_multi.py
```

Attendu : `9/9 verifications passees`. Le test met une à deux minutes, le temps que deux moteurs chargent le catalogue.

Si une vérification échoue, ne pas corriger le test : lire `/tmp/marvel-serveur-1.log` et `/tmp/marvel-serveur-2.log`, et comparer `.serveur/launch-1.json` et `.serveur/launch-2.json`. Un test rouge ici veut dire que l'isolement est réellement cassé.

- [ ] **Step 3: Vérifier qu'aucun processus ne traîne**

```bash
ss -lptn | grep -E ':2351|:2352' ; echo "---"
pgrep -fa launcher_fast.py
```

Attendu : les deux commandes ne renvoient rien. Si un moteur traîne, le test n'a pas nettoyé et il faut corriger le bloc `finally` avant de continuer.

- [ ] **Step 4: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add -f Fusion/marvel-lcg-src/tools/test_serveur_multi.py
git commit -m "test(serveur): prouver l'isolement des sauvegardes et des decks"
```

---

### Task 4: Entrée Windows, dépôt propre, et mesure de la charge

**Files:**
- Create: `JOUER-SERVEUR.bat`
- Modify: `.gitignore`
- Read for reference: `JOUER-EN-MULTI.bat`

**Interfaces:**
- Consumes: `Fusion/marvel-lcg-src/launcher-serveur.sh`.
- Produces: rien que d'autres tâches consomment. C'est la dernière.

- [ ] **Step 1: Créer l'entrée Windows**

Créer `JOUER-SERVEUR.bat`, en calquant `JOUER-EN-MULTI.bat` :

```bat
@echo off
title Marvel Champions - serveur pour les amis
echo Demarrage du serveur...
echo (laisse cette fenetre ouverte : les liens ne marchent que pendant ce temps)
echo.
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && ./launcher-serveur.sh"
echo.
echo Serveur arrete.
pause
```

- [ ] **Step 2: Ignorer ce que le mode serveur engendre**

Ajouter à la fin de `.gitignore` :

```
Fusion/marvel-lcg-src/.serveur/
Fusion/marvel-lcg-src/deck/serveur-*/
Fusion/replays/serveur-*/
Fusion/games_history-serveur-*.json
Fusion/statistics-serveur-*.json
```

- [ ] **Step 3: Mesurer ce que quatre places coûtent**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
SANS_TUNNEL=1 ./launcher-serveur.sh 4 &
sleep 120
ps -o rss=,comm= -C python3.10 | awk '{somme += $1} END {printf "RAM totale des moteurs : %.0f Mo\n", somme/1024}'
free -m | head -2
kill %1
```

Noter le chiffre et le rapporter à l'utilisateur. S'il dépasse la moitié de la RAM disponible, lui dire que `./launcher-serveur.sh 2` est le réglage raisonnable chez lui, et pourquoi.

- [ ] **Step 4: Essai complet avec tunnels, une seule place**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
./launcher-serveur.sh 1
```

Attendu : l'encadré `SERVEUR PRET (1 place(s) sur 1)` avec un lien `https://….trycloudflare.com/prepare.html`. Ouvrir ce lien dans un navigateur, vérifier que l'assistant de création de partie s'affiche, puis Ctrl+C et vérifier que le lien ne répond plus.

Ne pas cocher cette étape sans avoir réellement ouvert le lien dans un navigateur.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add JOUER-SERVEUR.bat .gitignore
git commit -m "feat(serveur): entree Windows et depot propre"
```

---

## Ce que le plan ne fait pas

- Aucun mot de passe, c'est la décision de la spec. Remplir le champ `password` dans `config_serveur.py` n'aurait de toute façon aucun effet : `launcher_fast.py` fait `WebServer.IsAuthenticate = lambda self, request=None: True`, qui court-circuite le contrôle du mot de passe (`src/engine/network/web_server.py`). Rendre un mot de passe possible demanderait de revoir `launcher_fast.py`, un autre chantier.
- Aucune adresse fixe : les liens changent à chaque lancement.
- Aucun garde-fou contre deux personnes sur le même lien. C'est une convention, pas une contrainte technique.
- Aucun mode d'emploi écrit : le lanceur affiche tout à l'écran.

---

## Amendement du 2026-08-07 : le moteur n'écoutait pas `--config`

Découvert pendant la Task 2, et validé avec l'utilisateur.

`launcher_fast.py` copie **toujours** `launch.json` dans `.game/`, puis démarre depuis `.game/`. L'option `--config` n'existe pas : elle est avalée sans effet, le moteur attendant `-config_files` (un seul tiret). Le mode multi souffre du même défaut depuis toujours : `launcher-multi.sh` attend le port 2347 alors que le moteur démarre sur 2345.

Deux conséquences pour ce plan, qui remplacent ce qui est écrit plus haut.

### 1. `launcher_fast.py` apprend deux options

Modifier `Fusion/marvel-lcg-src/launcher_fast.py` (hors `src/`, donc autorisé) :

- `--config <fichier>` : copier CE fichier vers `.game/launch.json` au lieu de `launch.json`. Chemin relatif à la racine du jeu. Fichier absent égale erreur claire et arrêt.
- `--no-browser` : ne pas lancer le fil qui ouvre le navigateur. Sans lui, chaque moteur ouvrirait une fenêtre, soit quatre fenêtres pour quatre places.

Ces deux options sont inertes quand elles ne sont pas passées : le mode solo et le mode multi gardent exactement leur comportement actuel. Le mode solo doit être vérifié après la modification.

### 2. Les chemins relatifs se résolvent depuis `.game/`, pas depuis la racine

Le moteur fait `os.chdir(.game)` avant de démarrer. Un `"../replays/serveur-1/"` dans la configuration désigne donc `Fusion/marvel-lcg-src/replays/serveur-1/`, et non `Fusion/replays/serveur-1/`. C'est d'ailleurs pour cela que `Fusion/marvel-lcg-src/replays/` existe et que `Fusion/replays/` n'existe pas.

Les valeurs écrites dans les configurations ne changent pas. Ce qui change, c'est `ecrire_configs` dans `tools/config_serveur.py` : les dossiers doivent être créés sous `<racine>/.game/`, pas sous `<racine>/`. Le test `tools/test_config_serveur.py` doit être corrigé en conséquence, et la Global Constraint « les chemins relatifs se résolvent depuis la racine du jeu » est remplacée par « depuis `<racine>/.game/` ».

Les dossiers `Fusion/replays/serveur-*/` créés au mauvais endroit pendant la Task 1 sont à supprimer.

### Ce que le plan ne fait toujours pas

`launcher-multi.sh` n'est pas réparé ici, mais la correction de `launcher_fast.py` lui rend l'option `--config` fonctionnelle. Il faudra le vérifier lors d'une prochaine partie multi.
