# Salon multijoueur — plan d'implémentation

> **Pour les agents :** SOUS-SKILL REQUIS — utiliser `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les étapes utilisent la syntaxe case à cocher (`- [ ]`).

**Objectif :** en multi, chaque invité choisit son héros et son deck depuis son siège ; l'hôte voit les choix arriver et ne peut lancer que lorsque tout le monde a choisi.

**Architecture :** deux routes serveur stockent un choix par siège dans un dict en mémoire (même forme que `set_cursor`/`get_cursors`). Une page autonome `/salon.html` laisse l'invité poster son choix. Le wizard de l'hôte sonde, affiche, et bloque le lancement. `buildDescriptor()` n'est pas modifié.

**Stack :** Python 3.10 + aiohttp (moteur), JavaScript ES modules sans framework (`public/js/`), Node pour les vérifications hors navigateur.

**Spec :** `.planning/todos/2026-08-02-salon-multijoueur.md`

## Contraintes globales

- **On édite dans la copie VIVANTE** `~/marvel-work/fusion/marvel-lcg-src/`, jamais dans le miroir. Recopie par le `rsync` du guide §1.3 à la fin de chaque tâche qui touche `data/`, `src/` ou `public/`.
- **`launcher-multi.sh` est à la RACINE du moteur, hors du `rsync`** : à éditer dans les DEUX copies (guide §1.3).
- **Numérotation des sièges** : index technique `p=0` pour l'hôte, `p=1..3` pour les invités ; libellés affichés « Joueur 1 » à « Joueur 4 ». Ne jamais mélanger.
- **Le chemin SOLO ne doit pas changer.** Quand `multi` est faux, le wizard doit se comporter exactement comme aujourd'hui.
- Toute chaîne visible passe par `t()` et a son entrée dans `public/js/prepare/dico-en.js` (guide §11).
- Pas d'em dash ni de tiret parenthétique dans les textes visibles.
- Python du moteur : `~/marvel-work/python/bin/python3.10`.

---

### Tâche 1 : les deux routes serveur et la remise à zéro

**Fichiers :**
- Modifier : `src/engine/device/web/server/server_get.py` (handlers après `get_cursors`, ligne ~350 ; enregistrement après la ligne 419)
- Modifier : `src/engine/device/web/server/server_new_game.py:16-20`
- Créer : `tools/test_salon.py`

**Interfaces :**
- Consomme : `self.allowed_seats(request)` de `server_base.py` (rend `Set[int]` des sièges autorisés, ou `None` si la protection est coupée) ; `SEAT_PASSWORDS` de `server_base.py`.
- Produit : `POST /set_choix_siege` corps `{p:int, hero_card_id:str, deck_id:str, deck_source:str}` → `{result:"ok"}` / 400 / 403. `GET /get_choix_sieges` → `{multi:bool, sieges:{"1":{hero_card_id,deck_id,deck_source}}}`. Attribut `self.choix_sieges: Dict[int, dict]`.

- [ ] **Étape 1 : écrire le test qui échoue**

Créer `tools/test_salon.py` :

```python
"""Teste les routes du salon multijoueur.

Demarre le moteur comme tools/test_newgame.py, puis tape les routes en HTTP.
Usage: python3.10 tools/test_salon.py <game_dir> <port>
"""
import json, os, sys, threading, time, urllib.request

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)

cfg = json.load(open(os.path.join(GAME_DIR, "launch.json")))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["seat_passwords"] = ["h0", "j1", "j2", "j3"]
json.dump(cfg, open(os.path.join(GAME_DIR, "launch.json"), "w"), indent=2)

sys.stdout = open("/tmp/test_salon_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True
from engine import Engine
Engine.Initialize()
threading.Thread(target=Engine.game.GameLoop, daemon=True).start()
time.sleep(3)

BASE = f"http://127.0.0.1:{PORT}"
resultats = []

def verifier(nom, ok, detail=""):
    resultats.append((nom, ok, detail))

def poster(corps, cookie=None):
    req = urllib.request.Request(
        BASE + "/set_choix_siege",
        data=json.dumps(corps).encode(),
        headers={"Content-Type": "application/json",
                 **({"Cookie": cookie} if cookie else {})})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, {}

def lire():
    with urllib.request.urlopen(BASE + "/get_choix_sieges") as r:
        return json.load(r)

import hashlib
jeton = hashlib.md5(b"j1").hexdigest()
choix = {"p": 1, "hero_card_id": "69001a", "deck_id": "madame_web",
         "deck_source": "base"}

code, _ = poster(choix)
verifier("sans jeton de siege -> 403", code == 403, f"code={code}")

code, _ = poster(choix, cookie=f"seat_token_1={jeton}")
verifier("avec le bon jeton -> 200", code == 200, f"code={code}")

etat = lire()
verifier("multi detecte", etat.get("multi") is True, str(etat.get("multi")))
verifier("choix relu", etat.get("sieges", {}).get("1", {}).get("hero_card_id") == "69001a",
         json.dumps(etat.get("sieges")))

code, _ = poster({"p": 1, "hero_card_id": "", "deck_id": "", "deck_source": ""},
                 cookie=f"seat_token_1={jeton}")
verifier("choix incomplet -> 400", code == 400, f"code={code}")

sortie = sys.__stdout__
for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"  [{detail}]"), file=sortie)
rates = [n for n, ok, _ in resultats if not ok]
print(("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)"), file=sortie)
os._exit(0 if not rates else 1)
```

- [ ] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 \
    tools/test_salon.py ~/marvel-work/fusion/marvel-lcg-src/.game-src 26000
```
Attendu : ECHEC sur les 5 lignes (routes inexistantes → 404, donc ni 403 ni 200).

- [ ] **Étape 3 : écrire les deux handlers**

Dans `src/engine/device/web/server/server_get.py`, juste après `get_cursors` :

```python
    # --- Salon multijoueur : un choix de heros/deck par siege ---------------
    # Meme forme que set_cursor/get_cursors ci-dessus, a deux differences pres :
    # aucune peremption (un choix vaut jusqu'au lancement) et une verification
    # du siege en ECRITURE. Sans elle, un spectateur muni du mot de passe
    # d'entree pourrait changer le heros d'un joueur.
    # On ne stocke PAS le deck complet, seulement de quoi le retrouver :
    # l'hote le recharge par /get_hero_json et /list_deck, deja en place.
    async def set_choix_siege(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            p = int(data['p'])
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)

        autorises = self.allowed_seats(request)
        if autorises is not None and p not in autorises:
            return web.json_response({'error': 'not your seat'}, status=403)

        hero_card_id = str(data.get('hero_card_id', ''))
        deck_id = str(data.get('deck_id', ''))
        if not hero_card_id or not deck_id:
            return web.json_response(
                {'error': 'hero_card_id and deck_id required'}, status=400)

        if not hasattr(self, 'choix_sieges'):
            self.choix_sieges = {}
        self.choix_sieges[p] = {
            'hero_card_id': hero_card_id,
            'deck_id': deck_id,
            'deck_source': str(data.get('deck_source', '')),
        }
        return web.json_response({'result': 'ok'})

    async def get_choix_sieges(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        choix = getattr(self, 'choix_sieges', {})
        return web.json_response({
            'multi': bool(passwords) and any(passwords),
            'sieges': {str(p): c for p, c in choix.items()},
        })
```

Enregistrement, juste après la ligne `self.AddAwaitGetSecurity('/get_cursors', self.get_cursors)` :

```python
        self.AddPostSecurity('/set_choix_siege', self.set_choix_siege)
        self.AddAwaitGetSecurity('/get_choix_sieges', self.get_choix_sieges)
```

- [ ] **Étape 4 : vider le salon à la création de partie**

Dans `src/engine/device/web/server/server_new_game.py`, méthode `new_game` :

```python
    async def new_game(self, request: web.Request) -> web.Response:
        data = request.rel_url.query.get('data', "")
        new_game = Json.LoadsAs(data, NewGameDescriptor)
        # Le salon a rempli son office : on le vide pour que la partie suivante
        # ne reparte pas avec les choix de la precedente. GameServer herite des
        # deux classes, l'attribut est donc le meme objet.
        self.choix_sieges = {}
        self.game.NewGame(new_game)
        return web.json_response({'result': "New game created"})
```

- [ ] **Étape 5 : relancer le test, vérifier qu'il passe**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 -m compileall -q src && \
    ~/marvel-work/python/bin/python3.10 tools/test_salon.py ~/marvel-work/fusion/marvel-lcg-src/.game-src 26001
```
Attendu : `TOUT PASSE`, 5 lignes OK.

- [ ] **Étape 6 : non-régression du moteur**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 \
    tools/test_cards.py ~/marvel-work/fusion/marvel-lcg-src/.game-src 26002 /tmp/rapport-cartes.json
```
Attendu : `ok 3973 / err 0`.

- [ ] **Étape 7 : recopier et committer**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
rsync -a --exclude __pycache__ "$S/src/" "$M/src/" && rsync -a "$S/tools/" "$M/tools/"
cd "$M/.." && git add Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/tools
git commit -m "feat(salon): routes de choix de heros/deck par siege"
```

---

### Tâche 2 : la décision « peut-on lancer », en module pur

**Fichiers :**
- Créer : `public/js/prepare/salon-etat.js`
- Créer : `outils/verifier-salon-etat.mjs` (à la racine du dossier projet, côté Windows)

**Interfaces :**
- Consomme : rien (module sans import, testable sous Node).
- Produit : `etatSalon({nombreJoueurs, sieges})` → `{prete: boolean, manquants: number[], choixParSiege: Map<number, object>}`. `manquants` contient les **libellés affichés** (2, 3, 4), pas les index techniques.

- [ ] **Étape 1 : écrire le vérificateur qui échoue**

Créer `outils/verifier-salon-etat.mjs` :

```js
// Vérifie la décision « peut-on lancer la partie ».
// Le module est pur et sans import : Node peut l'exécuter tel quel.
// Usage : node outils/verifier-salon-etat.mjs
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const chemin = resolve('Fusion/marvel-lcg-src/public/js/prepare/salon-etat.js')
const { etatSalon } = await import(pathToFileURL(chemin).href)

let echecs = 0
const verifier = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
  if (!ok) echecs += 1
  console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
  if (!ok) console.log(`      obtenu ${JSON.stringify(obtenu)} / attendu ${JSON.stringify(attendu)}`)
}

// 2 joueurs : on attend le seul invité, siège technique 1 = « Joueur 2 ».
let e = etatSalon({ nombreJoueurs: 2, sieges: {} })
verifier('2 joueurs, personne n’a choisi', [e.prete, e.manquants], [false, [2]])

e = etatSalon({ nombreJoueurs: 2, sieges: { 1: { hero_card_id: '69001a', deck_id: 'madame_web' } } })
verifier('2 joueurs, l’invité a choisi', [e.prete, e.manquants], [true, []])

// 4 joueurs : on attend les sièges techniques 1, 2, 3.
e = etatSalon({ nombreJoueurs: 4, sieges: { 1: { hero_card_id: 'a', deck_id: 'd' } } })
verifier('4 joueurs, un seul a choisi', [e.prete, e.manquants], [false, [3, 4]])

// Le siège de l’hôte n’est jamais attendu, même s’il traîne dans le dict.
e = etatSalon({ nombreJoueurs: 2, sieges: { 0: { hero_card_id: 'a', deck_id: 'd' } } })
verifier('le siège de l’hôte ne compte pas', [e.prete, e.manquants], [false, [2]])

// Un choix incomplet ne vaut pas un choix.
e = etatSalon({ nombreJoueurs: 2, sieges: { 1: { hero_card_id: '69001a', deck_id: '' } } })
verifier('choix incomplet', [e.prete, e.manquants], [false, [2]])

// Un siège au-delà du nombre de joueurs est ignoré.
e = etatSalon({ nombreJoueurs: 2, sieges: { 1: { hero_card_id: 'a', deck_id: 'd' }, 3: { hero_card_id: 'b', deck_id: 'e' } } })
verifier('siège hors table ignoré', [e.prete, e.manquants], [true, []])

console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)
```

- [ ] **Étape 2 : lancer, vérifier l'échec**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions" && node outils/verifier-salon-etat.mjs
```
Attendu : `ERR_MODULE_NOT_FOUND` (le module n'existe pas).

- [ ] **Étape 3 : écrire le module**

Créer `~/marvel-work/fusion/marvel-lcg-src/public/js/prepare/salon-etat.js` :

```js
// salon-etat.js — décide si la partie multi peut être lancée, et qui manque.
//
// Module PUR et sans import : il se teste sous Node
// (outils/verifier-salon-etat.mjs) sans navigateur ni serveur.
//
// Deux numérotations coexistent, ne pas les mélanger :
//   index technique p = 0 (hôte), 1..3 (invités)
//   libellé affiché  = p + 1  (« Joueur 1 » à « Joueur 4 »)
"use strict";

function choixComplet(choix) {
    return !!(choix && choix.hero_card_id && choix.deck_id);
}

/**
 * @param {{nombreJoueurs:number, sieges:Object}} etat
 *        `sieges` est indexé par index TECHNIQUE (clés numériques ou chaînes).
 * @returns {{prete:boolean, manquants:number[], choixParSiege:Map<number,object>}}
 *        `manquants` liste des LIBELLÉS affichés, croissants.
 */
export function etatSalon({ nombreJoueurs, sieges }) {
    const choixParSiege = new Map();
    for (const [cle, choix] of Object.entries(sieges || {})) {
        const p = Number(cle);
        if (Number.isInteger(p) && choixComplet(choix)) choixParSiege.set(p, choix);
    }

    const manquants = [];
    // Le siège 0 est celui de l'hôte : il choisit dans son wizard, jamais ici.
    for (let p = 1; p < nombreJoueurs; p += 1) {
        if (!choixParSiege.has(p)) manquants.push(p + 1);
    }

    return { prete: manquants.length === 0, manquants, choixParSiege };
}
```

- [ ] **Étape 4 : relancer, vérifier que tout passe**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions" && node outils/verifier-salon-etat.mjs
```
Attendu : 6 lignes OK, `TOUT PASSE`.

- [ ] **Étape 5 : recopier et committer**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
rsync -a "$S/public/" "$M/public/"
cd "$M/.." && git add Fusion/marvel-lcg-src/public/js/prepare/salon-etat.js outils/verifier-salon-etat.mjs
git commit -m "feat(salon): decision de lancement en module pur, teste sous node"
```

---

### Tâche 3 : la page `/salon.html` pour l'invité

**Fichiers :**
- Créer : `public/salon.html`
- Créer : `public/js/salon/app.js`
- Modifier : `src/engine/device/web/server/server_html.py:20-33` (déclarer la page)
- Modifier : `public/js/prepare/dico-en.js` (chaînes nouvelles)

**Interfaces :**
- Consomme : `catalog.heroes()` et `catalog.decksForHero(hero)` de `/public/js/prepare/catalog.js` ; `t()` de `/public/js/prepare/langue.js` ; `POST /set_choix_siege` (tâche 1) ; `GET /get_choix_sieges` (tâche 1) ; `GET /get_play_scene_name` (existante, rend une chaîne vide s'il n'y a pas de partie).
- Produit : la page `/salon.html?p=N`. Rien qu'une autre tâche consomme.

- [ ] **Étape 1 : déclarer la page côté serveur**

Dans `server_html.py`, à côté des autres `AddHtmlSecurity` :

```python
        self.AddHtmlSecurity('/salon.html', './public/salon.html')
```

- [ ] **Étape 2 : ajouter la destination `salon` à `/claim_seat`**

Dans `server_html.py`, méthode `handle_claim_seat`, remplacer le calcul de `destination` :

```python
        # L'hote reclame son siege PUIS va creer la partie : &to=prepare.
        # Les invites vont au SALON choisir leur heros : &to=salon.
        vers = request.query.get('to')
        if vers == 'prepare':
            destination = '/prepare.html'
        elif vers == 'salon':
            destination = f'/salon.html?p={seat}'
        else:
            destination = f'/app/board.html?p={seat}'
```

- [ ] **Étape 3 : écrire la page**

Créer `public/salon.html` : une coquille minimale qui charge le module et fournit trois conteneurs (`#salon-entete`, `#salon-heros`, `#salon-decks`) plus une zone de statut `#salon-statut`. Reprendre la feuille de style inline de `public/rejoindre.html` (même palette, même largeur) pour rester cohérent sans créer de CSS partagé.

Créer `public/js/salon/app.js` :

```js
// app.js — le salon : l'invité choisit SON héros et SON deck.
//
// Page autonome, volontairement à l'écart du wizard (public/js/prepare/app.js,
// 1850 lignes) : on ne veut prendre aucun risque sur le chemin SOLO.
// Seule la couche DONNÉES est partagée (catalog/api/cards), pas l'interface.
"use strict";
import { catalog } from "/public/js/prepare/catalog.js";
import { t } from "/public/js/prepare/langue.js";

const siege = Number(new URLSearchParams(location.search).get("p") ?? "-1");
const etat = { hero: null, decks: [], choixEnvoye: null };

const $ = (sel) => document.querySelector(sel);
function el(tag, attrs = {}, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
        if (k === "class") n.className = v;
        else if (k.startsWith("on")) n[k] = v;
        else if (v != null) n.setAttribute(k, v);
    }
    for (const e of enfants.flat()) if (e != null) n.append(e.nodeType ? e : document.createTextNode(e));
    return n;
}

function statut(texte, erreur = false) {
    const zone = $("#salon-statut");
    zone.textContent = texte;
    zone.classList.toggle("est-erreur", erreur);
}

async function envoyerChoix(deck) {
    const corps = {
        p: siege,
        hero_card_id: etat.hero.heroCardId,
        deck_id: deck.id,
        deck_source: deck.source,
    };
    const res = await fetch("/set_choix_siege", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corps),
    });
    if (res.status === 403) { statut(t("Ce siège n’est pas le tien."), true); return; }
    if (!res.ok) { statut(t("Choix refusé par le serveur."), true); return; }
    etat.choixEnvoye = { hero: etat.hero, deck };
    statut(`${t("Choix envoyé")} : ${etat.hero.name} — ${deck.name}. ${t("Tu peux encore changer d’avis.")}`);
}

async function rendreDecks() {
    etat.decks = await catalog.decksForHero(etat.hero);
    const zone = $("#salon-decks");
    zone.replaceChildren(
        el("h2", {}, `${t("Deck de")} ${etat.hero.name}`),
        ...etat.decks.map((dk) => el("button", {
            class: "salon-deck",
            onclick: () => envoyerChoix(dk),
        }, dk.name))
    );
}

async function rendreHeros() {
    const heroes = await catalog.heroes();
    const zone = $("#salon-heros");
    zone.replaceChildren(
        el("h2", {}, t("Choisis ton héros")),
        ...heroes.map((h) => el("button", {
            class: "salon-hero",
            onclick: () => { etat.hero = h; rendreDecks(); },
        }, h.name))
    );
}

/** Quand la partie démarre, on bascule sur le plateau. */
function surveillerLeLancement() {
    setInterval(async () => {
        try {
            const res = await fetch("/get_play_scene_name");
            const nom = (await res.text()).trim();
            if (nom) location.href = `/app/board.html?p=${siege}`;
        } catch (e) { /* serveur momentanement injoignable : on reessaie */ }
    }, 2000);
}

async function demarrer() {
    if (!Number.isInteger(siege) || siege < 0) {
        statut(t("Ouvre ton lien personnel : c’est lui qui réserve ton siège."), true);
        return;
    }
    $("#salon-entete").textContent = `${t("Tu es le")} ${t("Joueur")} ${siege + 1}`;
    await rendreHeros();
    surveillerLeLancement();
}

demarrer();
```

- [ ] **Étape 4 : ajouter les chaînes au dictionnaire**

Dans `public/js/prepare/dico-en.js` :

```js
    "Choisis ton héros": "Choose your hero",
    "Deck de": "Deck for",
    "Tu es le": "You are",
    "Choix envoyé": "Choice sent",
    "Tu peux encore changer d’avis.": "You can still change your mind.",
    "Ce siège n’est pas le tien.": "This seat is not yours.",
    "Choix refusé par le serveur.": "Choice rejected by the server.",
    "Ouvre ton lien personnel : c’est lui qui réserve ton siège.":
        "Open your personal link: that is what reserves your seat.",
```

- [ ] **Étape 5 : vérifier à la main**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 -m compileall -q src
node --check public/js/salon/app.js
```
Puis lancer le jeu en solo (`JOUER-SOLO.bat`), ouvrir `http://127.0.0.1:2345/salon.html?p=1`, vérifier : la grille de héros s'affiche, cliquer un héros liste ses decks, cliquer un deck affiche « Choix envoyé ». En solo la protection des sièges est coupée, donc l'écriture est acceptée : c'est normal et suffisant pour cette étape.

- [ ] **Étape 6 : recopier et committer**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
rsync -a --exclude __pycache__ "$S/src/" "$M/src/" && rsync -a "$S/public/" "$M/public/"
cd "$M/.." && git add Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/public
git commit -m "feat(salon): page de choix heros/deck pour l'invite"
```

---

### Tâche 4 : l'hôte voit les choix et le lancement se bloque

**Fichiers :**
- Modifier : `public/js/prepare/app.js` (import en tête ; `stepDecks()` ligne ~1123 ; le bloc « premier joueur » du panneau Avancé ; la garde du bouton de lancement)
- Modifier : `public/js/prepare/dico-en.js`

**Interfaces :**
- Consomme : `etatSalon()` de `salon-etat.js` (tâche 2) ; `GET /get_choix_sieges` (tâche 1) ; `catalog.decksForHero(hero)` pour retrouver le deck depuis son `deck_id`.
- Produit : rien qu'une autre tâche consomme.

- [ ] **Étape 1 : sonder le salon**

En tête de `app.js`, ajouter l'import et l'état :

```js
import { etatSalon } from "/public/js/prepare/salon-etat.js";
```

Puis une fonction de sondage. Elle remplit `state.salon` et redessine :

```js
// Salon multijoueur : les invités choisissent leur héros et leur deck depuis
// leur siège. En solo, /get_choix_sieges rend multi:false et tout ce bloc
// reste inerte — le wizard se comporte exactement comme avant.
state.salon = { multi: false, sieges: {}, prete: true, manquants: [] };

async function sonderSalon() {
    try {
        const res = await fetch("/get_choix_sieges");
        const brut = await res.json();
        const calc = etatSalon({ nombreJoueurs: state.playerCount, sieges: brut.sieges });
        const avant = JSON.stringify(state.salon);
        state.salon = { multi: !!brut.multi, sieges: brut.sieges, ...calc };
        if (state.salon.multi) await appliquerChoixSalon();
        if (JSON.stringify(state.salon) !== avant) render();
    } catch (e) { /* serveur momentanement injoignable : on reessaie */ }
}
setInterval(sonderSalon, 2000);
sonderSalon();
```

- [ ] **Étape 2 : recopier les choix dans `state.players`**

```js
/** Traduit les choix du salon en héros + deck dans state.players. */
async function appliquerChoixSalon() {
    const heroes = await catalog.heroes();
    for (const [p, choix] of state.salon.choixParSiege) {
        if (p === 0 || p >= state.playerCount) continue;   // 0 = l'hôte
        const hero = heroes.find((h) => h.heroCardId === choix.hero_card_id);
        if (!hero) continue;
        const decks = await catalog.decksForHero(hero);
        const dk = decks.find((d) => d.id === choix.deck_id);
        if (!dk) continue;
        const joueur = state.players[p] || (state.players[p] = {});
        joueur.hero = hero;
        joueur.deck = dk.deck;
        joueur.deckSource = dk.source;
        joueur.duSalon = true;
    }
}
```

- [ ] **Étape 3 : afficher en lecture seule à l'étape des decks**

Dans `stepDecks()`, avant de dessiner le sélecteur d'un joueur `i` :

```js
        // Siège piloté par un invité : on montre son choix, on ne le modifie pas.
        if (state.salon.multi && i > 0) {
            const p = state.players[i];
            if (p && p.duSalon) {
                return el("div", { class: "salon-choix" },
                    el("b", {}, `${t("Joueur")} ${i + 1}`),
                    el("span", {}, `${p.hero.name} — ${p.deck.name} ✓`));
            }
            return el("div", { class: "salon-attente" },
                el("b", {}, `${t("Joueur")} ${i + 1}`),
                el("span", {}, t("en attente de son choix…")));
        }
```

- [ ] **Étape 4 : bloquer le lancement et griser « premier joueur »**

Dans la fonction qui décide si l'étape finale est franchissable (`stepComplete`, ligne ~225), ajouter en tête du cas de l'étape finale :

```js
    if (state.salon.multi && !state.salon.prete) return false;
```

Et dans le rendu du bouton de lancement, afficher la raison :

```js
    state.salon.multi && !state.salon.prete
        ? el("span", { class: "salon-manquants" },
            `${t("En attente de")} ${state.salon.manquants.map((n) => `${t("Joueur")} ${n}`).join(", ")}`)
        : null,
```

Dans le bloc « Avancé », désactiver le sélecteur de premier joueur :

```js
        // En multi, le siège N est une PERSONNE : buildDescriptor fait tourner
        // l'ordre des joueurs pour appliquer ce réglage, ce qui donnerait à
        // chacun le deck de son voisin. On le grise plutôt que de le retirer :
        // en solo (hot-seat) il reste utile et sans danger.
        disabled: state.salon.multi ? "" : undefined,
```
accompagné, quand `state.salon.multi` est vrai, de la phrase :
```js
        el("span", { class: "avance-note" }, t("En multi, c’est toujours le Joueur 1 qui commence : les sièges restent attachés aux personnes.")),
```

- [ ] **Étape 5 : chaînes du dictionnaire**

```js
    "en attente de son choix…": "waiting for their choice…",
    "En attente de": "Waiting for",
    "En multi, c’est toujours le Joueur 1 qui commence : les sièges restent attachés aux personnes.":
        "In multiplayer, Player 1 always goes first: seats stay tied to people.",
```

- [ ] **Étape 6 : vérifier la non-régression du SOLO**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && node --check public/js/prepare/app.js
```
Puis `JOUER-SOLO.bat` : créer une partie 1 joueur et une partie 2 joueurs hot-seat, vérifier que le sélecteur de deck, le réglage « premier joueur » et le bouton de lancement se comportent comme avant. C'est la vérification la plus importante de cette tâche.

- [ ] **Étape 7 : recopier et committer**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
rsync -a "$S/public/" "$M/public/"
cd "$M/.." && git add Fusion/marvel-lcg-src/public
git commit -m "feat(salon): l'hote voit les choix et attend la table complete"
```

---

### Tâche 5 : les liens du lanceur, la doc, et la partie de bout en bout

**Fichiers :**
- Modifier : `launcher-multi.sh` lignes 83-85 et 101-103, **dans les DEUX copies**
- Modifier : `MULTIJOUEUR.md`
- Modifier : `GUIDE-CREATION-CONTENU.md` (§10, piège des deux numérotations de sièges)

**Interfaces :**
- Consomme : la destination `to=salon` de `/claim_seat` (tâche 3).
- Produit : rien.

- [ ] **Étape 1 : ajouter `&to=salon` aux six liens invités**

Dans `launcher-multi.sh`, les trois lignes du message copié (83-85) et les trois de l'encadré (101-103) :

```sh
- Joueur 2 : $URL/claim_seat?p=1&key=$SIEGE_1&to=salon
- Joueur 3 : $URL/claim_seat?p=2&key=$SIEGE_2&to=salon
- Joueur 4 : $URL/claim_seat?p=3&key=$SIEGE_3&to=salon
```

Le lien de l'hôte (`&to=prepare`) ne change pas.

- [ ] **Étape 2 : appliquer dans les DEUX copies**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
diff "$S/launcher-multi.sh" "$M/launcher-multi.sh" && echo "les deux copies sont identiques"
```
Attendu : aucune différence. Ce fichier est à la racine, hors du `rsync` du guide §1.3 : c'est le piège qui a déjà coûté cher avec `launch.json`.

- [ ] **Étape 3 : mettre à jour `MULTIJOUEUR.md`**

Dans « En bref — comment ça marche », remplacer le point 4 :

```markdown
4. Chaque ami clique sur **son** lien, entre le mot de passe d'entrée, et arrive sur **le salon** : il y choisit son héros puis son deck. Son choix apparaît chez toi au fur et à mesure. Il peut encore changer d'avis tant que tu n'as pas lancé.
```

Et ajouter dans « Bon à savoir / limites actuelles » :

```markdown
- **Le lancement attend tout le monde** : le bouton reste gris tant qu'un siège n'a pas choisi, avec le nom de ceux qu'on attend. Le nombre de joueurs, c'est toi qui le fixes.
- **Le réglage « premier joueur » est grisé en multi** : c'est toujours le Joueur 1 qui commence, sinon les sièges se décaleraient et chacun se retrouverait avec le deck du voisin.
- **Les invités ne peuvent pas construire de deck depuis le salon** : ils choisissent parmi le deck de base, les packages d'aspect et les decks déjà sauvegardés. Pour un deck sur mesure, ils passent par `…/deck-builder.html` (il apparaîtra ensuite dans leur liste).
```

- [ ] **Étape 4 : consigner le piège des sièges au guide**

Dans `GUIDE-CREATION-CONTENU.md` §10 (Pièges connus) :

```markdown
- **Deux numérotations de sièges en multi.** L'index technique (`p=` dans l'URL,
  cookie `seat_token_<p>`, index joueur du moteur) commence à **0 pour l'hôte** ;
  l'affichage parle de « Joueur 1 » à « Joueur 4 ». Les confondre donne à
  quelqu'un le deck de son voisin. Voir `public/js/prepare/salon-etat.js`, qui
  fait la conversion en un seul endroit, et `.planning/todos/2026-08-02-salon-multijoueur.md` §4 bis.
```

- [ ] **Étape 5 : partie de bout en bout à deux**

C'est le seul test qui valide la bascule salon → plateau, et il est manuel.

1. `JOUER-EN-MULTI.bat`.
2. Ouvrir le lien Joueur 2 dans un **second navigateur** (ou une fenêtre privée : le cookie de siège ne doit pas être partagé avec celui de l'hôte).
3. Côté invité : choisir un héros, choisir un deck, vérifier « Choix envoyé ».
4. Côté hôte : l'étape des decks affiche le choix ; le bouton de lancement était gris avant, il s'allume maintenant.
5. Lancer. Vérifier que l'invité **bascule tout seul** sur le plateau, sur son siège, avec le héros qu'il a choisi.
6. Vérifier qu'il ne peut agir que sur son siège (comportement existant, à ne pas avoir cassé).

- [ ] **Étape 6 : committer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add Fusion/marvel-lcg-src/launcher-multi.sh MULTIJOUEUR.md GUIDE-CREATION-CONTENU.md
git commit -m "docs(salon): liens invites vers le salon, mode d'emploi et piege des sieges"
```

---

## Auto-relecture du plan

**Couverture de la spec** — §5.1 routes → tâche 1 ; §5.2 page salon → tâche 3 ; §5.3 wizard hôte → tâche 4 ; §5.4 lanceur → tâche 5 ; §6 premier joueur → tâche 4 étape 4 ; §7 cas limites → couverts par les tests de la tâche 1 (403, 400), la tâche 2 (choix incomplet, siège hors table, siège de l'hôte) et la tâche 5 (bout en bout) ; §8 tests → tâches 1, 2 et 5.

**Cas limites de la spec §7 sans test automatisé, assumés :** redémarrage du serveur (salon vide, chacun rechoisit) et deck sauvegardé disparu entre le choix et le lancement (l'hôte voit un siège sans choix, le lancement reste bloqué — comportement obtenu gratuitement par `appliquerChoixSalon`, qui n'écrit rien quand le deck est introuvable).

**Cohérence des types** — `etatSalon({nombreJoueurs, sieges})` rend `{prete, manquants, choixParSiege}` : produit en tâche 2, consommé en tâche 4 étapes 1-2 sous ces noms exacts. Le corps de `POST /set_choix_siege` est `{p, hero_card_id, deck_id, deck_source}` en tâche 1 comme en tâche 3. `deck.id` et `deck.source` viennent de `catalog.decksForHero()`, dont la forme est déjà celle utilisée par `loadDecks()` dans `app.js`.
