# Stack Research

**Domain:** client web de jeu de cartes (LCG) numérique, servi en local par un serveur Python aiohttp
**Researched:** 2026-07-28
**Confidence:** HIGH sur les versions et les contraintes serveur (vérifiées sur le code et le registre npm), MEDIUM sur les choix d'ergonomie tactile (peu de sources autoritaires spécifiques aux jeux de cartes)

---

## Verdict

**Recommandation : chemin B, mais par étapes, avec le plateau porté en DERNIER.**

React 19.2 + TypeScript 6 + Vite 8, build statique multi-pages déposé dans `public/app/`, une page migrée à la fois. Le plateau de jeu actuel (`marvel.html` + `public/js/marvel/`) reste en service tel quel jusqu'à ce que son remplaçant React passe la non-régression autoplay.

**Pourquoi pas le chemin A (moderniser le vanilla) :** le projet a déjà commencé à réinventer React à la main. `public/js/prepare/app.js` (32 Ko, écrit récemment) définit un helper `el(tag, props, ...kids)` hyperscript, un objet `state` global et une fonction de re-render manuel. C'est un micro-framework maison, non typé, sans réconciliation. Les imports portent un cache-buster manuel (`?v=18`, `?v=9`, `?v=5`, désynchronisés entre fichiers), ce qui est exactement le problème que le hachage de contenu de Vite supprime. Continuer en A signifie payer le coût d'un framework sans en avoir les garanties.

**Pourquoi pas B en big-bang :** les 31 modules de `public/js/marvel/` (7 318 lignes) sont **de la sortie transpilée de TypeScript dont les sources sont perdues** (les 31 fichiers finissent par `//# sourceMappingURL=*.js.map`, et aucun `.ts` ni `.js.map` n'existe dans le dépôt). Dans ce volume, `effect.js` (818 l.), `buttons.js` (731 l.) et `select.js` (199 l.) encodent la sémantique des asks/options/ciblage, c'est-à-dire la partie du frontend la plus proche des règles et la plus coûteuse à reproduire à l'identique. Réécrire ça d'un coup, sans types d'origine, est le seul vrai risque de ce projet.

**Ce qui rend le staging sûr (découverte clé) :** le serveur route les fichiers **par extension**, pas par répertoire statique. `AddAwaitGetSecurity('/{path:.+\\.html}', handle_html)` cherche dans `./`, `./public/`, `./public/blueprints`. Donc **toute nouvelle page HTML posée dans `public/` est servie sans aucune modification du backend**. C'est déjà comme ça que `prepare.html` fonctionne : `main.html:169` fait `Open('prepare.html')` et aucune route `/prepare` n'existe côté serveur. La coexistence ancien/nouveau est gratuite.

---

## Head-to-head : A (vanilla modernisé) vs B (React + TS + Vite)

| Critère | A. Vanilla modernisé | B. React + TS + Vite | Poids ici |
|---|---|---|---|
| Sécurité de migration | Excellente (rien ne bouge) | Excellente aussi, via pages séparées `public/app/*.html` | Égalité, contrairement à l'intuition |
| Modification serveur requise | Aucune | Aucune (voir tableau des contraintes) | Égalité |
| Réutilisation du plateau existant (7 318 l. JS + 272 Ko CSS) | 100 % | 0 % pour la présentation, ~100 % pour le protocole si on l'extrait d'abord | A gagne, mais voir ligne suivante |
| Valeur réelle de cet existant pour la cible mobile | **Faible.** 6 `@media` dans TOUT `public/css/`. Zéro `touch-action`, zéro `dvh`, zéro `clamp()`, zéro `@container`. `draggable.js` n'écoute que `mousedown` : le drag est cassé au doigt. | Idem, tout est à faire | Neutralise l'avantage de A |
| Typage | Impossible à récupérer (sources TS perdues) | Types stricts, contrat serveur modélisé une fois | **B gagne largement** |
| Modèle de rendu vs modèle de données | `Cards.getDiv(object_id)` + patch `innerHTML` impératif, 30+ points de mutation | Réconciliation par `key={object_id}`, calquée sur le modèle serveur | **B gagne** (c'est la source n°1 de bugs UI en jeu de cartes) |
| Réutilisation de composants sur 6 écrans | Nulle (chaque page réimplémente) | Native | **B gagne** |
| Itération pendant une refonte visuelle | Rechargement complet + `?v=N` à incrémenter à la main | HMR, hachage de contenu automatique | **B gagne** |
| Nouvelle dépendance / toolchain | Zéro | Node + npm + ~15 devDeps | A gagne |
| Coût du portage du plateau | Zéro | Élevé : ~1 750 l. de sémantique asks/options à re-spécifier | **A gagne, décisif sur le calendrier** |
| Coût du portage menus/wizard/galerie/decks/replay | Élevé (tout à réécrire en CSS/JS à la main de toute façon) | Faible à moyen | **B gagne** |

**Lecture :** A gagne uniquement sur le plateau, B gagne partout ailleurs. D'où le découpage recommandé : B partout, plateau en dernier, protocole extrait avant présentation.

### Ordre de portage recommandé

1. **Couche de design tokens en CSS pur** (`tokens.css`). Indépendante du chemin choisi, consommable immédiatement par les pages legacy. Aucun risque.
2. **Menu principal** (`main.html`, 6,5 Ko). Pilote minimal du build Vite.
3. **Wizard de préparation** (`prepare.html` + `js/prepare/`, 6 modules). Le plus rentable : le hyperscript `el()` se traduit presque mécaniquement en JSX, et la spec fonctionnelle existe déjà (`Fusion/PREPARE-UI-PLAN.md`).
4. **Galerie de cartes** + **gestion de decks** (`cards.html` 30 Ko, `deck.html` 23 Ko). Beaucoup de listes/filtres : là où React paie le plus vite.
5. **Replay** (`replay.html`).
6. **Plateau** (`marvel.html`). En deux temps : (6a) extraire un client de protocole typé, (6b) reconstruire la présentation. Feature flag pour basculer entre l'ancien et le nouveau plateau tant que l'autoplay n'est pas à 0 traceback.

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|---|---|---|---|
| React | 19.2.8 | Couche vue | `key={object_id}` correspond exactement au modèle serveur (`world_descriptor.cards[].object_id`). `<Activity mode="hidden">`, stable en 19.2, permet de préparer le plateau ou une modale hors écran sans démonter l'état, ce qui est utile pour les overlays de sélection de cartes. `useEffectEvent` (stable) simplifie les handlers WebSocket sans redéclencher l'effet. |
| TypeScript | **6.0.3** (pas 7.0.2) | Typage | TS 7.0 est GA depuis le 08/07/2026 mais **ships sans API compilateur publique**, ce qui casse `typescript-eslint` en mode type-aware (issue #12518, fermée « not planned »), ts-jest et ts-morph. L'API arrive en 7.1. Pour un projet solo, la vitesse de compilation n'est pas le goulot : rester sur 6.0.3 évite un chantier de tooling. Migrer quand 7.1 sort. |
| Vite | 8.1.5 | Dev server + build statique | Vite 8 (stable 12/03/2026) unifie tout sur Rolldown (Rust) et Oxc. Deux propriétés cruciales ici : (1) le hachage de contenu supprime les `?v=N` manuels, (2) `build.rollupOptions.input` multi-entrées produit exactement le modèle multi-pages que le serveur sait déjà servir. `build.target` par défaut = `baseline-widely-available`, adapté à un navigateur local récent. |
| @vitejs/plugin-react | 6.0.4 | JSX + Fast Refresh | Requiert `vite ^8.0.0`. Les peers `@rolldown/plugin-babel` et `babel-plugin-react-compiler` sont **optionnels** : pas besoin de les installer. |
| CSS natif (Modules + custom properties) | n/a | Styles | Voir la section « Approche CSS ». Choix délibéré contre Tailwind, argumenté plus bas. |
| Zustand | 5.0.14 | État client | Le serveur est autoritaire et envoie des **snapshots complets** (`get_world`). Un store plat qui remplace `world` et `ask` en bloc est le bon modèle : pas de reducers, pas de logique de merge, donc aucune chance de dupliquer des règles côté client. ~1 Ko, pas de Provider. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---|---|---|---|
| Motion | 12.42.2 | Animations de cartes | Successeur de Framer Motion. `layout` + `layoutId` résolvent d'un coup les trois animations dures du jeu : main vers zone de jeu, pioche vers main, retournement de carte (`layoutId` partagé entre face cachée et face visible). `AnimatePresence` gère les défausses. Utiliser **uniquement** sur le plateau, pas dans les menus. |
| @dnd-kit/react | 0.5.0 | Drag & drop cartes | Pointer Events + capteurs tactile et clavier. **Attention : encore en 0.x** (0.5.0 publié le 11/06/2026), API instable. `@dnd-kit/core` 6.3.1 (l'ancienne ligne stable) date du 05/12/2024. À n'introduire qu'à l'étape 6, et seulement si le drag est retenu comme interaction primaire. Voir « Touch & drag » : la réponse par défaut devrait être tap-to-select. |
| @use-gesture/react | 10.3.1 | Pinch-zoom, long-press, pan | Pour le zoom carte (pinch sur tablette/mobile) et le long-press d'aperçu, indépendamment du drag. Plus simple que dnd-kit quand il n'y a pas de drop target. Version stable mais figée depuis 03/2024. |
| Zod | 4.4.3 | Validation des payloads serveur | **Optionnel mais recommandé à l'étape 6a.** Les sources TS du contrat serveur sont perdues : les schémas de `get_world` / `get_ask` doivent être reconstruits par observation de `descriptor.js` (312 l.) et `data.js` (167 l.). Un schéma Zod qui échoue bruyamment en dev transforme une erreur de reverse-engineering silencieuse en message clair. Alternative plus légère : `valibot` 1.4.2. |
| @tanstack/react-query | 5.101.4 | Cache des JSON statiques | **Pour les menus seulement** : `/get_cards_json`, `/get_sets_json`, `/list_scenarios`, `/list_starter_deck`. Ces réponses sont gzippées et `Cache-Control` côté serveur, et la galerie les relit sans cesse. **Ne PAS l'utiliser pour l'état de partie** (voir « Sync serveur »). |
| lucide-react | 1.27.0 | Icônes | Rend du SVG **inline**, donc aucun fichier `.svg` émis par le build. C'est une contrainte serveur dure ici (voir tableau des contraintes), pas une préférence esthétique. |
| clsx | 2.1.1 | Composition de classes | Trivial mais évite 200 concaténations de chaînes dans les composants de carte à états multiples. |

### Development Tools

| Tool | Version | Purpose | Notes |
|---|---|---|---|
| Node.js | 24 LTS (24.x) | Runtime de build | Vite 8 exige `^20.19.0 \|\| >=22.12.0`. WSL a actuellement **v25.3.0**, qui passe, mais 25 est une ligne impaire non-LTS. Basculer sur 24 LTS pour éviter les surprises. |
| Vitest | 4.1.10 | Tests unitaires | Partage la config Vite. Cibler la couche protocole (parsing de `get_world`, dérivation des options d'ask), pas les composants visuels. |
| happy-dom | 20.11.1 | Environnement DOM des tests | 3 à 5x plus rapide que jsdom, suffisant pour du React Testing Library. |
| vite-plugin-checker | 0.14.5 | `tsc` en parallèle du dev server | Sinon Vite ne type-check pas du tout au build (il transpile seulement). |
| ESLint | 10.8.0 + typescript-eslint 8.65.0 | Lint | Fonctionne avec TS 6.0.3. Si migration vers TS 7 plus tard : installer `@typescript/typescript6` (6.0.2) en side-by-side pour ESLint. |
| eslint-plugin-react-hooks | 7.1.1 | Règles hooks | La v7 embarque les règles issues du React Compiler, utile même sans activer le compilateur. |
| Playwright | 1.62.0 | Smoke tests | **Optionnel.** Un seul scénario utile : ouvrir `/prepare.html`, lancer une partie, vérifier que le plateau rend. Complète l'autoplay Python qui, lui, ne teste pas le DOM. |

**Ne PAS installer :** `babel-plugin-react-compiler` (1.0.0), `@rolldown/plugin-babel`. Peers optionnels. Le React Compiler apporte de la mémoïsation automatique dont un plateau de 40 à 80 cartes n'a aucun besoin, au prix d'une étape Babel dans une chaîne Rust.

---

## Contraintes du serveur Python (déterminantes pour la config du build)

Le routage est **par extension**, dans `src/engine/network/web_server.py:AddDefaultGet()`, avec un catch-all `'/{path:.+}'` en dernier qui redirige vers le loader d'images. Conséquences concrètes pour un build Vite :

| Extension émise | Route serveur | Répertoires cherchés | Verdict |
|---|---|---|---|
| `.html` | `handle_html` | `./`, `./public/`, `./public/blueprints` | ✅ OK. Nouvelle page = aucun changement backend. |
| `.js` | `handle_js` | `./`, `./public/js`, `./public/` | ✅ OK, y compris noms hachés et sous-dossiers (`/public/app/assets/index-a1b2.js` résolu depuis `./`). |
| `.css` | `handle_css` | `./`, `./public/css`, `./public/` | ✅ OK. |
| `.woff` / `.ttf` / `.eot` | `handle_font` | **`./public/fonts` uniquement, chemin écrasé** (`file_path.split('/')[-1]`) | ⚠️ Une police hachée par Vite dans `assets/` sera introuvable. **Garder les polices hors du pipeline Vite** : `@font-face { src: url('/fonts/ChampionsIcons.ttf') }`. Vite laisse intactes les `url()` absolues, le serveur ne garde que le nom de fichier, et les polices existantes (`ChampionsIcons.ttf`, `MarvelRegular-Dj83.ttf`) sont déjà là. |
| `.woff2` | **aucune route** | tombe dans le catch-all image → échec | ❌ Ne pas utiliser. Le gain de poids woff2 est sans objet sur `127.0.0.1`. |
| `.svg` | `handle_svg` | **`./assets/textures/` uniquement, chemin écrasé** | ❌ **Aucun fichier `.svg` ne doit sortir du build.** Utiliser du SVG inline (JSX, ou `lucide-react`). Les nouvelles illustrations SVG vont dans `assets/textures/` et se référencent `/mon-icone.svg`. |
| `.png` / `.jpg` / `.webp` | aucune route → catch-all → `Cache.LoadImage` | `./assets/pics/`, `./assets/textures/`, `./assets/cache/` | ⚠️ Une image hachée dans `assets/` échouera. Deux options : monter `build.assetsInlineLimit` pour inliner en base64, ou déposer l'art d'interface dans `assets/textures/` et le référencer en URL absolue (convention déjà en place : `url("sparkles.gif")`, `url("target")`). |
| `.json` | aucune route → catch-all image | n/a | ⚠️ Ne pas émettre de `.json` à charger au runtime. Les imports JSON de Vite sont bundlés dans le JS, donc sans risque. Les endpoints JSON du serveur (`/get_cards_json`, gzip) sont des routes explicites et fonctionnent normalement. |
| `.js.map` | `handle_js_map` | 404 si `RELEASE=1` | ⚠️ Les sourcemaps sont muettes en release. Pour déboguer, lancer sans `RELEASE=1`, ou utiliser le dev server Vite. |

**Deux garde-fous supplémentaires trouvés dans le code :**

- `IsVersionMatch()` compare un cookie `app_version` à `Ver.ui_version_str` et sert `clean_cache.html` en cas d'écart, **sur toutes les routes fichiers**. Le hachage de contenu de Vite rend ce mécanisme redondant mais inoffensif.
- `Cache-Control: public, max-age=<cache_max_age>`, avec `cache_max_age: 60` dans `launch.json`. Confortable en dev. En cas de passage à `31536000`, le hachage de Vite devient indispensable, ce qui est un argument de plus pour B.

### Configuration Vite qui en découle

```ts
// vite.config.ts
export default defineConfig({
  base: '/public/app/',                 // URL réelle servie par aiohttp
  build: {
    outDir: '../marvel-lcg-src/public/app',
    emptyOutDir: true,
    assetsInlineLimit: 16384,           // inline les petites images, évite le catch-all image
    rollupOptions: {
      input: {                          // multi-pages = migration page par page
        main:    'src/pages/main.html',
        prepare: 'src/pages/prepare.html',
        cards:   'src/pages/cards.html',
        // board: ajouté à l'étape 6 seulement
      },
    },
  },
  server: {
    proxy: {                            // dev sur :5173, backend réel sur :2345
      '/ws':        { target: 'ws://127.0.0.1:2345', ws: true },
      '/get_world': 'http://127.0.0.1:2345',
      '/get_ask':   'http://127.0.0.1:2345',
      // + get_cards_json, list_scenarios, read_file, new, client_updated, /sets, images
    },
  },
})
```

Le `server.proxy` avec `ws: true` est le point qui rend le HMR utilisable sur le plateau : sans lui, impossible d'itérer sur l'UI de partie sans rebuild.

---

## Approche CSS

**Recommandation : CSS natif, tokens en custom properties, CSS Modules par composant, container queries. Pas de Tailwind.**

Trois raisons propres à ce projet :

1. **La couche tokens est indépendante du chemin A/B.** Un `tokens.css` unique (couleurs par aspect, échelles d'espacement, rayons, ombres, durées, ratio de carte) est consommable *aujourd'hui* par les 60 CSS legacy de `public/css/marvel/` et par `wizard.css`. C'est le seul livrable de la refonte qui améliore l'ancien et le nouveau simultanément. Il doit être le tout premier. Les couleurs d'aspect sont déjà codées en dur dans `js/prepare/app.js` (`aggression: "#d1403a"`, etc.) : elles remontent dans les tokens.
2. **Les états de carte sont combinatoires.** Une carte peut être simultanément épuisée, confuse, étourdie, ciblable, sélectionnée, endommagée, active, en cours d'animation. En CSS natif ça s'écrit `[data-state~="stunned"]` et se compose proprement. En Tailwind ça devient des chaînes de classes conditionnelles illisibles dans le JSX, pour le composant le plus important de l'app.
3. **Compétence et actif existants.** `wizard.css` (21 Ko) et `prepare/prepare.css` (22 Ko), écrits récemment à la main, sont structurés. Rester en CSS permet un portage progressif des 272 Ko de CSS plateau au lieu d'une réécriture obligatoire.

Techniques à utiliser, toutes en Baseline :

- **Design tokens** : `@property` pour les customs animables (`--damage-count`, `--card-rotate`), sinon `:root { --… }`. Un fichier `tokens.css` chargé par toutes les pages, y compris les legacy.
- **Container queries** : Baseline depuis 2023, >93 % de couverture. **Le bon outil ici, pas les media queries.** Le plateau contient des zones imbriquées (zone joueur, main, zone villain, side schemes) dont la taille disponible ne suit pas celle du viewport. Une carte doit se compacter selon la largeur de *sa zone*, pas de l'écran. `@container (inline-size < 30rem)`.
- **Unités de container** : `cqi` dans `clamp()` pour la typo des cartes : `font-size: clamp(0.7rem, 0.4rem + 2.5cqi, 1.1rem)`. C'est ce qui permet à une carte lisible sur PC de rester lisible en petit sur mobile.
- **Type fluide** : `clamp()` en `rem` exclusivement (les `px` cassent le zoom et la préférence de taille de police). Ne pas rendre tout fluide : corps de texte fixe, titres fluides.
- **Viewport mobile** : `100dvh` et non `100vh` (barre d'URL iOS). Actuellement absent partout dans `public/css/`.
- **`@layer`** : `@layer tokens, legacy, base, components, utilities;` pour que le nouveau design system gagne sans guerre de `!important` contre `css/menu/style.css`.
- **`color-mix()` et `oklch()`** : pour dériver les variantes d'états (hover, disabled, ciblable) depuis une couleur d'aspect unique, au lieu de 6 hex par aspect.

**Outillage CSS :** aucun préprocesseur. Vite gère les CSS Modules nativement (`*.module.css`). Ajouter `postcss-preset-env` 11.3.2 seulement si un besoin de polyfill apparaît, ce qui est peu probable sur un navigateur local récent. Lightning CSS reste **expérimental** dans Vite en tant que transformer (`css.transformer: 'lightningcss'`) ; Vite l'utilise déjà par défaut pour la minification en production, donc ne rien configurer.

---

## Animations de cartes

| Interaction | Technique | Pourquoi |
|---|---|---|
| Retournement de carte (dos ↔ face) | CSS `transform: rotateY()` + `transform-style: preserve-3d`, ou Motion `layoutId` partagé | Déjà l'approche actuelle (`card_animation.js:228` fait du `translate3d` + `rotate` en rAF). Pas besoin de librairie pour ça seul. |
| Déplacement main → zone de jeu | Motion `layout` / `layoutId` | C'est le cas d'usage exact du FLIP automatique de Motion. Remplace `move-card.js` (349 l.) de calcul de position manuel. |
| Pioche / défausse | Motion `AnimatePresence` | Gère l'animation de sortie avant démontage, impossible proprement à la main en React. |
| Dégâts, menaces, jetons | Transition CSS sur une custom property `@property` | Pas de JS. Compteurs animables en CSS pur. |
| Zoom / aperçu de carte | `@use-gesture/react` (pinch) + CSS `scale` | Le zoom n'a pas de drop target, dnd-kit serait surdimensionné. |
| Effets d'ambiance (météo, particules) | Garder l'existant tel quel | `effects/weather/snow.html` (78 Ko) fonctionne, s'intègre en iframe/overlay. Zéro raison de le toucher. |

Règle de discipline : **animer uniquement `transform` et `opacity`**. Les 40 à 80 cartes du plateau sont des nœuds DOM ; toute animation touchant à `width`, `top` ou `box-shadow` déclenche layout ou paint sur l'ensemble.

**Note sur React 19.2 :** il n'y a **pas** de `<ViewTransition>` stable en 19.2 (mentionné dans le blog comme direction future uniquement). Ne pas planifier dessus. La View Transitions API native du navigateur reste utilisable directement pour les transitions inter-pages, mais avec un build multi-pages elle demande la variante cross-document, à considérer comme du confort en fin de projet.

---

## Touch & drag

**Recommandation forte : tap-to-select puis tap-to-target comme interaction primaire, drag comme accélérateur optionnel sur desktop uniquement.**

Justification : le moteur est **déjà** construit pour ça. `get_ask` renvoie une liste d'`options` et `effect.js` gère `all_legal_targets`. Le modèle mental du serveur est « le serveur propose N options, le joueur en choisit une », pas « le joueur déplace un objet ». Le tap-to-select est donc à la fois plus simple à implémenter, sans ambiguïté sur mobile, accessible au clavier, et fidèle au protocole. Le drag est une couche de plaisir, pas le mécanisme.

Points techniques :

- **Pointer Events uniquement.** Jamais l'API HTML5 Drag and Drop : elle ne fonctionne pas au tactile. L'état actuel le confirme : `draggable.js` n'écoute que `mousedown`, donc rien ne se déplace au doigt aujourd'hui.
- **`touch-action: none`** sur les éléments draggables et **`touch-action: pan-y`** sur les zones scrollables de cartes. Aucune occurrence de `touch-action` dans `public/css/` actuellement : c'est la cause première du drag cassé sur mobile.
- **`-webkit-touch-callout: none`** en plus de `user-select: none` (déjà présent partout) pour supprimer le menu contextuel iOS au long-press. Sinon le long-press d'aperçu de carte est inutilisable sur iPad.
- **`setPointerCapture`** pour ne pas perdre le pointeur quand le doigt sort de la carte.
- **Cibles de 44 px minimum** sur mobile. À 100 px de large (`--card--width: 100px` dans `scene.html`), les badges et compteurs sur carte sont sous ce seuil : prévoir une zone tactile étendue ou un panneau de détail dédié en mobile.
- **Zone de main sur mobile** : un fan de 5 à 8 cartes ne tient pas. Prévoir un carrousel scroll-snap ou un tiroir plein écran plutôt qu'une réduction homothétique.

---

## Sync avec le serveur

**Recommandation : garder exactement le protocole existant. Ne pas le réinventer.**

Le contrat actuel, lu dans `public/js/marvel/client.js` et `src/engine/device/web/server/server_sync.py`, est déjà le bon pattern pour un jeu de cartes à serveur autoritaire :

```
WebSocket /ws            → notification légère (« l'état a changé »)
GET get_world?p=0        → snapshot COMPLET du monde, avec render_id
GET get_ask?p=<ids>      → prompt + options légales du joueur
GET client_updated?p&r&g → accusé de réception du render_id
```

C'est du **notify-then-fetch**, et non du state-diffing sur WebSocket. Les avantages sont réels et méritent d'être préservés : le rendu est idempotent (rejouer un snapshot donne le même écran), le client ne duplique aucune règle, aucune logique de merge de deltas ne peut divergen, et le `render_id` + `client_updated` donnent une barrière de synchronisation que le serveur utilise pour ne pas avancer avant que l'UI ait fini d'animer.

Ce qu'il faut faire côté nouveau frontend :

1. Encapsuler ce protocole dans un module unique `src/engine/protocol.ts` (types + client WS + fetchers + ack). Un seul point de contact avec le serveur.
2. Poser le snapshot dans Zustand par **remplacement complet**, jamais par patch. `set({ world: parsed })`.
3. Valider le snapshot avec Zod en dev (`import.meta.env.DEV`) pour attraper les erreurs de reverse-engineering du contrat.
4. Conserver la file de messages WS avec écrasement (`client.js` fait `messageQueue.pop()` puis `length = 0`, c'est-à-dire « seule la dernière notification compte »). Comportement correct pour du snapshot : le reproduire, ne pas le « corriger ».
5. Conserver l'appel `client_updated` après la fin des animations, pas après le rendu. C'est ce qui empêche le serveur de brûler des étapes.

**Le polling HTTP est à écarter** : le WebSocket existe déjà côté serveur (`server_socket.py:93`), il fonctionne, et un fallback polling n'aurait de sens que sur un réseau hostile, ce qui n'existe pas sur `127.0.0.1`. Conserver seulement le `doReconnect()` déjà présent, qui suffit au cas du serveur redémarré.

**Pourquoi pas TanStack Query pour l'état de partie** : Query est un cache de requêtes, avec invalidation, retry, staleness et refetch en arrière-plan. Sur un snapshot poussé par le serveur, chacune de ces fonctionnalités est au mieux inutile, au pire nuisible (un refetch spontané pendant une animation casse la barrière `render_id`). Le garder strictement pour les JSON statiques des menus.

---

## Installation

```bash
# Core
npm install react@19.2.8 react-dom@19.2.8 zustand@5.0.14

# Plateau (étape 6 uniquement)
npm install motion@12.42.2 @use-gesture/react@10.3.1
npm install @dnd-kit/react@0.5.0        # optionnel, voir Touch & drag

# Menus / galerie
npm install @tanstack/react-query@5.101.4 lucide-react@1.27.0 clsx@2.1.1

# Validation du contrat serveur (recommandé étape 6a)
npm install zod@4.4.3

# Dev
npm install -D vite@8.1.5 @vitejs/plugin-react@6.0.4 typescript@6.0.3
npm install -D @types/react@19 @types/react-dom@19
npm install -D vite-plugin-checker@0.14.5
npm install -D vitest@4.1.10 happy-dom@20.11.1 @testing-library/react
npm install -D eslint@10.8.0 typescript-eslint@8.65.0 eslint-plugin-react-hooks@7.1.1
```

Node 24 LTS. Ne pas installer `babel-plugin-react-compiler` ni `@rolldown/plugin-babel` (peers optionnels de plugin-react).

---

## Alternatives Considered

| Recommandé | Alternative | Quand préférer l'alternative |
|---|---|---|
| CSS Modules + tokens | **Tailwind CSS 4.3.3** (+ `@tailwindcss/vite` 4.3.3) | Si la lisibilité des états de carte cesse d'être un critère, ou si le plateau finit par ne pas être porté du tout. Tailwind 4 est objectivement bon : `@theme` génère les tokens en custom properties, les variantes `@container` sont natives, et sur les menus/wizard/galerie il ferait gagner du temps. Le pas de côté acceptable : Tailwind sur les pages hors plateau, CSS Modules sur le plateau. Coût : deux systèmes à maintenir seul. |
| Zustand | **Valtio 2.3.2** (proxy) ou `useSyncExternalStore` brut | Valtio si l'accès en style mutable est plus confortable. `useSyncExternalStore` si la volonté est de rester à zéro dépendance d'état : sur un snapshot remplacé en bloc, il suffit presque. |
| Vite MPA (multi-entrées HTML) | **TanStack Router 1.170.18** ou **wouter 3.10.0** | Seulement si les 6 écrans deviennent une vraie SPA. Aujourd'hui la navigation est déjà `window.location.href` (`main.html:155`), et le MPA préserve la coexistence avec les pages legacy sans effort. Le routeur client casserait cette propriété. |
| Motion | **GSAP 3.15.0** / **anime.js 4.5.0** / **`@formkit/auto-animate` 0.10.0** | GSAP si des timelines complexes multi-cartes apparaissent (séquence d'attaque avec 5 étapes). auto-animate si l'on veut 80 % de l'effet pour 2 Ko et zéro API. Les transitions CSS pures suffisent pour la moitié des animations listées. |
| @dnd-kit/react | **`@atlaskit/pragmatic-drag-and-drop` 2.0.1** | Si le 0.x de dnd-kit pose problème. Pragmatic est stable, très performant, mais repose sur l'API HTML5 DnD pour le desktop et demande un adaptateur tactile séparé, ce qui est un mauvais compromis pour la cible mobile. |
| TypeScript 6.0.3 | **TypeScript 7.0.2** | Quand 7.1 expose la nouvelle API compilateur et que typescript-eslint la supporte. En attendant, possible en side-by-side : TS 7 pour `tsc`, `@typescript/typescript6` (6.0.2, binaire `tsc6`) pour ESLint. Complexité non justifiée sur un projet solo. |
| @vitejs/plugin-react | **@vitejs/plugin-react-swc 4.3.2** | Accepte `vite ^4 \|\| ... \|\| ^8`. Marginalement plus rapide, mais Vite 8 étant déjà sur Oxc/Rust, l'écart est négligeable et plugin-react est le chemin par défaut. |

---

## What NOT to Use

| Éviter | Pourquoi | À la place |
|---|---|---|
| **Phaser / PixiJS / Three.js** | Le plateau compte 40 à 80 cartes statiques, pas 10 000 sprites. Un moteur canvas détruit ce qui compte le plus ici : texte de carte net et sélectionnable, zoom navigateur, accessibilité, focus clavier, et surtout `Cache.LoadImage` qui sert les visuels de cartes en JPEG par `card_id`. Il faudrait réimplémenter tout le layout, le texte et le hit-testing à la main. Le plateau existant tourne déjà en DOM avec `translate3d` et ça fonctionne. | DOM + CSS `transform` + Motion |
| **API HTML5 Drag and Drop** (`dragstart`, `dataTransfer`) | Ne fonctionne pas au tactile. Rédhibitoire pour la cible tablette/mobile. | Pointer Events, via dnd-kit ou à la main |
| **`.woff2` pour les polices** | Aucune route serveur : tombe dans le catch-all image et échoue. Gain de poids nul sur localhost. | `.ttf` / `.woff` dans `public/fonts/`, hors pipeline Vite |
| **Fichiers `.svg` émis par le build** | `handle_svg` écrase le chemin et ne lit que `./assets/textures/`. Un `assets/icon-a1b2.svg` est introuvable. | SVG inline (JSX, `lucide-react`), ou dépôt manuel dans `assets/textures/` |
| **TanStack Query pour l'état de partie** | Refetch en arrière-plan et staleness entrent en conflit avec la barrière `render_id` / `client_updated`. Un refetch spontané pendant une animation désynchronise l'UI. | Zustand alimenté par le WebSocket |
| **Polling HTTP de l'état** | Le WebSocket existe déjà et fonctionne (`server_socket.py:93`). Le polling ajouterait de la latence et de la charge sans aucun bénéfice en local. | WS notify + `get_world` snapshot |
| **Sortable.js** (128 Ko, présent dans `public/js/lib/`) | Manipule le DOM directement, ce qui entre en conflit frontal avec la réconciliation React. C'est la première cause de bugs « carte fantôme » dans les portages React. | dnd-kit (headless, laisse React posséder le DOM) |
| **vanilla-tilt.js** (17 Ko, présent) | Idem : mutation directe de `style.transform` sur des nœuds gérés par React et par Motion. Trois acteurs sur la même propriété. | Effet tilt en CSS (`rotateX/Y` depuis des custom properties mises à jour au pointeur) |
| **Font Awesome 4** (`css/font-awesome.css`, 40 Ko + `.eot`/`.woff`) | Version datée, poids important, et dépend de la route `handle_font` à chemin écrasé. | `lucide-react` (SVG inline, tree-shaké) |
| **`babel-plugin-react-compiler`** | Mémoïsation automatique inutile à cette échelle, ajoute une étape Babel dans une chaîne Rust. | Rien. `eslint-plugin-react-hooks` 7 en donne les garde-fous sans le coût. |
| **Réécriture du plateau en premier** | 7 318 lignes de TS transpilé sans sources, dont ~1 750 de sémantique asks/options/ciblage. C'est le seul endroit du projet où un bug se confond avec un bug de règles. | Plateau en dernier, protocole typé extrait d'abord, feature flag, autoplay à 0 traceback avant bascule |
| **`100vh`** | Barre d'URL iOS : le plateau est rogné en bas sur mobile. | `100dvh` |
| **Toucher au moteur ou à ses endpoints** | Contrainte absolue du projet. Aucun besoin identifié : les 10 extensions nécessaires sont déjà routées. | Utiliser `public/*.html` (déjà servi) et `assets/textures/` (déjà servi) |

---

## Version Compatibility

| Package A | Compatible avec | Notes |
|---|---|---|
| vite@8.1.5 | Node `^20.19.0 \|\| >=22.12.0` | WSL a v25.3.0 : passe, mais non-LTS. Préférer 24 LTS. |
| @vitejs/plugin-react@6.0.4 | vite `^8.0.0` **strictement** | Ne fonctionne pas avec Vite 7. Peers `@rolldown/plugin-babel` et `babel-plugin-react-compiler` optionnels. |
| typescript@7.0.2 | ❌ typescript-eslint@8.65.0 (type-aware), ts-jest, ts-morph | Pas d'API compilateur publique avant TS 7.1. **Rester en 6.0.3.** |
| typescript@6.0.3 | ✅ typescript-eslint@8.65.0, vite-plugin-checker@0.14.5 | Combinaison sûre aujourd'hui. |
| react@19.2.8 | motion@12.42.2, zustand@5.0.14, @dnd-kit/react@0.5.0, @tanstack/react-query@5.101.4 | Aucun conflit connu. `@types/react@19` obligatoire. |
| @dnd-kit/react@0.5.0 | @dnd-kit/abstract@0.5.0 | Ligne 0.x, **pas** compatible avec l'API `@dnd-kit/core@6.3.1`. Ce sont deux bibliothèques différentes malgré le nom. Ne pas mélanger les tutoriels des deux. |
| @use-gesture/react@10.3.1 | react 19 | Figée depuis 03/2024 mais stable et sans dépendance. |
| tailwindcss@4.3.3 (si retenu) | vite `^5.2 \|\| ^6 \|\| ^7 \|\| ^8` via `@tailwindcss/vite@4.3.3` | v4.2 est EOL depuis le 08/05/2026 : viser 4.3.x directement. Le preflight de Tailwind écraserait `css/menu/style.css` : ne jamais charger les deux sur la même page. |
| Build Vite → serveur aiohttp | `.html` `.css` `.js` OK ; `.svg` `.woff2` `.png` `.json` **KO** | Voir le tableau des contraintes serveur. |

---

## Sources

**Code du projet (confiance HIGH, lu directement)**
- `src/engine/network/web_server.py` (l. 130-274) : routage par extension, `ReadFile`, `IsVersionMatch`, `Cache-Control`
- `src/engine/device/web/server/server_files.py`, `server_html.py`, `server_get.py`, `server_sync.py`, `server_socket.py` : inventaire complet des routes
- `src/engine/lib/mime_type.py`, `src/engine/file/cache.py` (l. 11-38) : types MIME et dossiers de résolution d'images
- `public/js/marvel/client.js` (l. 340-460) : protocole WS notify + `get_world` / `get_ask` / `client_updated`
- `public/js/marvel/cards.js`, `effect.js`, `buttons.js` : rendu impératif par `object_id`
- `public/js/prepare/app.js` : hyperscript `el()` maison, tokens de couleur en dur, cache-buster `?v=N`
- `public/marvel.html` (l. 5-63) : 60 feuilles CSS ; `public/scene.html` : ~2 000 l. avec 15 blocs `<script>` et 9 blocs `<style>` inline
- `launch.json` : `cache_max_age: 60`, `127.0.0.1:2345`
- Mesures : 6 `@media` dans tout `public/css/`, 0 `touch-action`, 0 `dvh`, 0 `clamp()`, 0 `@container` ; 31/31 fichiers `js/marvel/` avec `sourceMappingURL` et 0 fichier `.ts` ou `.js.map` présent

**Versions (confiance HIGH, registre npm interrogé le 2026-07-28)**
- react/react-dom 19.2.8, vite 8.1.5 (16/07/2026), typescript 7.0.2 (08/07/2026) et 6.0.3 (16/04/2026), tailwindcss 4.3.3, motion 12.42.2 (30/06/2026), @dnd-kit/react 0.5.0 (11/06/2026), @dnd-kit/core 6.3.1 (05/12/2024), @use-gesture/react 10.3.1 (21/03/2024), zustand 5.0.14, @tanstack/react-query 5.101.4, @vitejs/plugin-react 6.0.4, zod 4.4.3, vitest 4.1.10, eslint 10.8.0, typescript-eslint 8.65.0, lucide-react 1.27.0
- Peers vérifiés : `@vitejs/plugin-react@6.0.4` → `vite ^8.0.0`, peers Babel `optional: true` ; `@tailwindcss/vite@4.3.3` → `vite ^5.2 || ^6 || ^7 || ^8`

**Documentation officielle (confiance HIGH)**
- https://vite.dev/blog/announcing-vite8 : Vite 8 stable 12/03/2026, Rolldown unifié, Node 20.19+/22.12+
- https://vite.dev/config/build-options : `base` relatif supporté via `import.meta.url`, `assetsInlineLimit` 4096 par défaut, `target` `baseline-widely-available`, `minify` `oxc`
- https://vite.dev/guide/features : CSS Modules natifs, Lightning CSS **expérimental** comme transformer, imports JSON bundlés
- https://react.dev/blog/2025/10/01/react-19-2 : `<Activity>` et `useEffectEvent` stables, **pas** de `<ViewTransition>` stable

**Sources secondaires (confiance MEDIUM, croisées)**
- https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/ et https://github.com/typescript-eslint/typescript-eslint/issues/12518 : TS 7 sans API compilateur publique, support typescript-eslint « not planned », `@typescript/typescript6` en side-by-side, API en 7.1
- https://blog.logrocket.com/container-queries-2026/ et https://web.dev/articles/baseline-in-action-fluid-type : container queries Baseline depuis 2023, >93 % de couverture, `cqi` dans `clamp()`
- https://laravel-news.com/tailwindcss-4-2-0 et https://eosl.date/eol/product/tailwind-css/ : Tailwind 4.2 EOL 08/05/2026, 4.3.3 courant
- https://puckeditor.com/blog/top-5-drag-and-drop-libraries-for-react : dnd-kit défaut de facto en 2026

**Confiance LOW (non retenu comme argument)**
- Résultats de recherche généralistes sur « DOM vs canvas pour jeu de cartes » : contradictoires et non spécifiques. L'argumentaire DOM ci-dessus repose sur les faits du projet (nombre de cartes, texte de carte, `Cache.LoadImage`, plateau DOM déjà fonctionnel), pas sur ces sources.
- Comparatifs génériques « WebSocket vs polling » : la recommandation vient du protocole déjà implémenté dans le code, non de ces articles.

---

## Gaps et questions ouvertes

1. **Contrat `get_world` / `get_ask` non spécifié.** Reconstructible seulement par lecture de `descriptor.js` (312 l.) et `data.js` (167 l.). C'est le prérequis de l'étape 6a et la principale inconnue de charge du projet. À traiter comme une phase de recherche dédiée au moment du portage du plateau.
2. **Sémantique exacte de `effect.js` (818 l.) et `buttons.js` (731 l.).** Combien de types d'ask, combien de modes de ciblage, quelles interactions composites (payer un coût puis choisir une cible puis confirmer). Non chiffré à ce stade.
3. **Nombre réel de nœuds carte simultanés sur un plateau 4 joueurs.** Estimé 40 à 80 par analogie avec le jeu physique, non mesuré. Si le chiffre réel dépasse 200, revalider le choix DOM.
4. **Coexistence des tokens avec `css/menu/style.css`.** `@layer` devrait suffire, mais `style.css` (8 Ko) n'a pas été audité ligne à ligne pour détecter des sélecteurs très spécifiques ou des `!important`.
5. **`assets/textures/`** contient un mélange `.svg` / `.webp` / `.jpg`. La convention de référencement (`url("target")` sans extension) est résolue côté serveur par essai d'extensions dans `Cache.LoadImage` : le mécanisme exact d'essai n'a pas été lu en détail.

---
*Stack research for: client web de jeu de cartes numérique servi en local (Python aiohttp)*
*Researched: 2026-07-28*
