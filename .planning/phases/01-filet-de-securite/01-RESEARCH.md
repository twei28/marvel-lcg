# Phase 1 : Filet de sécurité et boucle de dev - Research

**Researched:** 2026-07-28
**Domain:** Tests de non-régression visuelle (Playwright), fixtures d'état de jeu, bascule de version d'UI côté client
**Confidence:** HIGH (la majorité des conclusions vient de mesures faites sur le serveur en cours d'exécution et sur le code source local)

## Summary

Cette phase pose quatre outils avant toute refonte : (1) une commande unique de captures/diff visuel, (2) 20-40 fixtures `get_world` rejouables, (3) une bascule `?ui=old`, (4) un test automatisé du contrat de lancement `/new?data=`.

La recherche a été menée **contre le serveur réel en train de tourner** (`http://127.0.0.1:2345`, PID 180492, lancé par `launcher.py`) et contre les sources dans `~/marvel-work/fusion/marvel-lcg-src/`. Six contraintes d'environnement, toutes vérifiées par mesure, dictent la conception et sont plus structurantes que le choix d'outil :

1. **`node` dans WSL est en fait `node.exe` de Windows** (`~/.local/bin/node` → `/mnt/c/Program Files/nodejs/node.exe`, `process.platform === 'win32'`). Il n'existe aucun Node natif Linux. L'outillage doit donc vivre sur un chemin **Windows natif** (le dépôt Desktop), pas dans WSL. Vérifié : Windows node atteint sans problème le serveur WSL sur `127.0.0.1:2345` et `localhost:2345`.
2. **Le routage serveur est une liste blanche d'extensions avec échec silencieux.** Mesuré : `GET /x.json` et `GET /x.woff2` renvoient **200 OK, `image/jpeg`, 2035 octets** (une image placeholder). Aucune erreur. Les fixtures ne peuvent donc pas être servies en `.json` statique.
3. **`launcher.py` copie `public/` dans `.game/`** au démarrage : tout fichier ajouté à `public/` est en 404 jusqu'au redémarrage. `launcher_fast.py` fait un symlink : édition à chaud. C'est la boucle de dev.
4. **Un verrou de version côté serveur peut servir `clean_cache.html` en 200 OK** à la place de n'importe quelle page si le cookie `app_version` est absent — soit des baselines silencieusement fausses.
5. **Le serveur ignore complètement les query strings sur les `.html`** (`/main.html?ui=old` renvoie les mêmes 6517 octets). `?ui=old` est donc **obligatoirement** une mécanique client, ce qui est une bonne nouvelle : zéro modification backend.
6. `scene.html` génère un **seed aléatoire à chaque chargement** (ligne ~786) et l'affiche : source de faux positifs garantie si on ne le masque pas.

**Primary recommendation :** `@playwright/test` 1.62.0 avec Chromium **bundled** (pas `channel: 'chrome'`), installé dans un dossier `ui-check/` à la racine du dépôt Desktop (chemin Windows natif), pointant sur le serveur WSL déjà lancé ; baselines committées ; validation avant/après par une page HTML générée maison (le rapport Playwright ne montre que les échecs, l'utilisateur veut voir tous les écrans côte à côte) ; fixtures `get_world` dumpées depuis une **copie** de `test_autoplay.py` et stockées en modules `.js` ESM sous `public/js/fixtures/` (seule extension servie de façon fiable).

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `@playwright/test` | **1.62.0** | Runner + captures + diff pixel + rapport HTML | Vérifié sur le registre npm le 2026-07-28 (`latest: 1.62.0`). Le diff d'image (pixelmatch), l'attente des polices, la désactivation des animations et le stockage des baselines sont **intégrés**. Aucune dépendance supplémentaire. |
| Chromium bundled Playwright | épinglé par 1.62.0 | Moteur de rendu des captures | Épinglé par la version de Playwright ⇒ rendu stable dans le temps. `npx playwright install chromium` (télécharge le build **win32**, aucun sudo nécessaire). |
| Node | node.exe Windows (v25.3.0) | Exécution du harnais | Seul Node disponible. Fonctionne, à condition de lancer depuis un chemin Windows natif. |
| Python 3.10 | `~/marvel-work/python/bin/python3.10` | Dump des fixtures `get_world` | Version imposée par le moteur. `python3.10` n'est **pas** dans le PATH : utiliser le chemin absolu. |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| (aucune) | — | — | Tout le reste est du script Node/Python maison de moins de 100 lignes. |

**Ne pas ajouter :** `pixelmatch`, `jest-image-snapshot`, `backstopjs`, `reg-suit`, `lost-pixel`. Playwright couvre le besoin ; toute dépendance en plus est une charge de maintenance sur un projet solo.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Chromium bundled | `channel: 'chrome'` (Chrome Windows déjà installé à `C:\Program Files\Google\Chrome\Application\chrome.exe`) | Évite un téléchargement de ~150 Mo, mais Chrome se met à jour tout seul → les baselines changent sans qu'on ait rien fait. **Rejeté** : la stabilité de la référence prime. |
| Exécution locale | Image Docker `mcr.microsoft.com/playwright` | C'est la recommandation de la littérature 2026, mais elle vise la cohérence **entre machines** (dev ↔ CI). Ici : une seule machine, un seul utilisateur, pas de CI, et un utilisateur non technique. Docker ajoute une couche à maintenir pour un problème qui n'existe pas. **Rejeté**, à réévaluer seulement si le projet gagne une CI. |
| Outillage dans WSL | Installer nvm + Node Linux dans WSL | Possible sans sudo, mais `npx playwright install-deps` (libnss3, libgbm…) **exige sudo avec mot de passe** (vérifié : `sudo -n` échoue). Chemin plus long pour un résultat identique. **Rejeté.** |
| Harnais dans `marvel-lcg-src/` | — | Le dossier est re-zippé vers `Fusion/` à chaque livraison : y mettre `node_modules` alourdirait le livrable. **Interdit.** |

**Installation :**

```bash
# Depuis un chemin Windows natif (obligatoire — voir Pitfall 1)
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
npm init -y
npm install -D @playwright/test@1.62.0
npx playwright install chromium
```

## Architecture Patterns

### Recommended Project Structure

Deux emplacements, séparés volontairement.

**A. Le harnais (dépôt Desktop, chemin Windows natif, versionné avec `.planning/`)**

```
"Marvel LCG"/
├── .planning/
└── ui-check/                      # tout l'outillage de non-régression
    ├── package.json               # scripts en français (voir plus bas)
    ├── playwright.config.ts
    ├── ecrans.ts                  # table des 5 écrans + 3 gabarits + masques
    ├── global-setup.ts            # pose le cookie app_version (Pitfall 4)
    ├── tests/
    │   ├── captures.spec.ts       # 5 écrans × 3 gabarits
    │   ├── lancement-partie.spec.ts  # contrat /new?data= gelé
    │   └── fixtures.spec.ts       # rendu des fixtures (utile dès la phase 5)
    ├── references/                # BASELINES committées (snapshotPathTemplate)
    │   └── <ecran>/<gabarit>.png
    ├── scripts/
    │   ├── comparer.mjs           # génère comparaison/index.html (avant/après)
    │   └── valider.mjs            # promeut les captures approuvées
    └── comparaison/               # sortie HTML, gitignorée
```

**B. Les fixtures et la bascule (dans le jeu, `~/marvel-work/fusion/marvel-lcg-src/`)**

```
marvel-lcg-src/
├── public/
│   ├── js/
│   │   ├── fixtures/              # NOUVEAU — modules .js ESM (voir Pattern 3)
│   │   │   ├── index.js           # catalogue { nom, titre FR, description }
│   │   │   └── <scenario>__<hero>__<NNN>__<phase>.js
│   │   └── ui-switch.js           # NOUVEAU — bascule ?ui=old (voir Pattern 4)
│   └── legacy/                    # NOUVEAU — copies verbatim des écrans migrés
└── (tools/ hors dépôt) ~/marvel-work/tools/dump_get_world.py   # NOUVEAU
```

**Règle :** rien dans `public/js/marvel/` n'est lu, modifié ou importé. Le nouveau code est une fonction pure de `get_world`.

---

### Pattern 1 : Table d'écrans déclarative, pas de test par écran

**Quoi :** un seul fichier de données décrit les écrans et les gabarits ; le spec les parcourt. Ajouter un écran = ajouter une ligne.

**Pourquoi :** l'utilisateur n'est pas technique. Une table lisible en français est le seul endroit qu'il aura à comprendre.

**Les 5 écrans** — repris à l'identique de `research/PITFALLS.md:102`, et confirmés servis en 200 par mesure :

| Clé | Titre FR | URL | Notes mesurées |
|---|---|---|---|
| `menu` | Menu principal | `/main.html` | 6517 o. Statique. |
| `preparation` | Préparation (ancienne) | `/scene.html` | 96849 o. **Seed aléatoire à masquer.** |
| `cartes` | Galerie de cartes | `/cards.html` | 30557 o. |
| `decks` | Gestion de decks | `/deck.html` | 22900 o. |
| `replay` | Replays | `/replay.html` | 12133 o. |

**À trancher par le planner :** `prepare.html` (le nouvel écran de préparation, déjà en service, 497 o + `js/prepare/app.js`) est un 6ᵉ candidat évident — c'est la page déjà en cours d'étranglement, et `main.html` propose déjà les deux (`Open('prepare.html')` **et** `Open('scene')`). Le coût marginal est d'une ligne. Recommandation : l'inclure, en le nommant `preparation-nouvelle`.

**Le plateau (`marvel.html`) n'est PAS capturé par URL.** Son état dépend d'une partie en cours : non déterministe, non reproductible, et une capture prise aujourd'hui ne sera jamais rejouable. C'est précisément le rôle du critère 2 (fixtures) : le plateau se baseline via le harnais de fixtures, pas via une URL.

**Les 3 gabarits** (issus du tableau mesuré de `research/PITFALLS.md`) :

| Clé | Titre FR | Viewport | Rationale |
|---|---|---|---|
| `pc` | Ordinateur | 1920 × 1080 | Cible principale actuelle |
| `tablette` | Tablette | 1180 × 820 | iPad Air paysage |
| `mobile` | Téléphone | 390 × 844 | iPhone 12/13/14 — le cas qui casse (scale 0.20 sur le plateau) |

Toujours `deviceScaleFactor: 1` et `scale: 'css'` : sinon les PNG pèsent 4× plus lourd pour zéro information supplémentaire.

---

### Pattern 2 : Deux commandes distinctes, jamais `-u` en direct

**Quoi :** séparer strictement « je vérifie » de « je valide un changement voulu ».

```jsonc
// ui-check/package.json
"scripts": {
  "captures":          "playwright test tests/captures.spec.ts",
  "captures:comparer": "playwright test tests/captures.spec.ts; node scripts/comparer.mjs",
  "captures:valider":  "node scripts/valider.mjs",
  "lancement":         "playwright test tests/lancement-partie.spec.ts"
}
```

- `npm run captures` : compare aux références. **Ne met jamais rien à jour.**
- `npm run captures:comparer` : compare **puis** génère `comparaison/index.html` — la page avant/après côte à côte demandée dans le CONTEXT — et l'ouvre.
- `npm run captures:valider` : demande une confirmation explicite en français (« Tu as bien regardé la page de comparaison ? Écris OUI pour figer les nouvelles images comme référence. ») puis lance `playwright test -u`.

**Pourquoi ce découpage :** la décision utilisateur du CONTEXT est « pas de mise à jour silencieuse des baselines ». `-u` mis à disposition directement finirait par être tapé par réflexe.

**Anti-pattern :** se reposer sur le rapport HTML de Playwright pour la validation. Il n'affiche **que les tests en échec**, en anglais, avec un vocabulaire technique (Expected/Actual/Diff). L'utilisateur veut voir **tous** les écrans, avant/après, en français. D'où `scripts/comparer.mjs` (une page statique d'une centaine de lignes, deux `<img>` par ligne + un curseur). Garder `reporter: [['html', { open: 'never' }]]` pour le diagnostic technique, mais ce n'est pas l'interface de validation.

---

### Pattern 3 : Fixtures `get_world` en modules `.js` ESM

**Quoi :** chaque fixture est un fichier `public/js/fixtures/<nom>.js` contenant `export default { ... };` — le JSON exact que `/get_world` renvoie.

**Pourquoi pas du `.json` :** **mesuré** — `GET /quelquechose.json` renvoie `200 OK`, `image/jpeg`, 2035 octets. Le `.json` n'est pas dans la liste blanche d'extensions et tombe dans le fourre-tout `/{path:.+}` → `handle_image_request` → image placeholder. `fetch()` réussirait et `response.json()` planterait sur un JPEG : échec incompréhensible.

`.js` est dans la liste blanche (vérifié : `/public/js/prepare/app.js` → 200 `application/javascript`). Un module ESM est lisible **à la fois** par le navigateur (`await import('/public/js/fixtures/x.js')`) et par Node dans les tests. Un seul artefact, zéro dépendance serveur.

**Solution de repli documentée :** `GET /read_file?<chemin>` sert n'importe quel JSON depuis le dossier du jeu (vérifié : `/read_file?data/sets_info.json` → 200 `application/json`, gzip). Renvoie **500** si le fichier n'existe pas. Utile à connaître, mais moins robuste que `.js`.

**Où dumper — point d'accroche exact.** `handle_get_world` fait littéralement :

```python
# src/engine/device/web/server/server_sync.py:58-69
data = controller.world.render.descriptor
compressed_data = Json.DumpGZip(data)
```

Donc `Json.Dumps(game.world.render.descriptor)` produit exactement le même contenu que `/get_world`, sans gzip. Le hook est la fonction `auto_input` de `test_autoplay.py`, appelée à chaque `DoGetInput` avec le monde in-process accessible en global `game`.

**Ne pas modifier `test_autoplay.py`** : c'est un outil validé (baseline 0 traceback). Créer `~/marvel-work/tools/dump_get_world.py` — copie de `test_autoplay.py` avec le dump ajouté.

**Sélection des 20-40 fixtures.** Une partie fait jusqu'à 900 asks : dumper tout est inexploitable. Sélectionner par **prédicat sur le descripteur**, un seul dump par prédicat et par run :

| Nom du cas | Prédicat sur le `WorldDescriptor` |
|---|---|
| `mise-en-place` | premier `render_id` avec `phase == 'Scenario Setup'` |
| `debut-de-tour` | premier `round_id == 1` |
| `main-pleine` | `max(len(p.hand_cards))` du run |
| `side-scheme` | `area_schemes_side` non vide (première occurrence) |
| `sbire-en-jeu` | présence d'un `Minion` dans `area_villain` |
| `defausse-rencontre-pleine` | `len(encounter_discard_pile)` maximal |
| `deck-rencontre-vide` | `len(encounter_deck) == 0` |
| `carte-mise-de-cote` | `area_set_aside` non vide |
| `zone-victoire` | `victory_display` non vide |
| `statuts` | `area_status_cards` non vide |
| `fin-de-partie` | `prompt_last_text` commence par `"\n--- Game Over ---"` (c'est le test exact fait par `client.js:doGetWorld`) |
| `stade-2`, `stade-3` | changement du `id` de `area_schemes_main[0]` |

Faire tourner le dumper sur 4-6 couples scénario/héros différents (les combos déjà validés par l'autoplay) × ~8 prédicats ⇒ 30-40 fixtures naturellement. Nommage : `<scenario>__<hero>__<cas>.js`.

**Rejouabilité (critère 2).** Deux niveaux, dans cet ordre :

1. **Immédiat, sans nouvelle UI (Phase 1) :** une page `public/fixtures.html` autonome (nouveau fichier, ne touche pas `js/marvel/`) qui liste les fixtures depuis `index.js` et affiche, pour la fixture choisie, un rendu texte structuré : phase, tour, prompt, et le contenu de chaque zone (nom de carte, dégâts, menace, prêt/épuisé). ~150 lignes, zéro dépendance. Cela **prouve** le critère « afficher un état de plateau sans lancer une partie réelle » et sert de premier consommateur de `get_world` comme fonction pure.
2. **À partir de la Phase 5 :** la même page monte le vrai renderer React à la place du rendu texte. Le contrat (`import` d'une fixture → props) ne bouge pas.

**Anti-pattern :** faire rejouer une fixture en monkey-patchant `window.fetch` dans `marvel.html` pour tromper le runtime existant. Ça « marche » en démo mais viole l'esprit de l'intouchabilité (le comportement dépend alors de la connaissance du protocole interne : `/ws`, `/get_ask`, `/client_updated`), et ça se casse au premier état que le runtime refuse. Le nouveau code doit être une fonction pure de `get_world`, point.

---

### Pattern 4 : Bascule `?ui=old` — 100 % client, mémorisée

**Contraintes mesurées :**
- Le serveur ignore les query strings sur les `.html` : `/main.html?ui=old` → 200, mêmes 6517 octets. Aucune bascule serveur possible (et interdite : zéro modification backend).
- Les sous-dossiers de `public/` fonctionnent pour `.html` / `.css` / `.js` (`ReadFile` cherche dans `./public/`), mais **exigent un redémarrage** sous `launcher.py` (voir Pitfall 3).
- Les pages existantes référencent leurs assets en absolu (`/public/css/menu/style.css`) : **déplacer un `.html` ne casse pas ses liens.** C'est ce qui rend le motif ci-dessous quasi gratuit.
- La query string est **perdue** au lancement d'une partie : `js/prepare/launcher.js` fait `window.location.href = "/?hot_seat"`. La préférence doit donc survivre à une navigation ⇒ `localStorage`.

**Mécanique recommandée (5 étapes) :**

1. Avant de migrer `X.html`, le copier **verbatim** en `public/legacy/X.html`. Ce fichier n'est plus jamais touché.
2. Le nouveau `public/X.html` commence par un aiguillage inline, **tout premier élément du `<head>`**, avant tout CSS/JS (pas de flash) :

```html
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var choix = q.get('ui');                       // 'old' | 'new' | null
  if (choix === 'old' || choix === 'new') {
    try { localStorage.setItem('ui', choix); } catch (e) {}
  } else {
    try { choix = localStorage.getItem('ui'); } catch (e) { choix = null; }
  }
  if (choix === 'old') {
    location.replace('/legacy/X.html' + location.hash);
  }
})();
</script>
```

3. Chaque page `legacy/` reçoit **une seule ligne** : `<script src="/public/js/ui-switch.js"></script>`. Ce script injecte un bandeau non technique en haut de page : « **Vous utilisez l'ancienne version.** [Revenir à la nouvelle version] », le bouton faisant `localStorage.setItem('ui','new')` puis retour à la page moderne.
4. Chaque page moderne expose un lien discret « Revenir à l'ancienne version » (même script partagé, `ui-switch.js`, qui détecte le contexte).
5. Le plateau est un cas particulier : il est servi par `/` et `/watch` **avec query string non vide** (`handle_marvel` : `query_string == '' → main.html`, sinon `marvel.html`). Sa copie legacy est donc adressée par nom de fichier (`/legacy/marvel.html`), et l'aiguillage vit en tête de `marvel.html`. À vérifier au moment de la Phase 5, pas maintenant.

**Pourquoi `localStorage` et pas un cookie :** un cookie serait envoyé au serveur, ce qui suggère à tort une bascule serveur. `localStorage` dit clairement « c'est une préférence de navigateur ». Et le serveur pose déjà deux cookies (`session_token`, `app_version`) qu'il ne faut pas risquer de perturber.

**Livrable Phase 1 :** l'aiguillage + `ui-switch.js` + le dossier `legacy/` **existent et sont démontrés sur au moins une page réelle** (le meilleur candidat est `prepare.html` ↔ `scene.html`, déjà en coexistence). Le critère 3 (« sur toute page en cours de migration ») se vérifie par ce précédent, pas en migrant tout.

---

### Pattern 5 : Geler le contrat `/new?data=`

**Contrat mesuré** (`server_new_game.py:14-18` + `js/prepare/launcher.js`) :

```
GET /new?data=<encodeURIComponent(JSON.stringify(descriptor))>
→ 200 {"result": "New game created"}
puis le client navigue vers "/?hot_seat"
```

`descriptor` (`NewGameDescriptor`, désérialisé par `Json.LoadsAs`) :

| Clé | Type | Observé |
|---|---|---|
| `campaign_json` | string | JSON du scénario **sérialisé en chaîne** |
| `encounter_set_names` | string[] | `raw.encounter_sets` + sets modulaires, dédupliqués |
| `hero_json` | string[] | un JSON de deck **sérialisé en chaîne** par joueur |
| `seed` | int | `-1` = aléatoire |
| `timeout` | int | `0` |
| `challenges` | any[] | `raw.challenges \|\| []` |
| `rules` | string[] | `mode_skirmish`, `mode_campaign`, `mode_heroic_<n>`, `v16_all`, `no_crisis_of_infinite_deadpools`, `no_encounter_cards_ignore_crisis` |
| `campaign_log` | object | `{}` par défaut |

**Le test doit faire deux choses**, pas une :

1. **Geler la charge utile.** Intercepter la requête (`page.waitForRequest(/\/new\?data=/)`), décoder le JSON, et comparer à un golden committé — au minimum l'**ensemble des clés** et le type de chaque valeur (le contenu exact du deck varie). Toute évolution du contrat fait échouer le test bruyamment. C'est ça, « contrat gelé ».
2. **Vérifier qu'on atteint le plateau.** Après la navigation, interroger `GET /get_world?p=0` en boucle jusqu'à `render_id > 0` et `phase` non vide. Mesuré sur le serveur en cours : `{"render_id": 22, "round_id": 0, "phase": "Scenario Setup", ...}`. C'est un signal fiable et bien plus stable que d'attendre un sélecteur DOM du runtime existant.

Ajouter en complément un test **sans navigateur** (`fetch` direct sur `/new?data=<golden>`) : il garde le contrat vérifié même si l'UI de préparation est en chantier.

### Anti-Patterns to Avoid

- **Ajouter une route backend** pour servir les fixtures, les baselines ou la bascule. La contrainte est zéro modification backend et la liste blanche existante suffit (`.html`, `.css`, `.js`).
- **Mettre à jour une baseline « parce que le test est rouge ».** Une référence qui bouge sur un écran qu'on n'a pas touché est exactement le signal recherché (`research/PITFALLS.md:104`).
- **Baseliner le plateau depuis une partie live.** Non reproductible. Ce sont les fixtures qui font ce travail.
- **Installer le harnais dans `marvel-lcg-src/`.** Il partirait dans le zip de livraison.
- **Lire `public/js/marvel/` pour « comprendre le format ».** Le format est `WorldDescriptor` (`src/game/render/descriptor/world.py`), qui est lisible et suffisant.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Comparaison d'images | Boucle sur pixels / `pixelmatch` à la main | `expect(page).toHaveScreenshot()` | pixelmatch est intégré, avec anti-aliasing (`threshold: 0.2`), tolérance (`maxDiffPixels`, `maxDiffPixelRatio`), masques et génération du PNG de diff |
| Attendre que la page soit « stable » | `waitForTimeout(2000)` | `toHaveScreenshot()` | Il désactive les animations (`animations: 'disabled'` par défaut), cache le curseur (`caret: 'hide'` par défaut), attend `document.fonts.ready` et **réessaie jusqu'à deux captures consécutives identiques** |
| Stocker/nommer les baselines | Arborescence maison | `snapshotPathTemplate` | Une ligne de config donne `references/<ecran>/<gabarit>.png` |
| Parallélisme, réessais, rapport | Script shell | `@playwright/test` | Inclus |
| Un état de plateau de test | Écrire un faux `get_world` à la main | Dump du vrai descripteur depuis l'autoplay | Un état de Marvel Champions a des dizaines de zones et d'invariants ; un faux sera faux et testera la mauvaise chose |
| Servir du JSON | Nouvelle route serveur | Modules `.js` ESM | `.json` renvoie une image (mesuré) |
| Détecter une régression fonctionnelle du moteur | Nouveau harnais | `test_autoplay.py` existant | Déjà validé, 0 traceback, et c'est déjà le critère de livraison |

**Insight clé :** dans ce projet, la tentation du sur-mesure ne vient pas de l'outillage de test (Playwright couvre tout) mais du **contournement des contraintes serveur**. Chaque fois qu'un fichier « ne se charge pas », le réflexe correct est de vérifier l'extension contre la liste blanche, pas d'écrire un chargeur.

## Common Pitfalls

### Pitfall 1 : `node` = Windows, et le dossier de travail est un chemin UNC

**Ce qui se passe :** `~/.local/bin/node` est un lien vers `/mnt/c/Program Files/nodejs/node.exe`. Il n'y a **aucun Node natif Linux**. Depuis un dossier WSL, `process.cwd()` vaut `\\wsl.localhost\Ubuntu\home\arnau` — un chemin UNC. `npm` résout aussi vers `/mnt/c/Program Files/nodejs/npm`.
**Mesures :** `node -e "console.log(process.platform, process.cwd())"` → `win32 \\wsl.localhost\Ubuntu\home\arnau`. `npm init -y` dans `/tmp` fonctionne (Windows 11 gère `\\wsl.localhost`), mais l'accès UNC est lent et fragile sur une arborescence `node_modules`.
**Comment l'éviter :** installer `ui-check/` sous `/mnt/c/Users/arnau/Desktop/Marvel LCG/` (= `C:\Users\arnau\Desktop\...`, chemin Windows natif). Lancer toutes les commandes npm depuis là.
**Vérifié :** Windows node atteint le serveur WSL — `fetch('http://127.0.0.1:2345/main.html')` → 200, 6516 octets ; `fetch('http://localhost:2345/get_world?p=0')` → 200. La redirection localhost de WSL2 fonctionne, aucune configuration réseau à faire.
**Signes d'alerte :** `EPERM`/`ENOENT` inexpliqués à l'install ; `UNC paths are not supported` ; scripts npm très lents.

---

### Pitfall 2 : Extensions hors liste blanche → 200 OK avec une image vide

**Ce qui se passe :** le serveur enregistre des routes par extension puis un fourre-tout `/{path:.+}` → `handle_image_request` → `Cache.LoadImage(basename)`. Toute extension non listée renvoie une **image placeholder en 200**. Rien n'échoue visiblement.
**Mesuré :** `GET /nonexistent.json` → `200, image/jpeg, 2035 o`. `GET /nonexistent.woff2` → idem.
**Liste blanche réelle** (`web_server.py:258-277`, ordre d'enregistrement) :

| Extension | Dossiers cherchés | Remarque |
|---|---|---|
| `.html` | `./`, `./public/`, `./public/blueprints` | sous-dossiers OK |
| `.css` | `./`, `./public/css`, `./public/` | sous-dossiers OK |
| `.js` | `./`, `./public/js`, `./public/` | sous-dossiers OK |
| `.ts`, `.js.map` | idem | **404 en mode RELEASE** |
| `.mp3`, `.wav` | dossiers de sons | |
| `.eot`, `.woff`, `.ttf` | `./public/fonts` **uniquement, à plat** (le chemin est réduit au nom de fichier) | |
| `.svg` | `TEXTURE_FOLDER` **uniquement, à plat** | |
| `.gif` | renvoie toujours `sparkles.gif` | |

**Absents et donc cassés :** `.woff2`, `.png`, `.jpg`, `.webp`, `.json`, `.mjs`, `.map` seul, `.webmanifest`, `.avif`, `.ico` (sauf `/favicon.ico` en route exacte).
**Comment l'éviter :** fixtures en `.js`. Et pour la Phase 2 (build Vite), c'est LA contrainte à retenir : `assetFileNames` ne doit produire que des extensions de la liste, les polices doivent finir à plat dans `public/fonts/` en `.woff`/`.ttf` (pas `.woff2`), et les images doivent être inlinées en base64 ou passer par les routes d'images existantes.
**Signes d'alerte :** une police qui ne s'applique pas sans erreur console ; un `fetch(...).json()` qui échoue sur `Unexpected token`.

---

### Pitfall 3 : `public/` est **copié** dans `.game/` — les nouveaux fichiers sont en 404

**Ce qui se passe :** `launcher.py` copie `data/ deck/ public/ puzzle/ assets/` dans `.game/` puis `chdir` dedans. Un fichier ajouté à `public/` après le démarrage n'existe pas pour le serveur.
**Mesuré :** création de `public/_probe/sub/legacy.html` et `public/js/_probe.js` sur le serveur en cours (lancé par `launcher.py`, PID 180492) → **404** sur les deux. `.game/public` est bien un répertoire (copie), pas un lien.
**Comment l'éviter :** utiliser `launcher_fast.py` pour la boucle de dev — il fait un **symlink** de `public/` (documenté en tête du fichier : « les modifications de `public/` sont prises en compte sans rien recopier »). Le premier plan de la phase doit acter ce point : **la boucle de dev, c'est `launcher_fast.py`.**
**Effet de bord à connaître :** `launcher_fast.py` patche `WebServer.IsAuthenticate` et `IsVersionMatch` à `True` (lignes 157-159). `launcher.py` **non**. Voir Pitfall 4.
**Signes d'alerte :** « j'ai créé le fichier, il est en 404 » ; une modification CSS sans effet après rechargement forcé.

---

### Pitfall 4 : Le verrou de version sert `clean_cache.html` en 200 OK

**Ce qui se passe :** `IsVersionMatch` (`web_server.py:81-89`) renvoie `False` si le cookie `app_version` est **absent** ou différent de `Ver.ui_version_str`. Toutes les routes protégées renvoient alors `clean_cache.html` — avec un **statut 200**. Un navigateur neuf (contexte Playwright = cookies vides) capturerait donc cinq fois la même page d'avertissement, en pensant avoir baseliné cinq écrans.
**Pourquoi c'est piégeux ici :** le serveur de dev (`launcher_fast.py`) désactive ce contrôle, le serveur de livraison (`launcher.py`) non. Le piège ne se déclenche donc que le jour où on rebaseline contre le vrai serveur.
**Comment l'éviter — deux ceintures :**
1. `global-setup.ts` : `await page.goto('/get_version')` une fois (la route pose le cookie, `httponly=false`, `need_auth=false`), puis sauvegarder l'état via `storageState`.
2. **Garde-fou de contenu** dans chaque test, avant la capture : asserter un marqueur propre à l'écran (`await expect(page).toHaveTitle(/Marvel/)`, ou la présence d'un `#id` connu). Une capture n'est prise que si la bonne page est là.
**Signes d'alerte :** cinq baselines de tailles très proches ; une baseline qui contient le mot « cache ».

---

### Pitfall 5 : `scene.html` tire un seed aléatoire à chaque chargement

**Ce qui se passe :** `scene.html` ligne ~786 : `random_seed()` est appelé au chargement et écrit `Math.floor(Math.random() * (2**31-2) + 1)` dans `#seed_div`. Le nombre est visible. Chaque capture diffère.
**Comment l'éviter :** `mask: [page.locator('#seed_div')]` (Playwright peint la zone en `#FF00FF`), **ou** `page.addInitScript(() => { Math.random = () => 0.42; })` avant `goto` — plus propre car le layout reste identique. Recommandation : `addInitScript`, plus `mask` en filet.
Autre `Math.random` dans le même fichier (`getRandomElements`, ligne ~1450), déclenché sur interaction et non au chargement : couvert d'office par le stub.
**Signes d'alerte :** un test rouge sur `preparation` uniquement, avec un diff minuscule au même endroit.

---

### Pitfall 6 : Les images de cartes peuvent partir chercher le réseau

**Ce qui se passe :** `Cache.LoadImage` cherche dans `image_folders`, puis, **si le nom correspond à `^\d{5}[a-z]?$`**, télécharge depuis `cerebrodatastorage.blob.core.windows.net` ou `marvelcdb.com` (configurés dans `launch.json`). Une image manquante = latence réseau, timeout, ou image différente selon le jour.
**Atténuation existante :** `image_folders` pointe sur `./assets/pics/` (387 fichiers) **et** sur `/mnt/c/.../Jeux original/assets/pics/` (**4263 fichiers**) — la bibliothèque est donc locale et complète en pratique.
**Comment l'éviter :** dans la config Playwright, bloquer explicitement le réseau externe et faire échouer le test si une requête sort :

```ts
await page.route('**://*/**', route => {
  const h = new URL(route.request().url()).hostname;
  return (h === '127.0.0.1' || h === 'localhost') ? route.continue() : route.abort();
});
```
Faire une passe de chauffe (`npm run captures` une fois, jetée) avant de figer les premières références.
**Signes d'alerte :** un run de captures qui dure beaucoup plus longtemps que le précédent ; des vignettes manquantes de façon intermittente.

---

### Pitfall 7 : `/new?data=` détruit la partie en cours

**Ce qui se passe :** `new_game` appelle `self.game.NewGame(...)` sur l'instance unique. Lancer le test E2E pendant que l'utilisateur joue perd sa partie.
**Comment l'éviter :** garder `npm run lancement` **séparé** de `npm run captures` (qui est en lecture seule), et afficher un avertissement en français au démarrage du script : « Attention : ce test lance une nouvelle partie. Si tu as une partie en cours, termine-la ou sauvegarde-la avant. » Ne pas tenter de lancer une seconde instance du serveur : `launcher_fast.py` et `launcher.py` écrivent tous deux dans le même `.game/` et le même `launch.json`, deux instances se marcheraient dessus.

---

### Pitfall 8 : Générer les références sur une machine, les vérifier sur une autre

**Ce qui se passe :** c'est LE sujet de la littérature 2026 sur le sujet — le rendu des polices diffère entre OS, d'où la recommandation Docker.
**Pourquoi ça ne s'applique pas ici :** une seule machine, un seul utilisateur, pas de CI. Le vrai risque de dérive est la **mise à jour du navigateur**.
**Comment l'éviter :** Chromium bundled (épinglé par la version de Playwright) et non `channel: 'chrome'` ; épingler `@playwright/test@1.62.0` **sans accent circonflexe** dans `package.json` ; traiter toute montée de version de Playwright comme un événement qui exige une re-validation des références (avec la page de comparaison).

---

### Pitfall 9 : `?ui=old` perdu à la navigation

**Ce qui se passe :** `js/prepare/launcher.js` fait `window.location.href = "/?hot_seat"` après la création de la partie. La query string disparaît. Si la bascule ne vivait que dans l'URL, l'utilisateur repartirait sur la nouvelle UI juste au moment critique (l'entrée en partie).
**Comment l'éviter :** `localStorage`, avec `?ui=old` en simple point d'entrée. Vérifier le cas concret « je choisis l'ancienne version → je lance une partie → j'arrive bien sur l'ancien plateau » comme critère d'acceptation.

## Code Examples

### `ui-check/playwright.config.ts`

```ts
// Source: https://playwright.dev/docs/test-configuration + https://playwright.dev/docs/api/class-pageassertions
import { defineConfig } from '@playwright/test';

const GABARITS = {
  pc:       { width: 1920, height: 1080 },
  tablette: { width: 1180, height: 820 },
  mobile:   { width: 390,  height: 844 },
};

export default defineConfig({
  testDir: './tests',
  globalSetup: './global-setup.ts',
  fullyParallel: false,          // une seule instance de jeu, pas de concurrence
  retries: 0,
  reporter: [['list'], ['html', { open: 'never' }]],

  // references/<ecran>/<gabarit>.png  — noms lisibles par un humain
  snapshotPathTemplate: '{testDir}/../references/{arg}/{projectName}{ext}',

  use: {
    baseURL: 'http://127.0.0.1:2345',
    storageState: './.auth/state.json',   // cookie app_version (global-setup)
    deviceScaleFactor: 1,
    reducedMotion: 'reduce',
  },

  expect: {
    toHaveScreenshot: {
      // threshold: 0.2 et animations:'disabled', caret:'hide' sont les défauts
      maxDiffPixelRatio: 0.002,   // ~0.2 % : absorbe l'antialiasing, pas un décalage réel
      scale: 'css',
    },
  },

  projects: Object.entries(GABARITS).map(([name, viewport]) => ({
    name,
    use: { viewport },
  })),
});
```

### `ui-check/global-setup.ts` — poser le cookie de version

```ts
import { chromium, type FullConfig } from '@playwright/test';
import fs from 'node:fs';

export default async function globalSetup(config: FullConfig) {
  const base = 'http://127.0.0.1:2345';
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();

  // /get_version pose le cookie app_version (need_auth: false, httponly: false).
  // Sans ce cookie, TOUTES les pages renvoient clean_cache.html en 200 OK.
  await page.goto(`${base}/get_version`);

  // Garde-fou : si le menu ne se charge pas, on arrête tout de suite,
  // plutôt que de baseliner cinq pages d'avertissement.
  await page.goto(`${base}/main.html`);
  const titre = await page.title();
  if (!/Marvel/i.test(titre)) {
    throw new Error(
      `Le serveur ne sert pas le menu (titre reçu : "${titre}"). ` +
      `Le jeu est-il bien lancé sur ${base} ?`
    );
  }

  fs.mkdirSync('./.auth', { recursive: true });
  await ctx.storageState({ path: './.auth/state.json' });
  await browser.close();
}
```

### `ui-check/ecrans.ts` — la table que l'utilisateur peut lire

```ts
export type Ecran = {
  cle: string;
  titre: string;      // affiché dans la page de comparaison
  url: string;
  marqueur: string;   // sélecteur qui prouve que la bonne page est chargée
  masques?: string[]; // zones à neutraliser
};

export const ECRANS: Ecran[] = [
  { cle: 'menu',         titre: 'Menu principal',          url: '/main.html',    marqueur: '.menu' },
  { cle: 'preparation',  titre: 'Préparation (ancienne)',  url: '/scene.html',   marqueur: '#mode', masques: ['#seed_div'] },
  { cle: 'cartes',       titre: 'Galerie de cartes',       url: '/cards.html',   marqueur: 'body' },
  { cle: 'decks',        titre: 'Gestion de decks',        url: '/deck.html',    marqueur: 'body' },
  { cle: 'replay',       titre: 'Replays',                 url: '/replay.html',  marqueur: 'body' },
  // Candidat 6e écran (déjà en cours d'étranglement) :
  // { cle: 'preparation-nouvelle', titre: 'Préparation (nouvelle)', url: '/prepare.html', marqueur: '#app' },
];
```

### `ui-check/tests/captures.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { ECRANS } from '../ecrans';

test.beforeEach(async ({ page }) => {
  // Aucun accès réseau externe : les images de cartes doivent venir du disque.
  await page.route('**://*/**', route => {
    const h = new URL(route.request().url()).hostname;
    return (h === '127.0.0.1' || h === 'localhost') ? route.continue() : route.abort();
  });
  // Neutralise les seeds aléatoires (scene.html les tire au chargement).
  await page.addInitScript(() => { Math.random = () => 0.42; });
});

for (const ecran of ECRANS) {
  test(ecran.titre, async ({ page }) => {
    await page.goto(ecran.url, { waitUntil: 'networkidle' });
    await expect(page.locator(ecran.marqueur).first()).toBeVisible();

    await expect(page).toHaveScreenshot(`${ecran.cle}.png`, {
      fullPage: true,
      mask: (ecran.masques ?? []).map(s => page.locator(s)),
    });
  });
}
```

### `ui-check/tests/lancement-partie.spec.ts` — geler `/new?data=`

```ts
import { test, expect } from '@playwright/test';

test('une partie se lance et atteint le plateau', async ({ page, baseURL }) => {
  await page.goto('/prepare.html');

  // ... pilotage du wizard (héros, deck, scénario, difficulté) ...

  const [requete] = await Promise.all([
    page.waitForRequest(/\/new\?data=/),
    page.getByRole('button', { name: /lancer/i }).click(),
  ]);

  // 1) Le contrat est gelé : les clés du descripteur ne bougent pas.
  const brut = decodeURIComponent(new URL(requete.url()).searchParams.get('data')!);
  const d = JSON.parse(brut);
  expect(Object.keys(d).sort()).toEqual([
    'campaign_json', 'campaign_log', 'challenges', 'encounter_set_names',
    'hero_json', 'rules', 'seed', 'timeout',
  ]);
  expect(typeof d.campaign_json).toBe('string');
  expect(Array.isArray(d.hero_json)).toBe(true);
  expect(d.rules).toContain('v16_all');

  // 2) Le moteur démarre vraiment : get_world finit par répondre un monde.
  await expect.poll(async () => {
    const r = await page.request.get('/get_world?p=0');
    const w = await r.json();
    return w.render_id;
  }, { timeout: 60_000, intervals: [1000] }).toBeGreaterThan(0);
});
```

### `~/marvel-work/tools/dump_get_world.py` — le hook exact

```python
# Copie de test_autoplay.py. SEULE différence : le dump ci-dessous.
# handle_get_world fait Json.DumpGZip(controller.world.render.descriptor) ;
# Json.Dumps du même objet donne donc exactement le contenu de /get_world.
from engine.lib import Json
import os, re

SORTIE = os.path.expanduser('~/marvel-work/fusion/marvel-lcg-src/public/js/fixtures')
deja_vus = set()

def peut_etre_dumper(d):
    """Renvoie un nom de cas si l'état mérite d'être conservé, sinon None."""
    if d.prompt_last_text.startswith('\n--- Game Over ---'): return 'fin-de-partie'
    if d.area_schemes_side:                                   return 'side-scheme'
    if not d.encounter_deck:                                  return 'deck-rencontre-vide'
    if d.area_set_aside:                                      return 'carte-mise-de-cote'
    if d.victory_display:                                     return 'zone-victoire'
    if d.area_status_cards:                                   return 'statuts'
    if d.phase == 'Scenario Setup':                           return 'mise-en-place'
    return None

def dump_si_interessant():
    d = game.world.render.descriptor
    cas = peut_etre_dumper(d)
    if not cas or cas in deja_vus:
        return
    deja_vus.add(cas)
    nom = re.sub(r'[^a-z0-9_-]', '-', f'{SCENARIO}__{HERO}__{cas}'.lower())
    os.makedirs(SORTIE, exist_ok=True)
    with open(f'{SORTIE}/{nom}.js', 'w', encoding='utf-8') as f:
        f.write('// Généré par dump_get_world.py — ne pas éditer à la main.\n')
        f.write('export default ' + Json.Dumps(d, indent=1) + ';\n')
    print(f'[FIXTURE] {nom} (render_id={d.render_id})', flush=True)

# Dans auto_input(), tout au début :
#     dump_si_interessant()
```

Lancement :

```bash
export RELEASE=1
PY=~/marvel-work/python/bin/python3.10
GAME=~/marvel-work/fusion/marvel-lcg-src
$PY ~/marvel-work/tools/dump_get_world.py $GAME 8801 rhino spider_man
$PY ~/marvel-work/tools/dump_get_world.py $GAME 8802 klaw captain_marvel
# ... 4 à 6 couples pour atteindre 20-40 fixtures
```

### Aiguillage `?ui=old` — voir Pattern 4 pour le snippet complet

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| `page.screenshot()` + comparaison maison | `expect(page).toHaveScreenshot()` | Playwright 1.23 (2022) | Diff, tolérance, masques, attente de stabilité intégrés |
| `waitForTimeout` avant capture | `animations: 'disabled'` (défaut) + attente de `document.fonts.ready` + double capture identique | intégré depuis longtemps, défaut aujourd'hui | Supprime la principale source de faux positifs |
| `-u` binaire (tout ou rien) | `--update-snapshots=all\|changed\|missing\|none` (`changed` = défaut du flag) | flags actuels vérifiés dans la doc CLI | Permet d'accepter précisément ce qui a été validé |
| Baselines générées localement | Baselines générées en CI dans l'image Docker Playwright | consensus 2026 | **Ne s'applique pas ici** : une machine, pas de CI. La stabilité vient de l'épinglage de version. |

**Obsolète / à ne pas utiliser :**
- `channel: 'chrome'` pour du visual regression : mises à jour automatiques ⇒ dérive des références.
- BackstopJS / `jest-image-snapshot` : redondants avec Playwright.
- `.ts` et `.js.map` servis par le serveur : **404 en mode RELEASE** (`handle_ts`, `handle_js_map`). Ne pas compter dessus pour du debug — pertinent dès la Phase 2 (sourcemaps Vite).

## Open Questions

1. **Le `render.descriptor` est-il à jour au moment de `DoGetInput` ?**
   - Ce qu'on sait : `handle_get_world` lit `controller.world.render.descriptor` sans le recalculer ; le client fait `fetch('get_world?p=0')` puis affiche puis répond. Il est donc très probable que le descripteur soit celui du rendu courant au moment de l'ask.
   - Ce qui reste flou : on n'a pas prouvé qu'aucun rendu intermédiaire n'est écrasé entre le rendu et l'ask.
   - Recommandation : **première tâche du plan de fixtures** — dumper une fixture, mettre l'autoplay en pause à cet ask, faire `curl /get_world?p=0 --compressed` et comparer les deux JSON. Cinq minutes, et ça sécurise tout le reste. (Le serveur en cours répond bien : `render_id: 22`, `phase: "Scenario Setup"`.)

2. **5 ou 6 écrans ?** `research/PITFALLS.md:102` liste exactement `main.html`, `scene.html`, `cards.html`, `deck.html`, `replay.html`. `prepare.html` existe déjà et est la cible de l'étranglement. Recommandation : 6 (coût marginal nul), en gardant les 5 historiques comme le noyau exigé par le critère.

3. **`scene.html` : un seul écran ou ses 4 étapes ?** PITFALLS parle de « `scene.html` (4 étapes) ». Les étapes sont des `<details>` dans une même page. Recommandation : une capture `fullPage` de la page tout ouverte (simple, couvre tout) ; ajouter des captures par étape seulement si la Phase 4 le demande.

4. **Où committer les références ?** Le dépôt Desktop est un dépôt git avec `.planning/` suivi, mais `Fusion/`, `Claude/`, `Chatgpt/`, `Jeux original/` non suivis. 6 écrans × 3 gabarits = 18 PNG, quelques Mo. Recommandation : committer `ui-check/` (dont `references/`) et gitignorer `node_modules/`, `comparaison/`, `test-results/`, `playwright-report/`, `.auth/`.

5. **Combien de couples scénario/héros pour les fixtures ?** L'autoplay tourne sur « 7+ combos » selon la recherche, mais la liste exacte des combos validés n'est pas écrite dans les documents lus. À récupérer auprès de l'utilisateur ou dans `~/marvel-work/TODO.md` avant d'écrire le plan.

6. **Multi-héros.** Le CONTEXT cite « multi-héros » parmi les moments à couvrir, mais `dump_get_world.py` (comme `test_autoplay.py`) lance `SceneLoader.NewScene(SCENARIO, None, [HERO], 42)` — un seul héros. Ajouter un second héros à la liste est probablement suffisant, mais le bot n'a jamais été exercé dans cette configuration : à valider avant de le mettre dans le plan.

## Sources

### Primary (HIGH confidence) — mesuré ou lu dans le code local

- Serveur en cours d'exécution `http://127.0.0.1:2345` (PID 180492, `launcher.py`) — 16 requêtes de sonde : codes, `content-type`, tailles. C'est la source des Pitfalls 2, 3, 4 et de la table des 5 écrans.
- `~/marvel-work/fusion/marvel-lcg-src/src/engine/network/web_server.py` — liste blanche d'extensions (258-277), `IsVersionMatch` (81-89), `ReadFile` (130-164)
- `.../src/engine/device/web/server/server_files.py` — fourre-tout `/{path:.+}` (37), `handle_marvel` (11-14)
- `.../src/engine/device/web/server/server_sync.py` — `handle_get_world` (58-69)
- `.../src/engine/device/web/server/server_new_game.py` — `new_game` (14-18)
- `.../src/engine/device/web/server/server_html.py`, `server_get.py` — routes `/main`, `/scene`, `/read_file`
- `.../src/game/render/descriptor/world.py` — schéma complet de `WorldDescriptor`
- `.../src/engine/file/cache.py` — `LoadImage`, condition de téléchargement `^\d{5}[a-z]?$`
- `.../src/engine/lib/mime_type.py` — table MIME (à ne pas confondre avec la liste blanche de routage)
- `.../launcher_fast.py` (symlinks + patch d'auth), `.../launcher.py` (copies)
- `.../public/scene.html:786` (`random_seed()`), `.../public/main.html:169-172`, `.../public/js/prepare/launcher.js` (contrat `/new?data=`), `.../public/js/marvel/client.js:180` (`get_world?p=0`)
- `~/marvel-work/tools/test_autoplay.py` — point d'accroche `auto_input`
- Environnement : `node -e` (platform/cwd), `type -a npm`, `ls -la ~/.local/bin/node`, `sudo -n`, `npm view @playwright/test version` → **`latest: 1.62.0`** (2026-07-28)
- https://playwright.dev/docs/api/class-pageassertions — options et défauts de `toHaveScreenshot` (`threshold: 0.2`, `animations: 'disabled'`, `caret: 'hide'`, `scale: 'css'`, `maskColor: '#FF00FF'`)
- https://playwright.dev/docs/test-cli — `--update-snapshots=all|changed|missing|none`, `--update-source-method`
- https://playwright.dev/docs/test-snapshots — `snapshotPathTemplate`, `stylePath`, `maxDiffPixels`
- https://playwright.dev/docs/test-configuration — `projects`, `webServer`, `baseURL`, `expect.toHaveScreenshot`
- https://playwright.dev/docs/test-reporters — reporter HTML, `open: 'never'`, `show-report`

### Secondary (MEDIUM confidence)

- `.planning/research/PITFALLS.md` (Pitfalls 2, 3, 4) et `.planning/research/SUMMARY.md` — origine des 5 écrans, des 3 gabarits et de la cible 20-40 fixtures
- `.planning/research/STACK.md:87` — Playwright 1.62.0 (concorde avec le registre npm)
- [TestQuality, Playwright Visual Regression: Baselines, Flake & CI Guide 2026](https://testquality.com/playwright-visual-regression-guide/) — heuristique « moins de 25 tests visuels ⇒ le natif suffit »
- [QASkills, Playwright Visual Comparison & Screenshot Testing Guide 2026](https://qaskills.sh/blog/playwright-visual-comparison-snapshots-guide) — masquage, attente des polices
- [Bug0, Playwright Visual Regression Testing 2026](https://bug0.com/knowledge-base/playwright-visual-regression-testing)

### Tertiary (LOW confidence — à valider)

- Le rapport HTML de Playwright affiche bien un comparateur Expected/Actual/Diff pour les échecs de capture : très probable, mais **non confirmé** par la doc consultée. Sans importance pour le plan : la validation utilisateur passe de toute façon par la page de comparaison maison (décision du CONTEXT).
- La liste exacte des couples scénario/héros validés par l'autoplay (voir Open Question 5).

## Metadata

**Confidence breakdown :**
- Standard stack : **HIGH** — version Playwright vérifiée sur le registre le jour même ; contraintes Node mesurées, pas supposées
- Architecture (fixtures, `?ui=old`, contrat `/new`) : **HIGH** — chaque décision s'appuie sur une ligne de code lue ou une réponse HTTP mesurée
- Pitfalls : **HIGH** — 6 des 9 reproduits par mesure sur le serveur en cours ; les 3 autres lus directement dans le source
- Choix de la découpe des écrans : **MEDIUM** — la roadmap dit « 5 écrans » sans les nommer ; la liste vient de `research/PITFALLS.md`

**Research date :** 2026-07-28
**Valid until :** 2026-08-27 (30 jours — Playwright bouge vite, mais tout le reste est du code local figé)
