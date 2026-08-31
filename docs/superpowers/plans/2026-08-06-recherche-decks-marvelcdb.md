# Recherche de decks MarvelCDB — plan d'implémentation

> **Pour un agent exécutant :** SOUS-COMPÉTENCE REQUISE : utiliser `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les étapes sont des cases à cocher (`- [ ]`).

**Objectif :** permettre de choisir, depuis l'écran de préparation, n'importe quel deck publié sur MarvelCDB pour le héros déjà sélectionné, sans internet au moment de la partie.

**Architecture :** un indexeur Python aspire l'historique de `by_date` et écrit un fichier par héros dans `data/marvelcdb/` ; un module JavaScript pur (chargement, filtres, favoris, conversion) lit ces fichiers via `/read_file` ; l'assistant de préparation ouvre un panneau qui consomme ce module. L'indexeur et le module survivront à la refonte React de l'écran de préparation ; seul le panneau est jetable.

**Pile technique :** Python 3.10 (bibliothèque standard uniquement, `urllib`), modules ES servis tels quels (pas de build), tests Node en `.mjs` sans framework, tests Python en script autonome sans framework.

**Spec de référence :** `.planning/todos/2026-07-28-recherche-decks-marvelcdb.md`. Le présent plan la suit, avec quatre écarts constatés en relisant le code aujourd'hui, listés en fin de document (§ Écarts à la spec).

## Contraintes globales

- **Ne jamais modifier le moteur** (`src/`) ni `public/js/marvel/`. Rien dans ce plan n'y touche.
- **Copie vivante = `~/marvel-work/fusion/marvel-lcg-src`** (dite ①). C'est là qu'on édite. Le miroir Windows `Jeu Marvel Champions/Fusion/marvel-lcg-src` (dit ②) est celui que lance `JOUER-EN-MULTI.bat` : il doit recevoir chaque changement. Voir GUIDE-CREATION-CONTENU.md §1.1 à §1.3.
- **`deployer.sh` synchronise `public/js` et `public/css` de ① vers ②, mais PAS `data/`.** La propagation de l'index se fait par le `rsync -a "$S/data/" "$M/data/"` du guide §1.3.
- **Le serveur lit depuis `.game/`, pas depuis la racine.** Dans ②, `.game/data` est un lien symbolique vers `data` : rien à faire. Dans ①, `.game/data` est une **copie figée au 4 août** : l'index n'y apparaîtrait jamais. L'indexeur doit rendre `data/marvelcdb` visible depuis `.game/data` (tâche 2, `publier_vers_game`).
- **Python : `~/marvel-work/python/bin/python3.10`.** Aucune dépendance nouvelle : `urllib.request` seulement, jamais `requests`.
- **Node est le binaire Windows** : il ne lit pas les chemins WSL. Les tests `.mjs` importent la copie ② par chemin relatif, comme `outils/verifier-salon-etat.mjs`. Un test lancé avant la synchro vers ② teste l'ancienne version : **toujours synchroniser avant de tester**.
- **Bilingue obligatoire** : toute chaîne française nouvelle passe par `t("...")` et reçoit son entrée dans `public/js/prepare/dico-en.js`. Une chaîne sans traduction s'affiche en français dans l'interface anglaise, sans erreur : c'est silencieux, donc à vérifier à l'œil.
- **Les fichiers du jeu vivent hors du dépôt git.** Les étapes « commit » ne portent que sur ce qui est suivi : `outils/*.mjs`, `docs/`, `.planning/`. La sauvegarde des fichiers du jeu, c'est la synchro vers ②. Voir la question ouverte en fin de plan.
- **Aucune route serveur nouvelle.** `/read_file?<chemin>` sert déjà n'importe quel JSON du dossier de jeu, gzippé (`src/engine/device/web/server/server_get.py:158`). Le chemin est résolu depuis le répertoire courant du moteur, c'est-à-dire `.game/`.

---

## Structure des fichiers

| Fichier | Responsabilité |
|---|---|
| `①/tools/marvelcdb_index.py` | **[A]** Aspiration incrémentale, regroupement par héros, calcul de jouabilité, écriture de l'index, publication vers `.game`. Aucun import du moteur. |
| `①/tools/test_marvelcdb_index.py` | Test de [A] **sans réseau** : la fonction d'aspiration est injectée. |
| `①/public/js/marvelcdb/index.js` | **[B]** `chargerHeros(heroCode)` : lit `/read_file?data/marvelcdb/<code>.json`, mémorise pour la session. |
| `①/public/js/marvelcdb/filtres.js` | **[B]** `filtrer(decks, criteres)` : fonction pure, tri chronologique décroissant. |
| `①/public/js/marvelcdb/favoris.js` | **[B]** Favoris dans `localStorage`, stockage injectable pour les tests. |
| `①/public/js/marvelcdb/conversion.js` | **[B]** `versDeckMoteur` et `ecartDeConversion` : entrée d'index → deck moteur. Seule source de la règle de conversion, y compris pour l'import par lien déjà en place. |
| `②/outils/verifier-marvelcdb.mjs` | Test de `filtres.js`, `favoris.js` et `conversion.js`. Suivi par git. |
| `①/public/js/prepare/app.js` | **[C]** Panneau « Decks MarvelCDB » dans l'étape des decks + branchement de l'import existant sur `conversion.js`. |
| `①/public/css/prepare/prepare.css` | **[C]** Styles du panneau (réutilise `.deck-modal` déjà présent). |
| `①/public/js/prepare/dico-en.js` | **[C]** Traductions anglaises des chaînes du panneau. |

---

## Tâche 1 : noyau de l'indexeur, sans réseau

Le cœur calculable de [A] : transformer une journée brute de MarvelCDB en entrées d'index, regrouper par héros, dire si un deck est jouable. Aucune requête, donc entièrement testable.

**Fichiers :**
- Créer : `~/marvel-work/fusion/marvel-lcg-src/tools/marvelcdb_index.py`
- Créer : `~/marvel-work/fusion/marvel-lcg-src/tools/test_marvelcdb_index.py`

**Interfaces :**
- Consomme : rien.
- Produit, pour la tâche 2 :
  - `charger_ids_cartes(racine: str) -> set[str]`
  - `table_deck_starter(racine: str) -> dict[str, str]` — `"13001a" -> "wasp"`
  - `entree_depuis_deck(brut: dict, ids_connus: set[str]) -> dict`
  - `regrouper(bruts: list[dict], ids_connus: set[str], table: dict[str, str]) -> tuple[dict[str, dict], int]` — le `int` est le nombre de decks écartés parce que leur héros est inconnu du jeu.

- [ ] **Étape 1 : écrire le test qui échoue**

Créer `tools/test_marvelcdb_index.py`. Style repris de `tools/test_salon.py` : script autonome, un accumulateur `verifier`, sortie `OK`/`ECHEC`, code de sortie 1 s'il reste un échec.

```python
"""Teste le noyau de l'indexeur MarvelCDB, SANS RESEAU.

Toutes les fonctions visees sont pures : on leur passe des journees figees,
ecrites ici, et un catalogue de cartes reduit. Aucun appel a marvelcdb.com.

Usage: python3.10 tools/test_marvelcdb_index.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marvelcdb_index as idx

resultats = []

def verifier(nom, obtenu, attendu):
    ok = obtenu == attendu
    resultats.append((nom, ok, f"obtenu {obtenu!r}, attendu {attendu!r}"))

# --- Journees figees, au format exact de by_date (verifie le 6/8/2026) -------
DECK_NOVA = {
    "id": 64331, "name": "Nova Justice", "hero_code": "28001a", "hero_name": "Nova",
    "date_creation": "2026-08-01T00:33:02+00:00", "user_id": 77086,
    "meta": '{"aspect":"justice"}', "tags": "solo", "version": "1.0",
    "slots": {"01062": 2, "28002": 1, "99999": 1},
}
DECK_WASP = {
    "id": 64332, "name": "Hives", "hero_code": "13001a", "hero_name": "Wasp",
    "date_creation": "2026-08-01T09:00:00+00:00", "user_id": 42,
    "meta": '{"aspect":"protection","aspect2":"basic"}', "tags": "multiplayer solo",
    "slots": {"01062": 2, "13002": 1},
}
IDS_CONNUS = {"01062", "28002", "13002"}
TABLE = {"28001a": "nova", "13001a": "wasp"}

# --- Aspect, tags -----------------------------------------------------------
e = idx.entree_depuis_deck(DECK_NOVA, IDS_CONNUS)
verifier("aspect lu dans meta", e["aspect"], "justice")
verifier("tags decoupes", idx.entree_depuis_deck(DECK_WASP, IDS_CONNUS)["tags"],
         ["multiplayer", "solo"])
verifier("meta vide ne casse rien",
         idx.entree_depuis_deck({**DECK_NOVA, "meta": ""}, IDS_CONNUS)["aspect"], "")
verifier("tags vides donnent une liste vide",
         idx.entree_depuis_deck({**DECK_NOVA, "tags": ""}, IDS_CONNUS)["tags"], [])

# --- Jouabilite -------------------------------------------------------------
verifier("carte inconnue -> non jouable", e["jouable"], False)
verifier("carte inconnue listee", e["cartes_absentes"], ["99999"])
verifier("toutes cartes connues -> jouable",
         idx.entree_depuis_deck(DECK_WASP, IDS_CONNUS)["jouable"], True)

# --- Champs conserves -------------------------------------------------------
verifier("date reduite au jour", e["date"], "2026-08-01")
verifier("cartes conservees", e["cartes"], {"01062": 2, "28002": 1, "99999": 1})
verifier("id conserve", e["id"], 64331)

# --- Regroupement -----------------------------------------------------------
paquets, ecartes = idx.regrouper([DECK_NOVA, DECK_WASP], IDS_CONNUS, TABLE)
verifier("un paquet par heros", sorted(paquets), ["13001a", "28001a"])
verifier("nom du heros conserve", paquets["28001a"]["hero_name"], "Nova")
verifier("deck starter resolu", paquets["28001a"]["deck_starter"], "nova")
verifier("aucun ecarte", ecartes, 0)

inconnu = {**DECK_NOVA, "id": 1, "hero_code": "77777a"}
paquets2, ecartes2 = idx.regrouper([inconnu], IDS_CONNUS, TABLE)
verifier("heros inconnu du jeu : ecarte", (sorted(paquets2), ecartes2), ([], 1))

# --- Catalogue et table, lus sur de vrais fichiers ---------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data"))
    os.makedirs(os.path.join(tmp, "deck", "starter"))
    json.dump({"pack": [{"card_id": "01001a,01001b"}, {"card_id": "01062"}]},
              open(os.path.join(tmp, "data", "cards.json"), "w", encoding="utf-8"))
    json.dump({"hero": ["13001a,13001b,13001c"]},
              open(os.path.join(tmp, "deck", "starter", "wasp.json"), "w", encoding="utf-8"))
    verifier("ids de cartes, faces separees",
             idx.charger_ids_cartes(tmp), {"01001a", "01001b", "01062"})
    verifier("table deck starter", idx.table_deck_starter(tmp), {"13001a": "wasp"})

for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"   [{detail}]"))
rates = [n for n, ok, _ in resultats if not ok]
print("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)")
sys.exit(0 if not rates else 1)
```

- [ ] **Étape 2 : lancer le test pour le voir échouer**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 tools/test_marvelcdb_index.py
```

Attendu : `ModuleNotFoundError: No module named 'marvelcdb_index'`.

- [ ] **Étape 3 : écrire le noyau**

Créer `tools/marvelcdb_index.py` :

```python
"""Index local des decks MarvelCDB, par heros.

L'API publique de marvelcdb n'a AUCUNE route de recherche : `by_hero`,
`popular`, `hot`, `search` repondent toutes 404 (reverifie le 6/8/2026). La
seule route de liste est `by_date/<AAAA-MM-JJ>.json`, qui rend les decks
publies ce jour-la, CONTENU COMPRIS. D'ou ce script : on aspire l'historique
une fois, on regroupe par heros, et l'ecran de preparation lit des fichiers
locaux. Un deck choisi est alors jouable sans internet.

Aucun import du moteur, bibliotheque standard uniquement.

Usage :
    python3.10 tools/marvelcdb_index.py                 # passage incremental
    python3.10 tools/marvelcdb_index.py --recalculer    # rejoue la jouabilite
    python3.10 tools/marvelcdb_index.py --depuis 2026-01-01 --jusqu-a 2026-01-07
"""
import json
import os

DEBUT_HISTORIQUE = "2019-10-01"   # premiere publication sur marvelcdb


def charger_ids_cartes(racine):
    """Tous les card_id connus du jeu, faces separees.

    cards.json est un dict {nom de pack: [carte, ...]}. Une carte recto-verso
    porte un id compose ("01001a,01001b") : les deux faces comptent, parce
    qu'un deck marvelcdb peut citer l'une ou l'autre.
    """
    ids = set()
    for nom in ("cards.json", "cards_custom.json"):
        chemin = os.path.join(racine, "data", nom)
        if not os.path.exists(chemin):
            continue
        paquets = json.load(open(chemin, encoding="utf-8"))
        for cartes in paquets.values():
            if not isinstance(cartes, list):
                continue
            for carte in cartes:
                brut = str(carte.get("card_id") or "")
                for face in brut.split(","):
                    if face:
                        ids.add(face)
    return ids


def table_deck_starter(racine):
    """« 13001a » -> « wasp », lu dans deck/starter/*.json (champ hero[0])."""
    table = {}
    dossier = os.path.join(racine, "deck", "starter")
    if not os.path.isdir(dossier):
        return table
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith(".json"):
            continue
        try:
            deck = json.load(open(os.path.join(dossier, fichier), encoding="utf-8"))
        except (ValueError, OSError):
            continue
        heros = (deck.get("hero") or [""])[0]
        code = str(heros).split(",")[0]
        if code:
            table[code] = fichier[:-5]
    return table


def _aspect(brut):
    """meta est une CHAINE JSON, pas un objet : '{"aspect":"justice"}'."""
    meta = brut.get("meta")
    if not meta:
        return ""
    try:
        return str(json.loads(meta).get("aspect") or "")
    except ValueError:
        return ""


def _tags(brut):
    """tags est une chaine, separee par des espaces ou des virgules."""
    brut_tags = str(brut.get("tags") or "").replace(",", " ")
    return sorted({t for t in brut_tags.split() if t})


def entree_depuis_deck(brut, ids_connus):
    """Un deck brut de by_date -> une entree d'index."""
    cartes = {str(k): int(v) for k, v in (brut.get("slots") or {}).items()}
    absentes = sorted(c for c in cartes if c not in ids_connus)
    return {
        "id": brut.get("id"),
        "nom": brut.get("name") or "",
        "aspect": _aspect(brut),
        "tags": _tags(brut),
        "date": str(brut.get("date_creation") or "")[:10],
        "auteur": brut.get("user_id"),
        "cartes": cartes,
        "jouable": not absentes,
        "cartes_absentes": absentes,
    }


def regrouper(bruts, ids_connus, table):
    """Regroupe par hero_code. Rend (paquets, nombre de decks ecartes).

    Un deck dont le heros n'existe pas dans le jeu est ecarte : le proposer
    ne menerait qu'a un message d'erreur au lancement.
    """
    paquets = {}
    ecartes = 0
    for brut in bruts:
        code = str(brut.get("hero_code") or "").split(",")[0]
        if not code or code not in table:
            ecartes += 1
            continue
        paquet = paquets.setdefault(code, {
            "hero_code": code,
            "hero_name": brut.get("hero_name") or "",
            "deck_starter": table[code],
            "decks": [],
        })
        paquet["decks"].append(entree_depuis_deck(brut, ids_connus))
    return paquets, ecartes
```

- [ ] **Étape 4 : lancer le test pour le voir passer**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 tools/test_marvelcdb_index.py
```

Attendu : `TOUT PASSE`, 17 lignes `OK`.

- [ ] **Étape 5 : synchroniser vers le miroir ② et commiter ce qui est suivi**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rsync -a "$S/tools/" "$M/tools/"
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add docs/superpowers/plans/2026-08-06-recherche-decks-marvelcdb.md
git commit -m "docs(marvelcdb): plan d'implementation de la recherche de decks"
```

---

## Tâche 2 : aspiration incrémentale, écriture et publication de l'index

**Fichiers :**
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/tools/marvelcdb_index.py`
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/tools/test_marvelcdb_index.py`

**Interfaces :**
- Consomme : `charger_ids_cartes`, `table_deck_starter`, `entree_depuis_deck`, `regrouper` (tâche 1).
- Produit :
  - `jours_a_traiter(derniere_date: str|None, aujourdhui: str, jusqu_a: str|None) -> list[str]`
  - `fusionner(anciennes: list[dict], nouvelles: list[dict]) -> list[dict]` — dédoublonne par `id`, tri par `date` décroissante puis `id` décroissant
  - `aspirer(dates, recuperer, ids_connus, table) -> tuple[dict, list[str], int]` — `recuperer(date) -> list[dict]` est **injecté** ; rend (paquets, jours en erreur, écartés)
  - `ecrire_index(racine, paquets) -> int`
  - `publier_vers_game(racine) -> str` — rend `"lien"`, `"copie"` ou `"rien a faire"`

- [ ] **Étape 1 : ajouter les tests qui échouent**

Insérer dans `tools/test_marvelcdb_index.py`, juste avant la boucle d'affichage finale :

```python
# --- Calendrier -------------------------------------------------------------
verifier("premier passage : depuis le debut de l'historique",
         idx.jours_a_traiter(None, "2019-10-04", None),
         ["2019-10-01", "2019-10-02", "2019-10-03"])
verifier("passage incremental : reprend au lendemain",
         idx.jours_a_traiter("2026-08-01", "2026-08-04", None),
         ["2026-08-02", "2026-08-03"])
verifier("le jour courant n'est jamais aspire (journee incomplete)",
         idx.jours_a_traiter("2026-08-02", "2026-08-03", None), [])
verifier("deja a jour", idx.jours_a_traiter("2026-08-05", "2026-08-03", None), [])
verifier("--jusqu-a borne la plage",
         idx.jours_a_traiter("2026-08-01", "2026-08-10", "2026-08-03"),
         ["2026-08-02", "2026-08-03"])

# --- Fusion -----------------------------------------------------------------
a = {"id": 1, "date": "2026-01-01"}
b = {"id": 2, "date": "2026-02-01"}
b2 = {"id": 2, "date": "2026-02-01", "nom": "renomme"}
verifier("tri par date decroissante", [d["id"] for d in idx.fusionner([a], [b])], [2, 1])
verifier("dedoublonnage par id, la nouvelle version gagne",
         idx.fusionner([b], [b2]), [b2])

# --- Aspiration, avec une fonction de recuperation INJECTEE -----------------
appels = []

def faux_recuperer(date):
    appels.append(date)
    if date == "2026-08-02":
        raise OSError("marvelcdb injoignable")
    return [DECK_NOVA] if date == "2026-08-01" else [DECK_WASP]

paquets3, en_erreur, ecartes3 = idx.aspirer(
    ["2026-08-01", "2026-08-02", "2026-08-03"], faux_recuperer, IDS_CONNUS, TABLE)
verifier("un jour en erreur n'interrompt rien", sorted(paquets3), ["13001a", "28001a"])
verifier("le jour en erreur est journalise", en_erreur, ["2026-08-02"])
verifier("le jour en erreur est reessaye une fois",
         appels.count("2026-08-02"), 2)

# --- Ecriture ---------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data"))
    n = idx.ecrire_index(tmp, paquets3)
    verifier("un fichier par heros", n, 2)
    ecrit = json.load(open(os.path.join(tmp, "data", "marvelcdb", "28001a.json"),
                          encoding="utf-8"))
    verifier("format du fichier heros",
             (ecrit["hero_code"], ecrit["deck_starter"], len(ecrit["decks"])),
             ("28001a", "nova", 1))

    # Second passage : le fichier existant est FUSIONNE, pas ecrase.
    autre = {"28001a": {"hero_code": "28001a", "hero_name": "Nova", "deck_starter": "nova",
                        "decks": [idx.entree_depuis_deck({**DECK_NOVA, "id": 99}, IDS_CONNUS)]}}
    idx.ecrire_index(tmp, autre)
    relu = json.load(open(os.path.join(tmp, "data", "marvelcdb", "28001a.json"),
                          encoding="utf-8"))
    verifier("second passage : fusion, pas ecrasement",
             sorted(d["id"] for d in relu["decks"]), [99, 64331])

# --- Publication vers .game -------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data", "marvelcdb"))
    os.makedirs(os.path.join(tmp, ".game", "data"))      # copie reelle, cas WSL
    verifier("copie reelle : marvelcdb devient visible",
             idx.publier_vers_game(tmp), "lien")
    verifier("visible depuis .game",
             os.path.isdir(os.path.join(tmp, ".game", "data", "marvelcdb")), True)

with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data", "marvelcdb"))
    os.makedirs(os.path.join(tmp, ".game"))
    os.symlink(os.path.join(tmp, "data"), os.path.join(tmp, ".game", "data"))
    verifier("lien symbolique deja en place : rien a faire",
             idx.publier_vers_game(tmp), "rien a faire")
```

- [ ] **Étape 2 : lancer le test pour le voir échouer**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 tools/test_marvelcdb_index.py
```

Attendu : `AttributeError: module 'marvelcdb_index' has no attribute 'jours_a_traiter'`.

- [ ] **Étape 3 : écrire l'aspiration, l'écriture et la publication**

D'abord l'en-tête d'imports du fichier, qui passe de :

```python
import json
import os
```

à :

```python
import datetime
import json
import os
import shutil
import sys
import time
import urllib.request
```

Puis, après `regrouper` :

```python
URL_JOUR = "https://marvelcdb.com/api/public/decklists/by_date/{}.json"
AGENT = "marvel-lcg-local/1.0 (index de decks hors ligne, usage personnel)"
DELAI = 0.2          # seconde entre deux requetes : on ne martele pas le site


def jours_a_traiter(derniere_date, aujourdhui, jusqu_a=None):
    """Jours restant a aspirer, bornes incluses.

    Le jour courant est volontairement exclu : sa journee n'est pas finie, et
    l'aspirer figerait un total partiel qu'aucun passage suivant ne reprendrait.
    """
    debut = DEBUT_HISTORIQUE if not derniere_date else _lendemain(derniere_date)
    fin = _veille(aujourdhui)
    if jusqu_a and jusqu_a < fin:
        fin = jusqu_a
    jours, jour = [], debut
    while jour <= fin:
        jours.append(jour)
        jour = _lendemain(jour)
    return jours


def _date(txt):
    return datetime.date(int(txt[0:4]), int(txt[5:7]), int(txt[8:10]))


def _lendemain(txt):
    return (_date(txt) + datetime.timedelta(days=1)).isoformat()


def _veille(txt):
    return (_date(txt) - datetime.timedelta(days=1)).isoformat()


def recuperer_jour(date):
    """Une journee de by_date. Leve en cas d'echec, l'appelant decide."""
    requete = urllib.request.Request(URL_JOUR.format(date), headers={"User-Agent": AGENT})
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        return json.loads(reponse.read().decode("utf-8"))


def aspirer(dates, recuperer, ids_connus, table):
    """Aspire chaque jour et regroupe. `recuperer` est injecte (testable).

    Un jour en erreur est reessaye UNE fois, puis journalise et saute : une
    coupure reseau au 900e jour ne doit pas perdre les 899 precedents.
    """
    paquets, en_erreur, ecartes = {}, [], 0
    for i, date in enumerate(dates):
        bruts = None
        for essai in (1, 2):
            try:
                bruts = recuperer(date)
                break
            except Exception as exc:           # reseau, JSON, 404 : meme traitement
                if essai == 2:
                    en_erreur.append(date)
                    print(f"  ! {date} saute apres 2 essais : {exc}")
        if bruts is None:
            continue
        du_jour, ecartes_jour = regrouper(bruts, ids_connus, table)
        ecartes += ecartes_jour
        for code, paquet in du_jour.items():
            cible = paquets.setdefault(code, {**paquet, "decks": []})
            cible["decks"].extend(paquet["decks"])
        if i % 100 == 0:
            print(f"  {date} ({i + 1}/{len(dates)})")
    return paquets, en_erreur, ecartes


def fusionner(anciennes, nouvelles):
    """Dedoublonne par id, la version la plus recente gagne, tri date decroissante."""
    par_id = {d["id"]: d for d in anciennes}
    par_id.update({d["id"]: d for d in nouvelles})
    return sorted(par_id.values(), key=lambda d: (d.get("date", ""), d["id"]), reverse=True)


def ecrire_index(racine, paquets):
    """Un fichier par heros, FUSIONNE avec l'existant. Rend le nombre ecrit."""
    dossier = os.path.join(racine, "data", "marvelcdb")
    os.makedirs(dossier, exist_ok=True)
    for code, paquet in paquets.items():
        chemin = os.path.join(dossier, code + ".json")
        anciennes = []
        if os.path.exists(chemin):
            try:
                anciennes = json.load(open(chemin, encoding="utf-8")).get("decks", [])
            except ValueError:
                anciennes = []          # fichier tronque par une interruption : on repart
        json.dump({
            "hero_code": code,
            "hero_name": paquet["hero_name"],
            "deck_starter": paquet["deck_starter"],
            "genere_le": datetime.date.today().isoformat(),
            "decks": fusionner(anciennes, paquet["decks"]),
        }, open(chemin, "w", encoding="utf-8"), ensure_ascii=False)
    return len(paquets)


def publier_vers_game(racine):
    """Rend data/marvelcdb visible depuis .game/, d'ou le moteur lit.

    Le moteur tourne avec .game pour repertoire courant : `/read_file?data/x`
    resout .game/data/x. Selon le lanceur utilise, .game/data est un lien
    symbolique vers data/ (launcher_fast.py, et l'installation miroir) ou une
    COPIE figee (installation WSL, heritee de launcher.py). Dans le second cas
    l'index n'apparaitrait jamais : on y pose un lien vers le vrai dossier, ou
    une copie si les liens sont impossibles.
    """
    data_game = os.path.join(racine, ".game", "data")
    if not os.path.isdir(data_game):
        return "rien a faire"                 # pas de .game : rien a publier
    if os.path.islink(data_game):
        return "rien a faire"                 # deja un lien vers data/
    source = os.path.join(racine, "data", "marvelcdb")
    cible = os.path.join(data_game, "marvelcdb")
    if os.path.islink(cible) or os.path.isdir(cible):
        if os.path.islink(cible):
            return "lien"
        shutil.rmtree(cible)
    try:
        os.symlink(source, cible, target_is_directory=True)
        return "lien"
    except OSError:
        shutil.copytree(source, cible)
        return "copie"
```

Puis la ligne de commande, en fin de fichier :

```python
def _meta(racine):
    chemin = os.path.join(racine, "data", "marvelcdb", "_meta.json")
    if os.path.exists(chemin):
        try:
            return json.load(open(chemin, encoding="utf-8"))
        except ValueError:
            pass
    return {}


def _recalculer(racine, ids_connus):
    """Rejoue la jouabilite sur l'index existant, sans reseau.

    A lancer apres l'ajout d'un pack : des decks jusque-la incomplets
    redeviennent jouables sans qu'il faille reaspirer quoi que ce soit.
    """
    dossier = os.path.join(racine, "data", "marvelcdb")
    if not os.path.isdir(dossier):
        print("Aucun index a recalculer : lance d'abord un passage d'aspiration.")
        return 0
    change = 0
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith(".json") or fichier.startswith("_"):
            continue
        chemin = os.path.join(dossier, fichier)
        paquet = json.load(open(chemin, encoding="utf-8"))
        for deck in paquet.get("decks", []):
            absentes = sorted(c for c in deck.get("cartes", {}) if c not in ids_connus)
            if absentes != deck.get("cartes_absentes"):
                change += 1
            deck["cartes_absentes"] = absentes
            deck["jouable"] = not absentes
        json.dump(paquet, open(chemin, "w", encoding="utf-8"), ensure_ascii=False)
    return change


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = sys.argv[1:]

    def option(nom):
        return args[args.index(nom) + 1] if nom in args else None

    ids_connus = charger_ids_cartes(racine)
    print(f"{len(ids_connus)} cartes connues du jeu.")

    if "--recalculer" in args:
        change = _recalculer(racine, ids_connus)
        print(f"Jouabilite recalculee, {change} deck(s) ont change d'etat.")
        print("Publication :", publier_vers_game(racine))
        raise SystemExit(0)

    meta = _meta(racine)
    depuis = option("--depuis") or meta.get("derniere_date")
    if option("--depuis"):
        depuis = _veille(option("--depuis"))       # --depuis est INCLUSIF
    dates = jours_a_traiter(depuis, datetime.date.today().isoformat(), option("--jusqu-a"))
    a_reessayer = [j for j in meta.get("jours_en_erreur", []) if j not in dates]
    dates = sorted(set(dates) | set(a_reessayer))
    if not dates:
        print("Deja a jour, rien a aspirer.")
        raise SystemExit(0)

    print(f"{len(dates)} jour(s) a aspirer, du {dates[0]} au {dates[-1]}.")

    def recuperer_ralenti(date):
        time.sleep(DELAI)
        return recuperer_jour(date)

    table = table_deck_starter(racine)
    paquets, en_erreur, ecartes = aspirer(dates, recuperer_ralenti, ids_connus, table)
    total = sum(len(p["decks"]) for p in paquets.values())
    ecrire_index(racine, paquets)

    ancien = _meta(racine).get("total_decks", 0)
    json.dump({
        "derniere_date": dates[-1],
        "genere_le": datetime.date.today().isoformat(),
        "total_decks": ancien + total,
        "jours_en_erreur": en_erreur,
    }, open(os.path.join(racine, "data", "marvelcdb", "_meta.json"), "w",
            encoding="utf-8"), ensure_ascii=False)

    print(f"{total} deck(s) indexes sur {len(paquets)} heros, "
          f"{ecartes} ecarte(s) (heros absent du jeu), "
          f"{len(en_erreur)} jour(s) en erreur.")
    print("Publication :", publier_vers_game(racine))
```

- [ ] **Étape 4 : lancer le test pour le voir passer**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 tools/test_marvelcdb_index.py
```

Attendu : `TOUT PASSE`.

- [ ] **Étape 5 : essai réel sur trois jours, contre le vrai site**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 \
  tools/marvelcdb_index.py --depuis 2026-08-01 --jusqu-a 2026-08-03
ls ~/marvel-work/fusion/marvel-lcg-src/data/marvelcdb/ | head
cat ~/marvel-work/fusion/marvel-lcg-src/data/marvelcdb/_meta.json
```

Attendu : quelques dizaines de decks, un fichier par héros, `_meta.json` avec `derniere_date: 2026-08-03` et `jours_en_erreur: []`. Vérifier aussi que `.game/data/marvelcdb` existe côté WSL :

```bash
ls -ld ~/marvel-work/fusion/marvel-lcg-src/.game/data/marvelcdb
```

- [ ] **Étape 6 : synchroniser et commiter**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rsync -a "$S/tools/" "$M/tools/"
rsync -a "$S/data/marvelcdb/" "$M/data/marvelcdb/"
```

Rien à commiter : `tools/` et `data/` vivent hors du dépôt.

---

## Tâche 3 : module [B], chargement, filtres et favoris

**Fichiers :**
- Créer : `~/marvel-work/fusion/marvel-lcg-src/public/js/marvelcdb/index.js`
- Créer : `~/marvel-work/fusion/marvel-lcg-src/public/js/marvelcdb/filtres.js`
- Créer : `~/marvel-work/fusion/marvel-lcg-src/public/js/marvelcdb/favoris.js`
- Créer : `outils/verifier-marvelcdb.mjs` (dans le dépôt)

**Interfaces :**
- Consomme : les fichiers écrits par la tâche 2.
- Produit :
  - `chargerHeros(heroCode, recuperer?) -> Promise<{hero_code, hero_name, deck_starter, decks: []}>` — rend un paquet vide plutôt que de lever si l'index n'existe pas
  - `filtrer(decks, {aspect, tag, texte, masquerIncomplets}) -> []`
  - `lireFavoris(stockage?) -> string[]`, `estFavori(id, stockage?) -> boolean`, `basculerFavori(id, stockage?) -> string[]`

- [ ] **Étape 1 : écrire le test qui échoue**

Créer `outils/verifier-marvelcdb.mjs` dans le dépôt, sur le patron de `outils/verifier-salon-etat.mjs` :

```js
// Vérifie les fonctions pures du module de recherche de decks MarvelCDB.
//
// Les modules visés n'importent rien et ne touchent au DOM que par un stockage
// injecté : Node les exécute tels quels, sans navigateur ni serveur.
//
// La cible est la copie Windows du jeu : Node est le binaire Windows et ne lit
// pas les chemins WSL. Synchroniser AVANT de lancer, sinon on teste la version
// précédente (bash ui-app/deployer.sh, ou le rsync du guide §1.3).
//
// Usage : node outils/verifier-marvelcdb.mjs

import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const mod = async (nom) =>
  import(pathToFileURL(resolve('Fusion/marvel-lcg-src/public/js/marvelcdb/' + nom)).href)

const { filtrer } = await mod('filtres.js')
const { lireFavoris, estFavori, basculerFavori } = await mod('favoris.js')

let echecs = 0
const verifier = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
  if (!ok) echecs += 1
  console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
  if (!ok) {
    console.log(`      obtenu  ${JSON.stringify(obtenu)}`)
    console.log(`      attendu ${JSON.stringify(attendu)}`)
  }
}

/* ---------------------------------------------------------------- filtres */
const deck = (id, o = {}) => ({
  id, nom: o.nom ?? ('deck ' + id), aspect: o.aspect ?? 'justice',
  tags: o.tags ?? [], date: o.date ?? '2026-01-01',
  jouable: o.jouable ?? true, cartes_absentes: o.cartes_absentes ?? [], cartes: {},
})
const ids = (l) => l.map((d) => d.id)

const jeu = [
  deck(1, { aspect: 'justice', date: '2026-03-01', tags: ['solo'] }),
  deck(2, { aspect: 'aggression', date: '2026-05-01', tags: ['multiplayer'] }),
  deck(3, { aspect: 'justice', date: '2026-04-01', nom: 'Le Grand Bleu' }),
  deck(4, { aspect: 'justice', date: '2026-06-01', jouable: false, cartes_absentes: ['99999'] }),
]

verifier('tri chronologique décroissant, incomplets masqués par défaut',
  ids(filtrer(jeu, {})), [2, 3, 1])
verifier('masquerIncomplets: false montre tout',
  ids(filtrer(jeu, { masquerIncomplets: false })), [4, 2, 3, 1])
verifier('filtre par aspect', ids(filtrer(jeu, { aspect: 'justice' })), [3, 1])
verifier('filtre par tag', ids(filtrer(jeu, { tag: 'solo' })), [1])
verifier('recherche par nom, insensible à la casse et aux accents',
  ids(filtrer(jeu, { texte: 'grand bleu' })), [3])
verifier('critères cumulés',
  ids(filtrer(jeu, { aspect: 'justice', texte: 'deck' })), [1])
verifier('aucun résultat rend une liste vide',
  filtrer(jeu, { aspect: 'pool' }), [])
verifier('liste vide en entrée', filtrer([], {}), [])

/* ---------------------------------------------------------------- favoris */
const faussStockage = () => {
  const m = new Map()
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
  }
}
let st = faussStockage()
verifier('aucun favori au départ', lireFavoris(st), [])
verifier('ajout', basculerFavori(64331, st), ['64331'])
verifier('un deuxième favori s’ajoute', basculerFavori(64332, st), ['64331', '64332'])
verifier('estFavori', estFavori(64331, st), true)
verifier('retrait', basculerFavori(64331, st), ['64332'])
verifier('stockage illisible : aucun favori, aucune erreur',
  lireFavoris({ getItem: () => 'pas du json', setItem: () => {} }), [])

/* La tâche 4 insérera le bloc « conversion » ICI, avant ces deux lignes. */
console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)
```

- [ ] **Étape 2 : lancer le test pour le voir échouer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && node outils/verifier-marvelcdb.mjs
```

Attendu : `ERR_MODULE_NOT_FOUND` sur `filtres.js`.

- [ ] **Étape 3 : écrire les trois modules**

`public/js/marvelcdb/filtres.js` :

```js
// filtres.js — sélection et tri des decks d'un héros. Fonctions PURES, sans
// DOM ni réseau : la refonte React de l'écran de préparation les reprendra
// telles quelles.
"use strict";

/** Minuscules sans accents, pour comparer un nom de deck à une recherche.
    La plage \u0300-\u036f est écrite en échappement : un caractère combinant
    posé littéralement dans le fichier serait invisible et illisible. */
function normaliser(texte) {
    return String(texte || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

/**
 * @param {Array} decks  entrées d'index
 * @param {{aspect?: string, tag?: string, texte?: string, masquerIncomplets?: boolean}} criteres
 * @returns {Array} decks retenus, du plus récent au plus ancien
 */
export function filtrer(decks, criteres) {
    const { aspect, tag, texte, masquerIncomplets = true } = criteres || {};
    const recherche = normaliser(texte);
    return (decks || [])
        .filter((d) => (!masquerIncomplets || d.jouable))
        .filter((d) => (!aspect || d.aspect === aspect))
        .filter((d) => (!tag || (d.tags || []).includes(tag)))
        .filter((d) => (!recherche || normaliser(d.nom).includes(recherche)))
        .sort((a, b) => (b.date || "").localeCompare(a.date || "") || b.id - a.id);
}

/** Aspects réellement présents dans une liste, pour ne proposer que ceux-là. */
export function aspectsPresents(decks) {
    return [...new Set((decks || []).map((d) => d.aspect).filter(Boolean))].sort();
}

/** Tags réellement présents, même usage. */
export function tagsPresents(decks) {
    return [...new Set((decks || []).flatMap((d) => d.tags || []))].sort();
}
```

`public/js/marvelcdb/favoris.js` :

```js
// favoris.js — decks mis de côté, mémorisés dans le navigateur.
//
// Le stockage est un PARAMÈTRE (défaut : localStorage) : sans ça le module
// serait intestable hors navigateur, et un localStorage indisponible (mode
// privé strict) ferait planter l'écran de préparation entier.
"use strict";

export const CLE_FAVORIS = "marvelcdb_favoris";

function stockageParDefaut() {
    try {
        return window.localStorage;
    } catch {
        return { getItem: () => null, setItem: () => {} };
    }
}

export function lireFavoris(stockage) {
    const st = stockage || stockageParDefaut();
    try {
        const brut = JSON.parse(st.getItem(CLE_FAVORIS) || "[]");
        return Array.isArray(brut) ? brut.map(String) : [];
    } catch {
        return [];
    }
}

export function estFavori(id, stockage) {
    return lireFavoris(stockage).includes(String(id));
}

/** Ajoute ou retire, puis rend la liste à jour. */
export function basculerFavori(id, stockage) {
    const st = stockage || stockageParDefaut();
    const cle = String(id);
    const liste = lireFavoris(st);
    const suite = liste.includes(cle) ? liste.filter((x) => x !== cle) : [...liste, cle];
    try {
        st.setItem(CLE_FAVORIS, JSON.stringify(suite));
    } catch {
        /* quota plein ou stockage refusé : le favori ne survivra pas à la
           session, ce qui vaut mieux qu'une exception dans l'écran. */
    }
    return suite;
}
```

`public/js/marvelcdb/index.js` :

```js
// index.js — accès à l'index local des decks MarvelCDB.
//
// Les fichiers sont produits par tools/marvelcdb_index.py et servis par la
// route existante /read_file, qui rend n'importe quel JSON du dossier de jeu.
// Aucune route serveur n'a été ajoutée.
"use strict";

const _cache = new Map();

/** Index d'un héros. Un héros sans index rend un paquet VIDE, pas une erreur :
 *  l'écran doit rester utilisable quand l'indexeur n'a jamais tourné. */
export async function chargerHeros(heroCode, recuperer) {
    const code = String(heroCode || "").split(",")[0];
    if (!code) return paquetVide(code);
    if (_cache.has(code)) return _cache.get(code);
    const fetcher = recuperer || ((url) => fetch(url));
    const promesse = fetcher("/read_file?data/marvelcdb/" + encodeURIComponent(code) + ".json")
        .then((r) => (r.ok ? r.json() : paquetVide(code)))
        .then((p) => (p && Array.isArray(p.decks) ? p : paquetVide(code)))
        .catch(() => paquetVide(code));
    _cache.set(code, promesse);
    return promesse;
}

function paquetVide(code) {
    return { hero_code: code, hero_name: "", deck_starter: "", decks: [] };
}
```

- [ ] **Étape 4 : synchroniser vers ② puis lancer le test**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rsync -a "$S/public/js/" "$M/public/js/"
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && node outils/verifier-marvelcdb.mjs
```

Attendu : 14 lignes `OK` puis `TOUT PASSE`.

- [ ] **Étape 5 : commiter le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add outils/verifier-marvelcdb.mjs
git commit -m "test(marvelcdb): filtres et favoris de la recherche de decks"
```

---

## Tâche 4 : module [B], conversion en deck moteur

Un deck MarvelCDB mélange cartes signature et pioche du joueur dans un seul `slots` de 40 cartes ; le moteur veut `hero_deck` et `player_deck` séparés. Cette règle existe déjà, écrite deux fois : dans `deck.html` et dans `importMarvelcdb` de `app.js`. Le panneau serait une troisième copie. On l'extrait donc, et on rebranche l'import existant dessus.

**Fichiers :**
- Créer : `~/marvel-work/fusion/marvel-lcg-src/public/js/marvelcdb/conversion.js`
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/js/prepare/app.js:1257-1290` (`importMarvelcdb`)
- Modifier : `outils/verifier-marvelcdb.mjs`

**Interfaces :**
- Consomme : les entrées d'index (tâche 1), le deck starter du jeu (`hero.deck` de `catalog.js`).
- Produit :
  - `versDeckMoteur(entree, deckStarter, classeDe) -> deck` où `classeDe(cardId) -> string`
  - `ecartDeConversion(entree, deck) -> number` — 0 si la conversion est cohérente

- [ ] **Étape 1 : ajouter les tests qui échouent**

Dans `outils/verifier-marvelcdb.mjs`, ajouter l'import à la suite des deux autres :

```js
const { versDeckMoteur, ecartDeConversion } = await mod('conversion.js')
```

Puis remplacer la ligne `/* La tâche 4 insérera le bloc « conversion » ICI... */` par :

```js
/* ------------------------------------------------------------- conversion */
// Deck starter du jeu, format réel (deck/starter/wasp.json, réduit ici).
const starterWasp = {
  name: 'Wasp', version: '0.5.8',
  hero: ['13001a,13001b,13001c'],
  hero_deck: ['13002', '13003', '13003'],
  obligations: ['13026'], nemesis_set: ['13027'], set_aside: [],
  player_deck: ['00000'],
}
// classeDe : « Hero » pour les signatures, l'aspect sinon (comme cards.aspectOf).
const classeDe = (id) => (['13002', '13003'].includes(String(id)) ? 'Hero' : 'Justice')

const entree = {
  id: 63358, nom: 'Hives are Stronger Together',
  cartes: { '13002': 1, '13003': 2, '01062': 2, '01063': 1 },
}
const converti = versDeckMoteur(entree, starterWasp, classeDe)

verifier('le squelette du héros vient du deck du jeu, pas de marvelcdb',
  [converti.hero, converti.hero_deck, converti.obligations, converti.nemesis_set],
  [starterWasp.hero, starterWasp.hero_deck, starterWasp.obligations, starterWasp.nemesis_set])
verifier('les cartes signature sont exclues du player_deck',
  converti.player_deck.filter((id) => id === '13002' || id === '13003'), [])
verifier('les cartes joueur sont répétées selon leur quantité',
  converti.player_deck.slice().sort(), ['01062', '01062', '01063'])
verifier('le player_deck du deck starter est remplacé, jamais concaténé',
  converti.player_deck.includes('00000'), false)
verifier('nom et provenance conservés',
  [converti.name, converti.metadata.url],
  ['Hives are Stronger Together', 'https://marvelcdb.com/decklist/view/63358'])
verifier('version du deck du jeu conservée', converti.version, '0.5.8')

// 26002 : exclusion héritée de deck.html, reprise à l'identique.
verifier('la carte 26002 est ignorée',
  versDeckMoteur({ id: 1, nom: 'x', cartes: { '26002': 1, '01062': 1 } },
    starterWasp, classeDe).player_deck, ['01062'])

// Cohérence : 4 cartes déclarées, 3 signatures reconnues... il en manque une.
verifier('conversion cohérente : écart nul', ecartDeConversion(entree, converti), 0)
const bancal = versDeckMoteur(entree, starterWasp, () => 'Justice')
verifier('signature non reconnue : écart non nul',
  ecartDeConversion(entree, bancal) !== 0, true)
```

Les deux lignes finales (`console.log` / `process.exit`) restent en dernier, inchangées.

- [ ] **Étape 2 : lancer le test pour le voir échouer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && node outils/verifier-marvelcdb.mjs
```

Attendu : `ERR_MODULE_NOT_FOUND` sur `conversion.js`.

- [ ] **Étape 3 : écrire `conversion.js`**

```js
// conversion.js — deck MarvelCDB -> deck moteur.
//
// Un deck marvelcdb est un `slots` de 40 cartes qui MÉLANGE les cartes
// signature du héros et la pioche du joueur. Le moteur, lui, veut hero_deck
// (signature) et player_deck (pioche) séparés, plus le squelette du héros
// (obligations, némésis, set_aside) qu'il ne faut jamais reconstruire : on le
// reprend tel quel dans le deck de départ du jeu.
"use strict";

/**
 * @param {{id: number, nom: string, cartes: Object}} entree  entrée d'index ou deck collé
 * @param {Object} deckStarter  deck de départ du héros, tel que servi par le jeu
 * @param {(cardId: string) => string} classeDe  classe d'une carte ("Hero" pour une signature)
 */
export function versDeckMoteur(entree, deckStarter, classeDe) {
    const player_deck = [];
    for (const id in (entree.cartes || {})) {
        // 26002 : exclusion héritée de deck.html, conservée à l'identique.
        if (id === "26002") continue;
        if (classeDe(id) === "Hero") continue;
        for (let n = 0; n < entree.cartes[id]; n++) player_deck.push(id);
    }
    return {
        name: entree.nom || deckStarter.name,
        version: deckStarter.version,
        metadata: { url: "https://marvelcdb.com/decklist/view/" + entree.id },
        hero: deckStarter.hero,
        hero_deck: deckStarter.hero_deck,
        player_deck,
        obligations: deckStarter.obligations,
        nemesis_set: deckStarter.nemesis_set,
        set_aside: deckStarter.set_aside,
    };
}

/**
 * Contrôle de cohérence : le total déclaré par marvelcdb doit se répartir
 * exactement entre les signatures du jeu et la pioche produite. Un écart
 * signale une carte signature que le catalogue n'a pas reconnue, donc un deck
 * à ne pas proposer tel quel.
 */
export function ecartDeConversion(entree, deck) {
    const total = Object.values(entree.cartes || {}).reduce((s, n) => s + n, 0);
    return total - (deck.hero_deck || []).length - (deck.player_deck || []).length;
}
```

- [ ] **Étape 4 : rebrancher l'import par lien sur le module**

Dans `public/js/prepare/app.js`, ajouter l'import en tête (après la ligne `import { appliquerTutoriel } ...`) :

```js
import { versDeckMoteur, ecartDeConversion } from "/public/js/marvelcdb/conversion.js";
```

(`ecartDeConversion` n'est pas utilisé par l'import par lien ; il sert au panneau de la tâche 5. Les deux sont importés ici pour n'avoir qu'une ligne d'import de ce module.)

Puis, dans `importMarvelcdb`, remplacer le bloc qui construit `player_deck` et `deck` (de `const player_deck = [];` jusqu'à la fin de l'objet `deck`) par :

```js
    // La règle de conversion vit dans public/js/marvelcdb/conversion.js : le
    // panneau de recherche et ce champ « coller un lien » doivent produire
    // EXACTEMENT le même deck, sinon un deck jouable ici serait refusé là.
    const deck = versDeckMoteur(
        { id, nom: data.name || hero.name, cartes: data.slots || {} },
        hero.deck,
        (cid) => { const c = cards.get(cid); return (c && c.class) || ""; },
    );
```

Le reste de la fonction (résolution du héros, `return { hero, deck }`) est inchangé.

- [ ] **Étape 5 : synchroniser et lancer le test complet**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rsync -a "$S/public/js/" "$M/public/js/"
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && node outils/verifier-marvelcdb.mjs
```

Attendu : `TOUT PASSE`, 23 lignes `OK`.

- [ ] **Étape 6 : vérifier à la main que l'import par lien marche toujours**

Le rebranchement touche un chemin qui fonctionnait : il faut le reprouver. Serveur allumé (voir tâche 6, étape 1), ouvrir `prepare.html`, choisir Wasp, coller `63358` dans le champ d'import, cliquer « Import ».

Attendu : le deck « Hives are Stronger Together » est importé, la fenêtre propose de le sauvegarder, « Voir les cartes » montre 40 cartes.

- [ ] **Étape 7 : commiter le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add outils/verifier-marvelcdb.mjs
git commit -m "test(marvelcdb): conversion d'un deck marvelcdb en deck moteur"
```

---

## Tâche 5 : panneau [C] dans l'écran de préparation

**Fichiers :**
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/js/prepare/app.js` (`stepDecks`, ~ligne 1354 ; nouvelle fonction `ouvrirPanneauCdb`)
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/css/prepare/prepare.css` (fin de fichier)
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/js/prepare/dico-en.js`

**Interfaces :**
- Consomme : `chargerHeros` (tâche 3), `filtrer`/`aspectsPresents`/`tagsPresents` (tâche 3), `lireFavoris`/`basculerFavori` (tâche 3), `versDeckMoteur`/`ecartDeConversion` (tâche 4).
- Produit : rien pour les tâches suivantes.

- [ ] **Étape 1 : ajouter les imports et le bouton d'ouverture**

En tête de `app.js`, à la suite de l'import de la tâche 4 :

```js
import { chargerHeros } from "/public/js/marvelcdb/index.js";
import { filtrer, aspectsPresents, tagsPresents } from "/public/js/marvelcdb/filtres.js";
import { lireFavoris, basculerFavori } from "/public/js/marvelcdb/favoris.js";
```

Dans `stepDecks`, dans le bloc `el("div", { class: "deck-import" }, ...)`, insérer un bouton **avant** le bouton « Éditeur de deck » :

```js
                el("button", {
                    class: "btn-ghost",
                    title: t("Parcourir les decks publiés sur MarvelCDB"),
                    onclick: () => ouvrirPanneauCdb(i),
                }, t("Decks MarvelCDB")),
```

- [ ] **Étape 2 : écrire le panneau**

Ajouter dans `app.js`, juste après `showDeckCards` :

```js
/* ---- Panneau : parcourir les decks MarvelCDB indexés ---- */
// L'index est produit hors ligne par tools/marvelcdb_index.py. Aucune requête
// vers marvelcdb ici : tout est local, cartes comprises.
async function ouvrirPanneauCdb(i) {
    const p = state.players[i];
    if (!p || !p.hero) return;
    await cards.load();
    const paquet = await chargerHeros(p.hero.heroCardId);
    const criteres = { aspect: "", tag: "", texte: "", masquerIncomplets: true };
    let favoris = lireFavoris();

    const liste = el("div", { class: "cdb-liste" });
    const compte = el("span", { class: "dm-sub" });

    const rendre = () => {
        const retenus = filtrer(paquet.decks, criteres);
        // Les favoris remontent en tête, l'ordre chronologique tient le reste.
        retenus.sort((a, b) => favoris.includes(String(b.id)) - favoris.includes(String(a.id)));
        compte.textContent = `${retenus.length} ${t("decks")}`;
        if (!retenus.length) {
            liste.replaceChildren(el("div", { class: "cdb-vide" },
                paquet.decks.length
                    ? t("Aucun deck ne correspond à ces filtres.")
                    : t("Aucun deck indexé pour ce héros. Lance tools/marvelcdb_index.py.")));
            return;
        }
        liste.replaceChildren(...retenus.map(ligne));
    };

    const ligne = (d) => {
        const estFavori = favoris.includes(String(d.id));
        const etoile = el("button", {
            class: "cdb-etoile" + (estFavori ? " on" : ""),
            title: t("Mettre de côté"),
            onclick: (e) => { e.stopPropagation(); favoris = basculerFavori(d.id); rendre(); },
        }, estFavori ? "★" : "☆");

        const choisir = () => {
            if (!d.jouable) {
                alert(t("Ce deck utilise des cartes absentes du jeu :") + "\n" +
                      d.cartes_absentes.join(", "));
                return;
            }
            const deck = versDeckMoteur(d, p.hero.deck,
                (cid) => { const c = cards.get(cid); return (c && c.class) || ""; });
            if (ecartDeConversion(d, deck) !== 0) {
                alert(t("Ce deck n’a pas pu être converti proprement, il n’est pas proposé."));
                return;
            }
            p.deck = deck; p.deckSource = "imported"; p.deckAuto = false;
            overlay.remove();
            render();
        };

        return el("div", { class: "cdb-ligne" + (d.jouable ? "" : " incomplet"), onclick: choisir },
            etoile,
            el("div", { class: "cdb-nom" },
                el("b", {}, d.nom),
                el("span", { class: "cdb-date" }, d.date)),
            el("div", { class: "do-tags" },
                d.aspect ? el("span", { class: "tag asp", style: { background: ASPECTS[d.aspect] || "#555" } }, d.aspect) : null,
                ...(d.tags || []).map((tg) => el("span", { class: "tag" }, tg)),
                d.jouable ? null : el("span", { class: "tag manque" },
                    `${d.cartes_absentes.length} ${t("cartes manquantes")}`)),
        );
    };

    const champ = (props, ...kids) => el("select", props, ...kids);
    const opt = (v, libelle) => el("option", { value: v }, libelle);

    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) overlay.remove(); } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, `${t("Decks MarvelCDB")} — ${p.hero.name}`),
                compte,
                el("button", { class: "dm-close", onclick: () => overlay.remove() }, "✕"),
            ),
            el("div", { class: "cdb-filtres" },
                el("input", {
                    class: "mcdb-input", placeholder: t("Chercher par nom..."),
                    oninput: (e) => { criteres.texte = e.target.value; rendre(); },
                }),
                champ({ onchange: (e) => { criteres.aspect = e.target.value; rendre(); } },
                    opt("", t("Tous les aspects")),
                    ...aspectsPresents(paquet.decks).map((a) => opt(a, a))),
                champ({ onchange: (e) => { criteres.tag = e.target.value; rendre(); } },
                    opt("", t("Tous les tags")),
                    ...tagsPresents(paquet.decks).map((tg) => opt(tg, tg))),
                el("label", { class: "cdb-tout" },
                    el("input", {
                        type: "checkbox",
                        onchange: (e) => { criteres.masquerIncomplets = !e.target.checked; rendre(); },
                    }),
                    t("Montrer les decks incomplets")),
            ),
            liste,
        ));

    rendre();
    document.body.append(overlay);
}
```

- [ ] **Étape 3 : ajouter les styles**

À la fin de `public/css/prepare/prepare.css` :

```css
/* --- Panneau de recherche MarvelCDB (réutilise .deck-modal) --------------- */
.cdb-filtres{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.cdb-filtres select{background:var(--ink2);color:#dfe6ef;border:1px solid var(--line);border-radius:8px;padding:7px 10px}
.cdb-tout{display:flex;align-items:center;gap:6px;color:#9aa7b6;font-size:13px}
.cdb-liste{display:flex;flex-direction:column;gap:8px;max-height:62vh;overflow:auto}
.cdb-ligne{display:flex;align-items:center;gap:12px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--ink2);cursor:pointer}
.cdb-ligne:hover{border-color:#4d6584}
.cdb-ligne.incomplet{opacity:.55}
.cdb-nom{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.cdb-nom b{color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cdb-date{color:#8b97a6;font-size:12px}
.cdb-etoile{background:none;border:0;color:#6d7a8a;font-size:19px;cursor:pointer;line-height:1}
.cdb-etoile.on{color:#efc34a}
.tag.manque{background:#7a2f2f;color:#ffd9d9}
.cdb-vide{color:#9aa7b6;padding:22px;text-align:center}
```

- [ ] **Étape 4 : traduire les chaînes**

Dans `public/js/prepare/dico-en.js`, ajouter un bloc à la suite de celui de l'import marvelcdb :

```js
    /* ---- Panneau de recherche marvelcdb ---- */
    "Decks MarvelCDB": "MarvelCDB decks",
    "Parcourir les decks publiés sur MarvelCDB": "Browse decks published on MarvelCDB",
    "decks": "decks",
    "Chercher par nom...": "Search by name...",
    "Tous les aspects": "All aspects",
    "Tous les tags": "All tags",
    "Montrer les decks incomplets": "Show incomplete decks",
    "Mettre de côté": "Bookmark",
    "cartes manquantes": "missing cards",
    "Aucun deck ne correspond à ces filtres.": "No deck matches these filters.",
    "Aucun deck indexé pour ce héros. Lance tools/marvelcdb_index.py.":
        "No deck indexed for this hero. Run tools/marvelcdb_index.py.",
    "Ce deck utilise des cartes absentes du jeu :": "This deck uses cards missing from the game:",
    "Ce deck n’a pas pu être converti proprement, il n’est pas proposé.":
        "This deck could not be converted cleanly and is not offered.",
```

- [ ] **Étape 5 : contrôle syntaxique et déploiement**

`node --check` ne lit pas un chemin WSL : passer par la forme `//wsl.localhost/`.

```bash
node --check "//wsl.localhost/Ubuntu/home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/prepare/app.js"
node --check "//wsl.localhost/Ubuntu/home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/prepare/dico-en.js"
bash "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app/deployer.sh"
```

Attendu : aucune sortie des deux `node --check`, et `deployer.sh` finit par « Deploye dans 2 installation(s) ».

- [ ] **Étape 6 : essai à l'œil, dans le navigateur**

Serveur allumé (tâche 6, étape 1), ouvrir `prepare.html`, aller jusqu'à l'étape des decks avec un héros bien fourni (Spider-Man), cliquer « Decks MarvelCDB ».

À vérifier, dans l'ordre :
1. la liste s'affiche, triée du plus récent au plus ancien ;
2. le filtre d'aspect réduit la liste ;
3. la recherche par nom fonctionne ;
4. l'étoile remonte un deck en tête et survit à une fermeture/réouverture du panneau ;
5. « Montrer les decks incomplets » fait apparaître des lignes grisées avec le badge de cartes manquantes, et un clic dessus refuse la sélection en nommant les cartes ;
6. le choix d'un deck jouable ferme le panneau et met à jour le bloc du joueur ;
7. bascule en anglais (bouton de langue) : aucune chaîne française ne subsiste dans le panneau.

- [ ] **Étape 7 : commiter ce qui est suivi**

Les fichiers touchés vivent tous hors du dépôt. Rien à commiter ; la sauvegarde est faite par `deployer.sh` (étape 5), qui a synchronisé ① vers ②.

---

## Tâche 6 : premier passage complet et vérification de bout en bout

**Fichiers :** aucun fichier de code. Cette tâche produit les données et la preuve.

- [ ] **Étape 1 : allumer le serveur de la copie vivante**

⚠️ Ne jamais couper le serveur du port 2345 sans prévenir : une partie en ligne peut être en cours.

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 launcher_fast.py
```

Ce lanceur remplace `.game/data` par un lien symbolique vers `data/`, ce qui rend `publier_vers_game` sans objet pour cette installation. Attendre `Engine.Initialize() -> True`.

- [ ] **Étape 2 : vérifier que `/read_file` sert bien l'index**

L'index de trois jours de la tâche 2 est déjà en place. Prendre un code de héros présent dans `data/marvelcdb/` :

```bash
curl -s --compressed "http://127.0.0.1:2345/read_file?data/marvelcdb/_meta.json"
```

Attendu : le JSON de `_meta.json`. Une réponse `{}` signifie que le chemin n'est pas résolu depuis `.game` : reprendre `publier_vers_game`.

- [ ] **Étape 3 : lancer le premier passage complet**

Environ 2 500 requêtes, à peu près 15 minutes. Le script est rejouable : une interruption reprend au jour suivant le dernier écrit.

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 \
  tools/marvelcdb_index.py 2>&1 | tee /tmp/index-marvelcdb.log
```

Attendu en fin de journal : un total de l'ordre de 40 000 decks, un nombre d'écartés non nul (héros absents du jeu), `0 jour(s) en erreur` ou une courte liste.

- [ ] **Étape 4 : relever la taille des fichiers**

La spec prévoit une découpe par année au-delà de 3 Mo par fichier. Vérifier si le cas se présente :

```bash
ls -S ~/marvel-work/fusion/marvel-lcg-src/data/marvelcdb/ | head -5
du -h ~/marvel-work/fusion/marvel-lcg-src/data/marvelcdb/ | tail -1
```

Si un fichier dépasse 3 Mo, **ne pas découper tout de suite** : mesurer d'abord le temps d'ouverture du panneau dans le navigateur. `read_file` sert le fichier gzippé, ce qui change beaucoup l'ordre de grandeur. Noter la mesure ici et n'agir que si l'attente est perceptible.

- [ ] **Étape 5 : propager l'index vers l'installation miroir**

`deployer.sh` ne synchronise pas `data/`.

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rsync -a "$S/data/marvelcdb/" "$M/data/marvelcdb/"
ls -ld "$M/.game/data"     # doit être un lien symbolique vers data/
```

- [ ] **Étape 6 : partie réelle avec un deck MarvelCDB**

Dans `prepare.html` : choisir un héros, ouvrir « Decks MarvelCDB », prendre un deck jouable, aller jusqu'au lancement, et jouer un tour complet (jouer une carte, attaquer, passer la phase du vilain).

Attendu : le plateau se charge, la main contient les cartes du deck choisi, aucun `traceback` dans la console du serveur.

- [ ] **Étape 7 : non-régression du harnais**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check" && npm run captures
```

`prepare.html` fait partie des écrans sous captures de référence, mais le panneau n'est visible qu'après un clic : la référence `preparation-nouvelle` **ne doit pas bouger**. Si elle bouge, c'est que le bouton « Decks MarvelCDB » a modifié la mise en page de la barre d'import : passer par `npm run captures:valider`, jamais par `--update-snapshots`.

- [ ] **Étape 8 : contrat gelé de lancement de partie**

C'est le test que la spec §10 désigne comme « celui qui compte » : il pilote `prepare.html` par libellés et compare la charge envoyée à `/new?data=` au contrat `ui-check/contrat-nouvelle-partie.json`.

⚠️ **Il détruit la partie en cours** (il appelle `/new`). À ne lancer qu'après l'étape 6.

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check" && npm run lancement
```

Attendu : vert. Le panneau n'ayant modifié ni les libellés (« Continuer », « Lancer la partie ») ni la forme de la charge, un rouge ici signale une vraie régression, pas un changement voulu. Le contrat ne se modifie jamais pour faire passer un test rouge.

- [ ] **Étape 9 : consigner le résultat**

Mettre le todo à jour (statut, date, écarts constatés) :

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add .planning/todos/2026-07-28-recherche-decks-marvelcdb.md
git commit -m "docs(marvelcdb): recherche de decks livree, todo mis a jour"
```

---

## Écarts à la spec, constatés en relisant le code le 6/8/2026

1. **L'import par lien existe déjà** (`app.js`, « Import marvelcdb »), livré avec la refonte de l'écran de préparation. La spec le décrivait comme à faire (`lien.js`). Le plan ne le réécrit pas : il extrait sa règle de conversion pour que le panneau et lui restent d'accord (tâche 4).
2. **La conversion ne passe pas par `/get_hero_json`.** L'écran de préparation tient déjà le deck de départ du héros en mémoire (`hero.deck`, via `catalog.js`). Le plan s'en sert, ce qui évite une requête et un aller-retour par nom de fichier.
3. **La vue n'est plus l'ancien `prepare.html`** décrit au §5 de la spec : cet écran est aujourd'hui une application de modules ES (`js/prepare/app.js`). Le panneau s'y insère comme une fenêtre modale, sur les styles `.deck-modal` déjà présents.
4. **Le §13 « hors périmètre » est en partie périmé** : le choix du deck par chaque joueur depuis son siège existe depuis le salon multijoueur (3/8/2026). Le panneau reste néanmoins réservé à l'hôte dans ce plan : le brancher dans `salon.html` est un chantier distinct, à décider après usage.

## Ce que l'exécution a appris, le 6/8/2026

Quatre choses que ni la spec ni les tests n'avaient vues, toutes trouvées en lançant le vrai passage. Elles sont corrigées et commitées ; elles sont notées ici pour que le plan ne mente pas sur ce qu'il a coûté.

1. **Le premier passage complet demande `--depuis 2019-10-01`.** L'essai à trois jours de la tâche 2 écrit un `_meta.json`, et le passage suivant se croit à jour. La tâche 6 étape 3, telle qu'écrite, n'aspirait que deux jours.
2. **`total_decks` dérivait.** Il s'additionnait d'un passage à l'autre, alors que les passages se recouvrent. Il se compte désormais sur les fichiers (`compter_index`).
3. **Un jour sans aucun deck publié rend HTTP 500, pas une liste vide.** Mesuré : `by_date/2019-10-01` → 500, `by_date/2019-10-02` → 200 avec un deck. Un jour sur trois est dans ce cas sur les débuts du site. Les traiter en pannes remplissait `jours_en_erreur` de dates réessayées à chaque passage, pour toujours. Seul le 500 est lu ainsi ; 502, 503 et coupure réseau restent des erreurs, et le nombre de jours creux s'affiche en garde-fou.
4. **La poignée de main TLS coûte treize fois le prix de la requête, depuis WSL.** Mesuré sur 5 jours : 21,2 s en rouvrant une connexion à chaque fois (ce que fait `urllib`), contre 1,6 s en réutilisant la même. Le passage sur `http.client` avec une connexion de module ramène l'historique complet de deux heures à une vingtaine de minutes.

Et un défaut de conception du plan lui-même : **l'index n'était écrit qu'à la toute fin.** La spec promettait qu'une interruption reprenne au jour suivant le dernier écrit ; c'était faux, et une coupure à la 33e minute a bien tout perdu. L'écriture se fait maintenant par tranches de 100 jours, avec le marqueur de reprise posé après chacune. La leçon générale : un traitement long doit écrire au fur et à mesure ET montrer où il en est, sinon on ne peut ni l'interrompre ni le diagnostiquer.

## Ce qui était déjà rouge avant ce chantier

`npm run captures` (19 écrans) et le test « depuis l'écran » de `npm run lancement` échouent, et ce n'est pas de ce plan que ça vient : l'étape 1 de l'assistant fusionne désormais mode et héros, si bien que le bouton « Continuer » reste inactif tant qu'aucun héros n'est choisi. Les références et le parcours du test datent d'avant cette refonte. La capture `preparation-nouvelle` ne photographie que l'étape 1, où le bouton « Decks MarvelCDB » n'existe pas, et elle attend une page 45 px plus haute que celle servie. Le test « sans l'écran », qui vérifie le contrat `/new`, est vert.

## Question ouverte, à trancher avec l'utilisateur

Les fichiers créés côté jeu (`tools/marvelcdb_index.py`, `public/js/marvelcdb/*`) vivent **hors du dépôt git**, comme tout le moteur. Leur seule sauvegarde est la copie miroir ②. Trois options : les laisser hors versionnement (pratique actuelle), forcer leur ajout depuis le miroir (`git add -f Fusion/marvel-lcg-src/public/js/marvelcdb/`), ou n'y toucher qu'au moment du prochain re-zip. Le plan suit la pratique actuelle tant que rien n'est décidé.
