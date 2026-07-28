# Architecture Research

**Domain:** Client web de jeu de cartes (LCG solo/hot-seat) piloté par un moteur de règles serveur
**Researched:** 2026-07-28
**Confidence:** HIGH sur l'intégration au système existant (lu dans le code source), MEDIUM sur les patterns de domaine (sources publiques croisées)

## Résumé

Le système existant est déjà, sans le nommer, l'architecture recommandée par le domaine : moteur **serveur autoritaire** qui publie un **snapshot complet d'état** (`WorldDescriptor`) plus une **demande d'action** (`AskOptionPayload`), et un client purement présentationnel qui rend le snapshot et renvoie un choix. Cette séparation est le bon acquis : elle signifie que la refonte est **entièrement remplaçable côté client, surface par surface**, sans jamais toucher au protocole.

Trois faits mesurés déterminent l'architecture de la refonte :

1. Le serveur sert les fichiers statiques **par extension de fichier**, pas par dossier (`web_server.py:263-278`). Il n'existe aucune route pour `.json`, `.png`, `.webp`, `.woff2`, et `.js.map` renvoie 404 en mode RELEASE (obligatoire ici). Toute chaîne de build doit être calibrée sur cette liste blanche d'extensions.
2. Le plateau est une **scène virtuelle fixe de 1920x1080 mise à l'échelle uniformément** (`scene.js:37-57`, `marvel.css:60-61`). Sur mobile portrait cela donne un facteur d'échelle d'environ 0,2 et des cartes de 25 px de large : illisible. Le responsive mobile n'est pas un réglage CSS, c'est un composant de layout à écrire.
3. Le contrat HTML/JS du plateau est constitué d'environ 60 identifiants d'éléments codés en dur (`descriptor.js`, `move-card.js`), de 5 objets exposés sur `window` pour les `onclick` inline, et d'un positionnement horizontal **calculé en JavaScript** par zone. Le restylage est donc gratuit, mais le re-layout ne l'est pas.

La conséquence pour la roadmap : le design system et la couche d'accès aux données viennent d'abord, les écrans hors-jeu ensuite (du plus petit au plus gros), et le plateau se découpe en trois étapes de risque croissant (restylage CSS, moteur de layout responsive, couche d'interaction) plutôt qu'en une réécriture unique.

## Architecture standard

### Vue d'ensemble système

Cible recommandée. Les composants marqués `[existant]` ne changent pas, `[nouveau]` est à écrire, `[legacy]` est à étrangler.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        SURFACES (une page HTML par surface)              │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐   │
│ │  Menu    │ │ Prepare  │ │ Galerie  │ │  Decks   │ │ Replay/Rapport │   │
│ │ [nouveau]│ │[en cours]│ │ [legacy] │ │ [legacy] │ │    [legacy]    │   │
│ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬────────┘   │
│      │            │            │            │               │            │
│      │        ┌───┴────────────┴────────────┴───────────────┴──┐         │
│      │        │        PLATEAU (marvel.html) [legacy → nouveau]│         │
│      │        │  Layout zones │ Couche interaction │ Animations│         │
│      │        └───────────────────────┬───────────────────────-┘         │
├──────┴────────────────────────────────┴──────────────────────────────────┤
│                    DESIGN SYSTEM  [nouveau]                              │
│  tokens.css (variables CSS)  │  primitives (Button, Panel, Dialog, Tabs) │
│  card-tile / card-preview    │  layout (Shell, Stack, Grid, Sheet)       │
├──────────────────────────────────────────────────────────────────────────┤
│                COUCHE D'ACCÈS AUX DONNÉES  [nouveau]                     │
│  ┌────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │  catalog (lecture) │  │  session (in-game)   │  │ prefs (local)    │  │
│  │  cartes/sets/      │  │  WS + snapshot + ask │  │ localStorage     │  │
│  │  scénarios/decks   │  │  + post              │  │ cookies          │  │
│  └─────────┬──────────┘  └──────────┬───────────┘  └──────────────────┘  │
│            │        anti-corruption layer (adapters)                     │
├────────────┼────────────────────────┼────────────────────────────────────┤
│            ▼                        ▼                                    │
│              SERVEUR PYTHON aiohttp  [existant, intouchable]             │
│  /get_sets_json /list_scenarios /get_hero_json /read_file  (catalogue)   │
│  /new?data=  (création de partie)                                        │
│  /ws  /get_world  /get_ask  POST /post  /client_updated  (runtime)       │
│  /{card_id}  /sets/{clé}  (images, cache disque + CDN)                   │
├──────────────────────────────────────────────────────────────────────────┤
│              MOTEUR DE RÈGLES  [existant, interdiction absolue]          │
│  World → render/to_descriptor.py → WorldDescriptor                       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Responsabilités des composants

| Composant | Responsabilité | Implémentation typique |
|-----------|----------------|------------------------|
| `tokens.css` | Source unique des couleurs, typo, espacements, rayons, ombres, durées, z-index | Variables CSS sur `:root`, un seul fichier, aucune dépendance |
| Primitives UI | Boutons, panneaux, dialogues, onglets, champs, badges, tooltips | Classes CSS + Custom Elements sans shadow DOM (pour rester stylables par les tokens) |
| `card-tile` / `card-preview` | Afficher une carte (image, coût, stats, état) à plusieurs densités | Le composant le plus réutilisé de l'app : galerie, deck builder, plateau, prévisualisation |
| Shell de surface | En-tête, navigation retour, zone de contenu, gestion du responsive de page | Un shell partagé, une instance par page HTML |
| `catalog` | Lire et mettre en cache les données statiques (cartes, sets, scénarios, decks) | Wrapper `fetch` + `Map` en mémoire, index par id (déjà amorcé dans `js/prepare/api.js`) |
| `session` | Cycle de vie d'une partie : connexion WS, récupération du snapshot, de l'ask, envoi du choix | Machine à états, source unique de vérité côté client, remplace l'usage direct de `Client` |
| `board-layout` | Assigner à chaque zone une position et une taille selon le viewport et le nombre de cartes | Module de layout, remplace `pos-area.css` + `move-card.js` |
| `board-render` | Réconcilier le snapshot avec le DOM (création, mise à jour, suppression, déplacement) | Diff par clé sur `object_id` + saut de rendu par hash d'état (déjà présent dans `cards.js`) |
| `board-interaction` | Traduire un `AskOptionPayload` en affordances cliquables, collecter cibles et paiement, poster | Machine à états `card → effect → targets → cost → post` (déjà présente dans `select.js`) |
| `board-fx` | Animations de déplacement, dégâts, révélations, flèches de ciblage | FLIP ou View Transitions same-document, file d'animations bornée dans le temps |
| `prefs` | Réglages utilisateur persistants (densité, animations, sons, aides) | localStorage plus cookies pour ce que le serveur lit déjà |

## Contraintes réelles d'intégration (vérifiées dans le code)

Ce tableau est le cœur du travail : ce sont des faits lus dans les sources, pas des hypothèses. Ils cadrent tous les choix techniques en aval.

| Fait | Preuve | Conséquence architecturale |
|------|--------|----------------------------|
| Le statique est routé **par extension**, avec des racines de recherche fixes | `web_server.py:263-278` : `.html` → `./public/` ; `.css` → `./public/css`, `./public/` ; `.js` → `./public/js`, `./public/` | Un build peut écrire dans n'importe quel sous-dossier de `public/` tant qu'il ne produit que des extensions servies |
| **Aucune route pour `.json`** | Absente de `AddDefaultGet` ; la requête tombe sur le fourre-tout `/{path:.+}` de `server_files.py:37` qui la traite comme une image de carte | Interdiction d'embarquer un fichier de config ou de données JSON statique dans `public/`. Passer par `/read_file?` ou les endpoints `get_*_json`, ou inliner les données dans un module `.js` |
| **Aucune route pour `.png` / `.webp` / `.avif`** | Idem, fourre-tout image par `card_id` | Les assets décoratifs doivent être en `.svg` (route dédiée, **nom de fichier seul**, servi depuis le dossier textures) ou en data URI dans le CSS, ou en pur CSS |
| **Aucune route pour `.woff2`** | Seuls `.eot`, `.woff`, `.ttf` sont routés, et le chemin est réduit au nom de fichier (`handle_font`) | Les webfonts doivent être en `.woff`/`.ttf`, à plat dans `public/fonts/`, noms uniques. Pas de sous-dossiers utiles |
| `.js.map` et `.ts` renvoient **404 en RELEASE** | `handle_js_map` / `handle_ts` testent `Build.release` ; `launcher.py:17` force `RELEASE=1` | Pas de source maps servies. Un bundle minifié serait indébuggable : privilégier une sortie lisible ou pas de bundling |
| Le fourre-tout image est enregistré **en dernier** | Ordre du MRO dans `server.py` : `GameServerFiles.__init__` appelle `super().__init__()` avant d'ajouter ses routes | Les routes par extension gagnent toujours contre le fourre-tout. Un nouveau `.html` est servi sans aucune modification Python |
| Auth et contrôle de version sont **neutralisés** par le launcher | `launcher.py:75-76` réécrit `IsAuthenticate` et `IsVersionMatch` en `lambda: True` | Pas de cookie `app_version` à gérer, pas de page `clean_cache` à craindre. Ne pas s'appuyer sur ce mécanisme non plus |
| Cache HTTP agressif en RELEASE | `HeaderCache = public, max-age=cache_max_age` (60 s par défaut), appliqué par `ReadFile` | Le versionnage par query string est déjà la convention en place (`prepare.html` charge `app.js?v=18`). La conserver |
| Le plateau est une scène fixe 1920x1080 mise à l'échelle | `marvel.css:60-61` définit `--scene-width: 1920` / `--scene-height: 1080` ; `scene.js:46` fait `Math.min(scaleX, scaleY)` et applique `transform: scale()` sur `#camera` | Letterboxing uniforme. Excellent sur PC et tablette paysage, inutilisable en portrait mobile |
| La taille de carte est une variable CSS **lue une seule fois** | `card.css:2` `--card-width: 127px` ; `move-card.js:344-346` fait un `parseFloat` unique au chargement du module | Un mode densité ou zoom exige un rechargement de page, ou une réécriture de ce module |
| Les positions horizontales sont **calculées en JS**, avec des cas particuliers par identifiant de zone | `move-card.js:16-50` branche sur `parent.id === "player-all-hand-cards"`, `'area-play'`, etc. | Déplacer ou réorganiser les zones n'est pas faisable en CSS seul. Le restylage l'est |
| Environ 60 identifiants d'éléments forment le contrat HTML/JS | `descriptor.js` passe des `parent_div_id` littéraux (`"player-all-allies"`, `"area-schemes-main"`, ...) ; `marvel.html:85-133` les déclare | Tant que ces identifiants existent, le runtime existant fonctionne. C'est le point d'appui de l'étranglement du plateau |
| 5 objets sont exposés sur `window` pour les `onclick` inline | `ui.js:556`, `buttons.js:731`, `cards.js:1123`, `history.js:65`, `settings.js:92` | Un nouveau shell de plateau doit soit conserver ces globales, soit remplacer aussi le HTML qui les appelle |
| Le JS livré est une **sortie de compilation TypeScript sans sources** | 31 fichiers de `js/marvel/` terminent par `//# sourceMappingURL=*.js.map`, aucun `.ts` ni `.map` présent | Modifier `js/marvel/` revient à éditer du code généré, exactement le même problème que le bytecode Python côté moteur. À traiter en lecture seule autant que possible |
| Le pattern d'étranglement est **déjà amorcé** | `main.html:169` ouvre `prepare.html` (nouveau, modules ES) et `main.html:172` ouvre `scene` (ancien) ; les deux coexistent dans le menu | Généraliser cette approche plutôt que d'en inventer une autre |

## Structure de projet recommandée

```
public/
├── main.html                    # menu           [à refondre en place]
├── prepare.html                 # préparation    [nouveau, en cours]
├── gallery.html                 # galerie        [nouveau, remplace cards.html]
├── decks.html                   # decks          [nouveau, remplace deck.html]
├── replay.html                  # replay         [à refondre plus tard]
├── marvel.html                  # plateau        [coquille, choisit le runtime]
│
├── scene.html                   # LEGACY préparation, conservé jusqu'à parité
├── cards.html  deck.html        # LEGACY, conservés jusqu'à parité
│
├── css/
│   ├── ds/                      # DESIGN SYSTEM (nouveau)
│   │   ├── tokens.css           # variables CSS : la source unique
│   │   ├── reset.css            # normalisation, box-sizing, touch-action
│   │   ├── typography.css       # échelle typographique, familles
│   │   ├── primitives.css       # button, panel, dialog, tabs, field, badge
│   │   ├── card-tile.css        # la carte, toutes densités
│   │   └── layout.css           # shell, stack, grid, sheet, safe-area
│   ├── surfaces/                # styles par surface, consomment les tokens
│   │   ├── menu.css  prepare.css  gallery.css  decks.css  replay.css
│   ├── board/                   # NOUVEAU plateau
│   │   ├── board-tokens.css     # override de densité propre au plateau
│   │   ├── zones.css            # géométrie des zones par palier de viewport
│   │   └── hud.css              # prompt, boutons OK/Annuler, barre de phase
│   ├── legacy/                  # ANCIEN, gelé
│   │   ├── menu/style.css  menu/wizard.css
│   │   └── marvel/*.css         # 63 fichiers, gelés puis supprimés
│   └── bridge.css               # mappe les tokens vers les sélecteurs legacy
│
├── js/
│   ├── core/                    # NOUVEAU, partagé par toutes les surfaces
│   │   ├── api.js               # fetch typé des endpoints, cache mémoire
│   │   ├── catalog.js           # index cartes/sets/scénarios/decks
│   │   ├── images.js            # URL d'image carte et boîte, préchargement
│   │   ├── prefs.js             # réglages persistants
│   │   └── result.js            # gestion d'erreur uniforme, pas d'exception nue
│   ├── ds/                      # composants du design system
│   │   ├── card-tile.js  dialog.js  tabs.js  sheet.js  virtual-grid.js
│   ├── surfaces/
│   │   ├── menu/  prepare/  gallery/  decks/  replay/
│   ├── board/                   # NOUVEAU plateau
│   │   ├── session.js           # WS, snapshot, ask, post : la seule porte
│   │   ├── model.js             # snapshot normalisé, indépendant du DOM
│   │   ├── layout.js            # zones → géométrie selon viewport
│   │   ├── render.js            # réconciliation DOM par object_id
│   │   ├── interaction.js       # machine à états de l'ask
│   │   └── fx.js                # file d'animations
│   ├── marvel/                  # LEGACY runtime, gelé, lecture seule
│   ├── module/                  # LEGACY réutilisable, à absorber dans ds/
│   └── lib/                     # tiers vendorés (sortable, tilt, clipboard)
└── fonts/                       # à plat, .woff/.ttf uniquement
```

### Rationale de la structure

- **`css/ds/` et `js/core/` séparés des surfaces :** la seule façon d'obtenir une cohérence visuelle réelle est que chaque surface consomme les mêmes tokens et les mêmes primitives. Les répertoires par surface ne contiennent que ce qui est spécifique.
- **`css/bridge.css` :** pendant la migration, les anciennes pages doivent au minimum ne pas jurer avec les nouvelles. Ce fichier ne redessine pas le legacy, il réécrit les valeurs des anciens sélecteurs (`.custom-btn`, `.w-step`, ...) en fonction des tokens. Coût faible, gain de cohérence immédiat, suppression triviale.
- **`js/marvel/` gelé :** c'est du code généré depuis des sources TypeScript perdues. Chaque modification y est aussi risquée qu'une modification du moteur. Le nouveau plateau vit à côté, dans `js/board/`.
- **`js/board/session.js` comme unique porte vers le protocole :** aucune autre partie du nouveau code ne doit connaître l'existence de `/get_world`, `/get_ask` ou `/post`. C'est ce qui rend le protocole remplaçable et le plateau testable.
- **Pas de sous-dossiers dans `fonts/` :** le serveur réduit le chemin au nom de fichier.
- **Un fichier HTML par surface :** aucune modification Python n'est nécessaire pour ajouter une surface, la route générique `.html` suffit.

## Patterns architecturaux

### Pattern 1 : Étranglement par nom de fichier HTML

**What:** Chaque nouvelle surface est un nouveau fichier `.html` dans `public/`, servi automatiquement par la route générique. L'ancienne page reste accessible sous son ancien nom. Le point d'entrée (le menu) expose la nouvelle, et garde un accès à l'ancienne le temps de la validation.

**When to use:** Pour les cinq surfaces hors-jeu. C'est le mécanisme déjà utilisé pour `prepare.html`.

**Trade-offs:** Zéro modification serveur, retour arrière instantané (on rebascule un lien), deux implémentations à maintenir temporairement. L'URL change (`/scene` devient `/prepare.html`), ce qui est sans conséquence pour une app locale sans liens externes.

**Exemple, l'état actuel dans `main.html` :**

```html
<!-- nouveau, sans aucune route Python ajoutée -->
<button class="custom-btn btn-3" onclick="Open('prepare.html')">Préparer</button>
<!-- ancien, conservé tant que la parité n'est pas atteinte -->
<button class="custom-btn btn-3" onclick="Open('scene')">Préparer (ancien)</button>
```

**Variante pour figer l'URL :** quand la parité est atteinte, une modification d'une ligne dans `server_html.py` fait pointer `/scene` sur le nouveau fichier, et l'ancien devient `/scene_legacy.html`. Utile seulement si l'on veut préserver des URL, ce qui n'est pas un besoin ici.

### Pattern 2 : Étranglement du plateau par coquille avec interrupteur

**What:** Le plateau n'a pas de nom de fichier libre : `server_files.py:11-14` sert `marvel.html` pour toute requête sur `/` avec query string, et le lien de lancement dans `js/prepare/launcher.js` fait `window.location.href = "/?hot_seat"`. La bonne manœuvre est donc de transformer `marvel.html` en coquille minimale qui choisit, à l'exécution, le runtime à charger.

**When to use:** Dès la première étape sur le plateau, avant même d'écrire du nouveau code. C'est l'interrupteur de sécurité qui rend toutes les étapes suivantes réversibles.

**Trade-offs:** Le DOM des zones doit être fourni par le runtime choisi (le legacy exige ses ~60 identifiants), ce qui déplace le corps de `marvel.html` dans un fragment. Coût réel mais unique, et bénéfice immédiat : on peut toujours revenir à l'ancien plateau en pleine partie.

**Exemple de coquille :**

```html
<script type="module">
  const forced = new URLSearchParams(location.search).get('ui');
  const useNew = forced ? forced === 'new'
                        : localStorage.getItem('board_ui') === 'new';
  const mod = useNew ? '/public/js/board/boot.js'
                     : '/public/js/marvel/marvel.js';
  // le runtime injecte son propre DOM de zones et ses feuilles de style
  await import(mod);
</script>
```

`?ui=old` reste toujours disponible comme sortie de secours, y compris après le basculement par défaut.

### Pattern 3 : Tokens CSS comme unique source de vérité, partagés legacy et nouveau

**What:** Un fichier `tokens.css` déclare l'intégralité des décisions visuelles en variables CSS sur `:root`. Les nouvelles surfaces les consomment directement. Les anciennes surfaces les consomment via `bridge.css`, qui réécrit les valeurs des anciens sélecteurs sans toucher aux anciens fichiers.

**When to use:** En tout premier, et sur toutes les surfaces simultanément. C'est le seul livrable qui produit un effet visible partout pour un coût unique.

**Trade-offs:** Les variables CSS n'exigent aucun build, fonctionnent nativement partout, et se modifient à l'exécution (utile pour un mode densité ou un thème). En contrepartie, elles ne sont pas typées et ne se valident pas : la discipline de nommage remplace le compilateur.

**Exemple :**

```css
/* css/ds/tokens.css */
:root {
  /* couleurs, nommées par rôle et non par teinte */
  --c-bg: #0d0f14;
  --c-surface: #171b23;
  --c-surface-raised: #202631;
  --c-text: #e8ecf3;
  --c-text-muted: #9aa4b5;
  --c-accent: #d8232a;          /* rouge Marvel, réservé aux actions */
  --c-focus: #569afe;

  /* ressources du jeu, sémantiques et non décoratives */
  --c-res-physical: #c8442f;
  --c-res-mental: #3f6fc0;
  --c-res-energy: #d8a521;
  --c-res-wild: #6aa84f;

  /* espacement, échelle géométrique */
  --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px;
  --s-6: 24px; --s-8: 32px; --s-12: 48px;

  /* typographie */
  --f-display: 'MarvelRegular', system-ui, sans-serif;
  --f-body: system-ui, -apple-system, sans-serif;
  --t-xs: 12px; --t-sm: 14px; --t-md: 16px; --t-lg: 20px; --t-xl: 28px;

  /* carte : ratio réel d'une carte Marvel Champions */
  --card-ratio: 0.7183;         /* 63 / 87.7 mm */
  --card-w: 127px;              /* densité par défaut, surchargée par palier */
  --card-h: calc(var(--card-w) / var(--card-ratio));
  --card-radius: calc(var(--card-w) * 0.045);

  /* mouvement, une seule échelle pour toute l'app */
  --d-fast: 120ms; --d-base: 200ms; --d-slow: 360ms;
  --e-out: cubic-bezier(.2,.8,.2,1);

  /* profondeur, centralisée pour éviter la guerre des z-index */
  --z-board: 1; --z-card-hover: 40; --z-hud: 60;
  --z-overlay: 80; --z-dialog: 100; --z-toast: 120;
}

@media (prefers-reduced-motion: reduce) {
  :root { --d-fast: 0ms; --d-base: 0ms; --d-slow: 0ms; }
}
```

```css
/* css/bridge.css : les anciennes pages héritent des tokens sans être réécrites */
.custom-btn.btn-3 {
  background: var(--c-surface-raised);
  color: var(--c-text);
  font-family: var(--f-display);
  border-radius: var(--s-2);
}
```

Note importante : le plateau existant déclare déjà `--card-width`, `--card-height`, `--font-size`, `--anime-time`, `--z-index-*`. Le pont doit **aliaser** ces noms vers les nouveaux tokens plutôt que les renommer, sinon `move-card.js` et les 63 feuilles de style du plateau cassent.

### Pattern 4 : Couche anti-corruption devant le protocole moteur

**What:** Un module `session.js` encapsule intégralement le protocole existant et n'expose que des événements de haut niveau. Le reste du nouveau code ne fait jamais de `fetch` vers `/get_world` ou `/post`.

**When to use:** Dès la première ligne de nouveau code de plateau. C'est aussi ce qui permet de rejouer des snapshots enregistrés pour développer et tester le plateau sans lancer de partie.

**Trade-offs:** Une indirection de plus, mais elle isole la partie la plus fragile du système et transforme le plateau en fonction pure du snapshot, donc testable hors ligne.

**Exemple de frontière :**

```js
// js/board/session.js
export const session = {
  connect(),                       // ouvre /ws, gère reconnexion et backoff
  on('snapshot', (state) => {}),   // WorldDescriptor normalisé
  on('ask', (ask) => {}),          // AskOptionPayload normalisé
  on('notify', (n) => {}),         // notifications, achievements, stats
  on('connection', (status) => {}),
  answer({ optionId, targets, resources }),  // POST /post
  ackRendered(),                   // /client_updated, débloque le moteur
};
```

Le protocole réel, mesuré, que cette couche masque :

1. WebSocket `/ws?<query de la page>` pousse un objet léger (`render_id`, `game_id`, `ask_players`, `notify_texts`, `current_step_id`, `remaining_time`).
2. Si `render_id` a changé, le client fait `GET /get_world?p=0` et reçoit le snapshot complet en JSON gzip.
3. Si le joueur local figure dans `ask_players`, le client fait `GET /get_ask?p=<ids>` et reçoit la liste des options.
4. Le client répond par `POST /post?p=<player_id>`, corps `{"id":<option>,"targets":[...],"resources":[...]}`, ou `{}` pour passer.
5. Quand le rendu et les animations sont terminés, `GET /client_updated?p=..&r=<render_id>&g=<game_id>` signale au moteur qu'il peut avancer.

Le point 5 est le détail le plus important : **le moteur attend le client**. Il n'y a donc aucun risque de désynchronisation, mais il y a un risque de blocage si le nouveau code oublie l'acquittement, et un risque de lenteur perçue si la file d'animations est longue. C'est un contrat de vivacité, pas de cohérence.

### Pattern 5 : Snapshot autoritaire, aucune prédiction locale

**What:** Le client ne modifie jamais l'état de jeu de sa propre initiative. Il rend le dernier snapshot reçu. Toute action utilisateur est une réponse à un ask.

**When to use:** Toujours, ici. La littérature sur la prédiction côté client et la réconciliation serveur concerne les jeux temps réel à latence réseau. Ici le serveur est sur `127.0.0.1` et le jeu est au tour par tour : la prédiction n'apporte rien et introduirait des états illégaux impossibles à corriger sans dupliquer les règles, ce qui est explicitement interdit.

**Trade-offs:** Simplicité maximale et impossibilité structurelle de divergence. En échange, le retour visuel immédiat d'un clic doit être purement cosmétique (état pressé, surbrillance, son) et ne jamais anticiper le résultat.

### Pattern 6 : Réconciliation par clé et saut de rendu

**What:** Chaque carte a un `object_id` stable côté serveur. Le rendu indexe les nœuds DOM par `object_id`, calcule un hash de l'état de la carte, et ne retouche que celles dont le hash a changé.

**When to use:** Sur le plateau, obligatoirement. Un plateau réel comporte typiquement de 40 à 120 cartes visibles, plus les piles.

**Trade-offs:** C'est déjà ce que fait le code existant (`descriptor.js:41` `need_render`, `cards.js` `stat_skip_render`). Le nouveau code doit reprendre cette idée, pas la réinventer : le naïf « vider le conteneur et tout recréer » détruit les animations, le focus, et le survol.

### Pattern 7 : Layout de zones déclaratif, avec paliers de viewport

**What:** La géométrie du plateau est décrite comme une donnée, pas comme du CSS dispersé : pour chaque palier de viewport, chaque zone reçoit une position, une taille, un mode de débordement et une priorité de visibilité. Un module unique applique cette table.

**When to use:** C'est le remplacement de `pos-area.css` plus la logique par zone de `move-card.js`. Nécessaire dès qu'on veut du responsive réel.

**Trade-offs:** Plus verbeux qu'un fichier CSS, mais c'est la seule façon d'avoir trois layouts (bureau, tablette, mobile) sans tripler le code, et de rendre la géométrie inspectable et testable.

**Exemple :**

```js
// js/board/layout.js
export const ZONES = {
  mainScheme:  { desktop:{ col:'center', row:1, overflow:'fan' },
                 tablet: { col:'center', row:1, overflow:'fan' },
                 mobile: { tab:'menace',  overflow:'list' } },
  villain:     { desktop:{ col:'center', row:2, overflow:'row' },
                 mobile: { tab:'menace',  overflow:'row' } },
  engaged:     { desktop:{ col:'center', row:3, overflow:'row' },
                 mobile: { tab:'menace',  overflow:'row', badge:'count' } },
  allies:      { desktop:{ col:'center', row:4, overflow:'row' },
                 mobile: { tab:'equipe',  overflow:'grid' } },
  supports:    { desktop:{ col:'center', row:5, overflow:'row' },
                 mobile: { tab:'equipe',  overflow:'grid' } },
  hero:        { desktop:{ col:'center', row:6, overflow:'row' },
                 mobile: { pinned:'bottom', overflow:'row' } },
  hand:        { desktop:{ col:'center', row:7, overflow:'fan' },
                 mobile: { pinned:'sheet', overflow:'fan' } },
  encounter:   { desktop:{ col:'right',  row:2, overflow:'stack' },
                 mobile: { pinned:'rail', overflow:'stack' } },
  // ...
};
```

### Pattern 8 : File d'animations bornée, adossée à l'acquittement

**What:** Les différences entre deux snapshots produisent une liste d'animations (déplacement, dégât, révélation, mélange). La file les joue, avec une durée totale plafonnée, puis appelle `session.ackRendered()`.

**When to use:** Sur le plateau. Le code existant fait déjà cela via `CardAnimation.rest_anime_time()` et un `setTimeout` avant `onUpdateFinished`.

**Trade-offs:** Le plafond de durée est indispensable : sans lui, un tour qui déplace 30 cartes bloque le moteur plusieurs secondes. Prévoir un réglage utilisateur « vitesse d'animation » et le respect de `prefers-reduced-motion`, qui doit court-circuiter la file entièrement.

**Sur l'outil d'animation :** l'API View Transitions same-document est Baseline (Chrome 111+, Firefox 133+, Safari 18+) et fournit gratuitement l'effet FLIP, y compris vers des dimensions inconnues. Elle est adaptée aux transitions d'écran et aux changements de layout. Pour l'animation de 30 cartes simultanées avec des durées individuelles, une implémentation FLIP explicite (mesurer, inverser, jouer via Web Animations API) reste plus contrôlable. Recommandation : View Transitions pour les changements de vue et l'ouverture de panneaux, FLIP explicite pour les cartes. Ne pas compter sur les transitions cross-document, encore derrière un drapeau dans Firefox.

## Flux de données

### Flux 1 : Catalogue (menu, galerie, decks, préparation)

```
[Surface]
   │ catalog.heroes() / catalog.scenarios() / catalog.card(id)
   ▼
[js/core/catalog.js]  ── index en mémoire, résolution des full_link
   │ api.getJSON(url)
   ▼
[js/core/api.js]      ── cache Map par URL, une seule requête par ressource
   │ fetch
   ▼
[Serveur]  get_sets_json | get_cards_json | list_scenarios | get_scenario_json
           list_starter_deck | list_deck | get_hero_json | read_file
           list_encounter_sets | get_encounter_set_json
   │
   ▼
[data/*.json sur disque]
```

Lecture seule, unidirectionnel, aucun état partagé. `cards.json` pèse environ 2,3 Mo : le charger une fois, indexer, et ne jamais le recharger dans une même session de page. Les images de cartes passent par une URL distincte (`/{card_id}`) servie par le cache disque puis les CDN, avec `Cache-Control` d'un an.

### Flux 2 : Lancement de partie

```
[Prepare]  état du wizard (scénario, sets modulaires, héros, difficulté, règles)
   │ buildDescriptor(state)  → NewGameDescriptor
   │   { campaign_json, encounter_set_names, hero_json[], seed,
   │     timeout, challenges, rules[], campaign_log }
   ▼
GET /new?data=<JSON encodé URI>
   │
   ▼
[Moteur]  SceneLoader → World → premier WorldDescriptor
   │
   ▼
[Prepare]  window.location.href = "/?hot_seat"
   │
   ▼
[Serveur]  handle_marvel : query non vide → sert marvel.html
```

Ce contrat est le point de couture le plus fragile de toute la refonte : la forme exacte du `NewGameDescriptor` et la valeur des chaînes de `rules` sont des données non documentées, reconstruites par lecture de l'ancien `scene.html`. `js/prepare/launcher.js` porte d'ailleurs le commentaire « reproduit à l'identique le contrat `/new?data=` de l'ancien `scene.html` ». Toute nouvelle surface de préparation doit réutiliser ce module tel quel plutôt que reconstruire le descripteur.

### Flux 3 : Boucle de jeu

```
[Moteur]  état modifié, render_id incrémenté
   │  push WebSocket /ws
   ▼
[session]  render_id changé ?
   │ oui
   ├──► GET /get_world?p=0  ──► snapshot complet (gzip)
   │       │
   │       ▼
   │    [model]  normalisation : zones, cartes indexées par object_id
   │       │
   │       ▼
   │    [layout] géométrie des zones pour le viewport courant
   │       │
   │       ▼
   │    [render] diff par object_id, saut si hash inchangé
   │       │
   │       ▼
   │    [fx]     file d'animations, durée plafonnée
   │       │
   │       ▼
   │    GET /client_updated?r=..&g=..    ◄── débloque le moteur
   │
   └──► joueur local dans ask_players ?
           │ oui
           ▼
        GET /get_ask?p=..  ──► options[] (EffectDescriptor)
           │
           ▼
        [interaction]  machine à états
           card ──(clic carte porteuse)──► effect ──(choix option)──►
           targets ──(n cibles dans target_num_range)──►
           cost ──(ressources satisfaisant target_payment)──► post
           │
           ▼
        POST /post?p=..  { id, targets[], resources[] }
           │
           ▼
        [Moteur]  résout, nouveau render_id, retour au début
```

### Gestion d'état côté client

Il n'y a **pas d'état de jeu côté client**, et c'est un choix à préserver explicitement. Trois stockages seulement :

| Stockage | Contenu | Durée de vie |
|----------|---------|--------------|
| `session` (mémoire) | dernier snapshot, ask courant, sélection en cours | la partie |
| `catalog` (mémoire) | cartes, sets, scénarios, decks | l'onglet |
| `prefs` (localStorage + cookies) | densité, animations, sons, aides, listes de filtrage de rendu | permanent |

L'existant utilise déjà des cookies pour certaines préférences (`Lib.cookie.setSet` pour les listes blanche et noire de rendu). Ne pas migrer sauvagement vers localStorage sans vérifier que le serveur ne les lit pas.

## Le plateau en détail

### DOM contre canvas : verdict DOM, avec surcouche vectorielle

**Recommandation : DOM et CSS pour les cartes, éléments positionnés pour les flèches et effets. Pas de canvas, pas de WebGL.** Confiance MEDIUM sur la généralité de ce conseil dans le domaine, HIGH sur son adéquation à ce projet précis.

La littérature généraliste sur les jeux web penche vers le canvas pour les performances. Ce conseil est calibré sur des jeux à boucle de rendu continue et des centaines d'entités animées par frame. Il ne s'applique pas ici, pour des raisons mesurables :

| Critère | Réalité de ce projet | Implication |
|---------|---------------------|-------------|
| Nombre d'éléments animés simultanément | 40 à 120 cartes visibles, quelques dizaines en mouvement sur un tour chargé | Très en dessous du seuil où le DOM s'effondre |
| Fréquence de rendu | Événementielle, un rendu par `render_id`, pas de boucle continue | Le principal avantage du canvas ne sert à rien |
| Contenu des cartes | Image JPEG servie par le serveur, plus des surcouches de texte et d'icônes | Le canvas obligerait à réimplémenter la mise en page du texte |
| Interaction | Survol avec prévisualisation, clic, clic droit, glisser, appui long tactile | Le canvas obligerait à réimplémenter tout le test de collision et la gestion du tactile |
| Accessibilité et débogage | Inspecteur d'éléments, sélection de texte, lecteurs d'écran | Perdus entièrement en canvas |
| Acquis existant | Diff par clé, saut de rendu, FLIP, tilt, flèches de ciblage, tous en DOM | Un passage au canvas jette tout cet acquis |

À noter : le projet a déjà tenté le canvas et l'a abandonné. `public/js/marvel/canvas.js` existe (33 lignes, tracé de lignes de ciblage) mais son inclusion est **commentée** dans `marvel.html:253-254`, et l'élément `#canvas` qu'il cible est absent. Les flèches de ciblage en production sont des `div` (`css/marvel/target-arrow.css`). C'est un signal empirique local qui va dans le même sens.

Le seul endroit où une surcouche non-DOM se justifierait est le tracé de courbes de ciblage complexes ou un système de particules. Dans ce cas, préférer un `<svg>` en surcouche plein écran avec `pointer-events: none` : il conserve le modèle déclaratif, s'anime en CSS, et ne demande aucun test de collision.

### Système de layout des zones

Le plateau comporte **environ 25 zones globales et 13 zones par joueur** (`descriptor.js:257-311`). C'est le vrai problème de conception, bien plus que le rendu.

Inventaire par nature, ce qui détermine le traitement de chacune :

| Nature | Zones | Traitement |
|--------|-------|------------|
| Toujours visibles, cartes individuelles importantes | schéma principal, vilain, ennemis engagés, alliés, soutiens, héros, main | Placement explicite, cartes lisibles, jamais réduites en pile |
| Toujours visibles, schémas secondaires | schémas annexes | Placement explicite, éventail si nombreux |
| Piles, seule la carte du dessus compte | paquets de rencontre et de joueur, défausses, paquets additionnels | Rendu en pile avec compteur, une seule carte dans le DOM |
| Transitoires, à mettre en avant pendant leur existence | zone de jeu, en cours de résolution, en révélation, boost, ressources | Surcouche centrée, disparaît quand vide |
| Rarement consultées | affichage victoire, retirées du jeu, mises de côté, némésis, cartes statut, avancées | Repliées derrière un accès secondaire avec compteur, ouvrable en panneau |

Règle de conception qui découle de cet inventaire : **ne pas donner à chaque zone une place permanente sur l'écran**. C'est l'erreur de l'existant, qui déclare les 25 zones dans un plan fixe de 1920x1080 et se retrouve avec des zones vides occupant de l'espace. La hiérarchie recommandée, cohérente avec la pratique du domaine (passé à gauche, présent au centre, ressources à droite) :

```
┌─────────────────────────────────────────────────────────────┐
│ HUD haut : phase, tour, menace, minuterie                   │
├──────┬──────────────────────────────────────────────┬───────┤
│ Rail │                                              │ Rail  │
│ G    │              COLONNE CENTRALE                │ D     │
│      │  schéma principal                            │ ren-  │
│ his- │  vilain + schémas annexes                    │ contre│
│ tori-│  ennemis engagés                             │ défau-│
│ que  │  alliés / soutiens                           │ sse   │
│      │  héros (identité, ressources)                │ paquet│
│ zones│  ─────────────────────────────────────────   │ joueur│
│ re-  │  MAIN (éventail)                             │ compt.│
│ pliées│                                             │       │
├──────┴──────────────────────────────────────────────┴───────┤
│ HUD bas : invite courante, options, OK / Annuler            │
└─────────────────────────────────────────────────────────────┘
```

Les zones transitoires apparaissent en surcouche centrée par-dessus la colonne centrale, pas dans le flux.

### Stratégies de mise à l'échelle responsive

Trois stratégies existent. La bonne réponse est de les combiner par palier, pas d'en choisir une.

| Stratégie | Principe | Convient | Ne convient pas |
|-----------|----------|----------|-----------------|
| Échelle uniforme d'une scène fixe | Concevoir en 1920x1080, `transform: scale(min(sx, sy))` | Bureau, tablette paysage, où le facteur reste au-dessus de 0,6 environ | Portrait mobile : facteur d'environ 0,2, cartes de 25 px. C'est le défaut actuel |
| Zone sûre plus adaptation | Une zone sûre 16:9 jamais réduite ; l'espace supplémentaire est absorbé par étirement, distribution ou marge | Toute la gamme paysage, du 16:9 au 21:9, et les encoches | Ne résout pas à lui seul le changement d'orientation |
| Layout adaptatif par palier | Le plan de zones change de nature selon le viewport ; les zones secondaires deviennent des onglets, des rails ou des panneaux | Portrait mobile, qui exige une réorganisation et non une réduction | Coûte un layout par palier à concevoir et à tester |

Paliers recommandés, avec la densité de carte comme grandeur pilote :

| Palier | Viewport | Stratégie | `--card-w` | Zones secondaires |
|--------|----------|-----------|-----------|-------------------|
| Bureau | largeur >= 1280 | zone sûre 16:9, tout visible | 120 à 140 px | Rails latéraux visibles |
| Tablette paysage | 900 à 1280 | zone sûre, rails condensés | 96 à 112 px | Rails en icônes plus compteur |
| Tablette portrait | 700 à 900, ratio < 1 | adaptatif : main en panneau escamotable | 88 à 104 px | Rails repliés en boutons |
| Mobile paysage | hauteur < 500 | adaptatif : HUD réduit au minimum, main superposée | 72 à 88 px | Tout replié |
| Mobile portrait | largeur < 700, ratio < 1 | adaptatif : onglets de zone (Menace, Équipe, Moi), main en panneau, héros épinglé | 80 à 96 px | Onglets |

Le principe non négociable : **la taille de carte ne descend pas en dessous du seuil de lisibilité (environ 72 px de large pour reconnaître une carte, environ 110 px pour lire son texte)**. Sous ce seuil, on retire des zones de l'écran, on ne rétrécit pas davantage. Le corollaire est qu'un appui ou un survol doit toujours pouvoir agrandir une carte au format lisible, ce qui fait de la prévisualisation un composant central du plateau et non un ornement.

Contraintes tactiles à intégrer dès le layout : cible de 44 px minimum, `touch-action` explicite pour distinguer glisser et défiler, `env(safe-area-inset-*)` pour les encoches, et un remplacement du survol par appui long ou par un panneau d'inspection (l'existant a déjà un `SwipeDetector` dans `window.js`, à reprendre comme précédent).

### Couche d'interaction pour les demandes serveur

C'est la partie la plus sous-estimée de la refonte, et celle qui détermine la qualité perçue. Le serveur envoie une liste d'options ; toute l'ergonomie consiste à ne pas la présenter comme une liste.

Anatomie réelle d'une option (`data.js:2-119`, HIGH confidence) :

| Champ | Sens | Usage UI |
|-------|------|----------|
| `id` | identifiant de l'option, à renvoyer | clé |
| `name` | nom de l'effet, `p_*` signifie une icône | libellé, avec substitution d'icône |
| `bind_id` | carte porteuse de l'effet | c'est **cette carte** qui doit devenir cliquable, pas une entrée de liste |
| `bind_player_id` | joueur concerné | routage du POST |
| `all_legal_targets` | cibles légales | surbrillance des cibles, tout le reste atténué |
| `target_num_range` | `[min, max]` de cibles | compteur « 2 sur 3 », activation du bouton OK |
| `target_payment` | coût par cible, avec `rule` (`UpTo`, `SameType`, `DifferentType`) | affichage du coût sur la carte, validation du paiement |
| `select_rule`, `select_rule_param` | contrainte de sélection | message d'aide contextuel |
| `target_must_include_traits` | traits obligatoires | filtrage visuel |
| `failure_reason` | pourquoi l'option est indisponible | à afficher, c'est un cadeau pour l'utilisateur, actuellement peu exploité |
| `is_search` | l'option ouvre une recherche dans un paquet | ouvre un panneau de recherche, pas une surbrillance |

Machine à états à quatre temps (`select.js`, à conserver dans son principe) :

```
   begin/card ──clic sur une carte ayant des options (bind_id)──► effect
   effect ──choix parmi les effets de cette carte──► targets
   targets ──sélection dans all_legal_targets, contrainte par target_num_range──► cost
   cost ──sélection des ressources satisfaisant target_payment──► POST
   (Annuler ramène à l'état précédent ; OK avance quand l'état est valide)
```

Principes de conception qui découlent directement de cette structure :

1. **Ancrer les affordances sur les cartes, pas dans un menu.** L'option porte un `bind_id` : la carte est le point d'entrée naturel. Un menu global n'est un recours que pour les options sans carte porteuse.
2. **Rendre l'espace de choix évident par soustraction.** Atténuer tout ce qui n'est pas légal est plus lisible que mettre en avant ce qui l'est.
3. **Afficher en permanence l'état de la machine.** Ce qu'on est en train de faire, combien de cibles il reste à choisir, combien il reste à payer. L'existant le fait dans une boîte d'invite, correctement dans le principe.
4. **Rendre l'annulation toujours disponible et toujours au même endroit.** Un ask ne peut pas être annulé côté moteur une fois posté : l'annulation locale avant envoi est le seul filet.
5. **Exposer `failure_reason`.** C'est l'explication du moteur sur ce qui manque. La masquer transforme une contrainte compréhensible en bug apparent.
6. **Traiter les cas dégénérés sans clic.** Une seule option, une seule cible légale, coût nul : l'existant court-circuite déjà (`doPost(false)` en cascade). Conserver ce comportement, avec un réglage pour le désactiver.
7. **Ne pas oublier l'acquittement.** Après rendu et animations, `client_updated`. C'est le seul contrat de vivacité avec le moteur.

## Considérations d'échelle

La grandeur qui monte n'est pas le nombre d'utilisateurs (mono-utilisateur local) mais le nombre de cartes, de zones et de supports.

| Échelle | Ajustements architecturaux |
|---------|---------------------------|
| 1 joueur, 1 scénario, écran de bureau | Le layout fixe de l'existant suffit. C'est le cas déjà couvert |
| 1 joueur, mobile portrait | Layout adaptatif obligatoire, onglets de zone, panneau pour la main, prévisualisation centrale. C'est le vrai saut de complexité |
| 4 joueurs en hot-seat | 4 x 13 zones. Le focus par joueur devient structurant. L'existant a déjà `focusOnPlayer` et un mode « tout-en-un ». Le nouveau layout doit décider tôt entre focus exclusif et vue condensée, car cela change la table des zones |
| Partie longue, 200 cartes ayant existé | Les nœuds DOM de cartes sorties du jeu doivent être libérés, pas seulement masqués. Vérifier que le diff supprime bien les nœuds absents du snapshot |
| Galerie sur la base complète, plus de 4600 cartes | Grille virtualisée obligatoire, et chargement paresseux des images. C'est le seul écran où le volume de données est réellement un enjeu de performance |
| Ajout d'une extension | Aucun impact structurel : le catalogue est dérivé de `cards.json` et `sets_info.json`. À condition de ne rien coder en dur par set dans l'UI |

### Priorités de goulot

1. **Premier goulot : le portrait mobile.** Pas une question de performance, une question de layout. Si l'architecture ne prévoit pas la table de zones par palier dès le départ, le portrait devient une réécriture.
2. **Deuxième goulot : la galerie.** 2,3 Mo de JSON plus des milliers d'images. Virtualisation et chargement paresseux, sinon l'écran est injouable sur tablette.
3. **Troisième goulot : la file d'animations.** Un tour qui déplace beaucoup de cartes bloque le moteur, puisqu'il attend `client_updated`. Plafonner la durée totale.
4. **Non-goulot : le rendu des cartes en DOM.** Mesuré à 40-120 nœuds avec diff et saut de rendu. Ne pas optimiser prématurément.

## Anti-patterns

### Anti-pattern 1 : Réécrire tout le plateau en une seule étape

**What people do:** Traiter le plateau comme une seule phase de roadmap, parce que c'est une seule page.
**Why it's wrong:** Le plateau concentre trois problèmes indépendants et de risques très différents : l'apparence (CSS pur, risque nul), la géométrie et le responsive (JS de layout, risque moyen), et l'interaction avec les asks (JS de protocole, risque élevé, casse le jeu si erreur). Les mélanger rend impossible de livrer quoi que ce soit de sûr, et interdit tout retour arrière partiel.
**Do this instead:** Trois étapes séquentielles derrière l'interrupteur du Pattern 2 : restylage sur DOM inchangé, puis moteur de layout, puis couche d'interaction. Chacune est livrable et réversible.

### Anti-pattern 2 : Modifier `js/marvel/` pour aller plus vite

**What people do:** Retoucher `cards.js` ou `move-card.js` plutôt qu'écrire à côté.
**Why it's wrong:** C'est du JavaScript généré par `tsc` dont les sources TypeScript sont perdues (31 fichiers portant un `sourceMappingURL` orphelin). On y perd la même chose que côté moteur : l'intention. Et les modifications sont invisibles pour tout outillage.
**Do this instead:** Geler `js/marvel/` en lecture seule. Le nouveau plateau vit dans `js/board/`. Si un correctif est indispensable dans le legacy, le marquer comme le projet marque déjà ses divergences moteur.

### Anti-pattern 3 : Renommer les variables CSS existantes du plateau

**What people do:** Remplacer `--card-width` par `--card-w` pour uniformiser la nomenclature.
**Why it's wrong:** `move-card.js:344-346` lit `--card-width` et `--card-height` par `getComputedStyle`, et 63 feuilles de style du plateau les consomment. Le renommage casse le plateau silencieusement, sans erreur console.
**Do this instead:** Les nouveaux tokens sont la source, les anciens noms deviennent des alias : `--card-width: var(--card-w)`. Supprimer les alias seulement quand le legacy correspondant disparaît.

### Anti-pattern 4 : Livrer des assets dans des extensions non routées

**What people do:** Poser un `logo.png`, un `theme.json` ou une police `.woff2` dans `public/`.
**Why it's wrong:** Aucune route n'existe pour ces extensions. La requête tombe sur le fourre-tout image, qui réduit le chemin au nom de fichier, cherche dans les dossiers d'images de cartes, échoue, et renvoie un corps vide avec un `Content-Type: image/jpeg`. Le symptôme est un asset silencieusement vide, pas un 404 clair.
**Do this instead:** SVG à plat pour l'iconographie, `.woff`/`.ttf` à plat dans `fonts/`, données inlinées dans un module `.js`, et tout le reste via les endpoints existants.

### Anti-pattern 5 : Introduire un état de jeu côté client

**What people do:** Mettre en cache l'état des cartes, appliquer optimistement le résultat d'une action, ou dériver localement des règles (« cette carte est jouable donc... »).
**Why it's wrong:** Cela duplique des règles que le moteur détient, en violation directe de la contrainte du projet, et crée des divergences que rien ne peut réconcilier puisque le client n'a pas les règles. Sur `127.0.0.1` en tour par tour, cela n'apporte aucun gain perceptible.
**Do this instead:** Le snapshot est la vérité. Le retour immédiat au clic reste cosmétique. Toute question sur la légalité d'une action se lit dans l'ask, `failure_reason` inclus.

### Anti-pattern 6 : Reconstruire le `NewGameDescriptor` depuis zéro

**What people do:** Réimplémenter la construction du descripteur dans la nouvelle surface de préparation.
**Why it's wrong:** La forme exacte du descripteur et le vocabulaire des `rules` (`mode_skirmish`, `mode_heroic_N`, `v16_all`, `no_crisis_of_infinite_deadpools`, ...) sont non documentés et ont été reconstruits par lecture de l'ancien `scene.html`. Une divergence produit une partie mal configurée, pas une erreur.
**Do this instead:** `js/prepare/launcher.js` est déjà l'adaptateur. Le promouvoir en `js/core/new-game.js` et le traiter comme du code de contrat : modification uniquement avec vérification par lancement réel.

### Anti-pattern 7 : Vider et recréer le conteneur de zone à chaque rendu

**What people do:** `zone.innerHTML = ''` puis recréer les cartes depuis le snapshot.
**Why it's wrong:** Cela détruit les animations en cours, le focus clavier, l'état de survol, la sélection en cours, et provoque un rechargement visuel des images. C'est aussi ce qui rend le FLIP impossible, puisque le nœud d'avant n'existe plus.
**Do this instead:** Diff par `object_id`, avec le saut de rendu par hash que le code existant pratique déjà.

### Anti-pattern 8 : Oublier `client_updated`

**What people do:** Rendre le snapshot et attendre le prochain message WebSocket.
**Why it's wrong:** Le moteur attend l'acquittement pour avancer. Sans lui, la partie se fige sans erreur et sans message.
**Do this instead:** L'acquittement est la dernière instruction du pipeline de rendu, dans `session.js`, systématiquement, y compris en cas d'échec d'animation.

## Points d'intégration

### Endpoints serveur

Aucun n'est à modifier. Colonne « nouveau usage » indique la responsabilité côté client.

| Endpoint | Méthode | Rôle | Nouveau usage |
|----------|---------|------|---------------|
| `/get_sets_json` | GET | métadonnées des extensions | `catalog` |
| `/get_cards_json` | GET | base de cartes complète (environ 2,3 Mo) | `catalog`, une fois par page, indexé |
| `/get_card_json` | GET | une carte | `catalog` (accès ponctuel) |
| `/list_scenarios`, `/get_scenario_json` | GET | scénarios | `catalog` |
| `/get_sets_custom_scenario` | GET | scénarios personnalisés | `catalog` |
| `/list_encounter_sets`, `/get_encounter_set_json` | GET | sets de rencontre et modulaires | `catalog` |
| `/list_starter_deck`, `/list_deck`, `/get_hero_json` | GET | decks de départ et sauvegardés | `catalog` |
| `/read_file` | GET | fichier de données arbitraire, dont `campaign_log_last.json` | `catalog`, journal de campagne |
| `/get_completion_rate`, `/get_statistics`, `/get_session_statistics` | GET | progression et statistiques | menu, écran de rapport |
| `/list_replay_files`, `/get_replay_json`, `/load_replay` | GET | replays | surface replay |
| `/new?data=` | GET | création de partie | `new-game.js` uniquement |
| `/ws` | WS | notification de changement d'état | `session.js` uniquement |
| `/get_world` | GET | snapshot complet, gzip | `session.js` uniquement |
| `/get_ask` | GET | options de la demande courante, gzip | `session.js` uniquement |
| `/post` | POST | réponse du joueur | `session.js` uniquement |
| `/client_updated` | GET | acquittement de rendu | `session.js` uniquement |
| `/debug` | GET | commandes moteur (pas, saut, replay) | outillage de développement uniquement |
| `/{card_id}` | GET | image de carte (JPEG) | `images.js` |
| `/sets/{clé}` | GET | image de boîte d'extension | `images.js` |
| `/save_local`, `/upload_cloudflare` | GET | sauvegarde et envoi de rapport | menu, écran de rapport |

### Frontières internes

| Frontière | Communication | Considérations |
|-----------|---------------|----------------|
| Surface → design system | Import CSS plus modules | Sens unique. Le design system n'importe jamais une surface |
| Surface → `js/core/` | Appel de fonction, promesses | Sens unique. `core` ignore l'existence des surfaces |
| `js/core/api.js` → serveur | `fetch` | Le **seul** endroit du nouveau code où une URL de serveur est écrite, hors `session.js` |
| `js/board/session.js` → serveur | WS plus `fetch` plus POST | Le seul endroit qui connaît le protocole de jeu. Frontière anti-corruption |
| `session` → `model` → `layout` → `render` → `fx` | Pipeline unidirectionnel | Aucun retour en arrière. `fx` ne relit pas le serveur |
| `interaction` → `session.answer()` | Appel unique | L'interaction ne poste jamais directement |
| Nouveau plateau ↔ ancien plateau | Aucune | Ils ne coexistent jamais dans la même page. L'interrupteur choisit à l'exécution |
| `bridge.css` → CSS legacy | Surcharge par sélecteur | Sens unique et temporaire. Ne jamais modifier un fichier de `css/legacy/` |
| Toute surface → moteur Python | Interdit | Aucun accès direct. Tout passe par les endpoints |

## Ordre de construction suggéré

Les dépendances techniques imposent largement l'ordre. Les numéros sont des blocs de travail, pas encore des phases de roadmap : le regroupement final est à l'appréciation du roadmap.

```
[1] Tokens + pont
     tokens.css, reset, typographie, bridge.css, alias des variables du plateau
     dépend de : rien
     débloque : tout
     effet visible immédiat sur les 6 surfaces existantes, y compris le plateau
        │
        ├──────────────────────────────┐
        ▼                              ▼
[2] js/core/                      [3] Primitives + card-tile
     api, catalog, images,             boutons, panneaux, dialogues, onglets,
     prefs, new-game (promu de         champs, la carte à toutes densités,
     js/prepare/launcher.js)           grille virtualisée
     dépend de : rien                  dépend de : [1]
     débloque : [4][5][6][7]           débloque : [4][5][6][7][9]
        │                              │
        └──────────────┬───────────────┘
                       ▼
              [4] Menu (surface pilote)
                   plus petite surface, valide shell, navigation, responsive,
                   tokens en conditions réelles
                   dépend de : [1][2][3]
                       │
                       ▼
              [5] Préparation (achever l'existant)
                   déjà amorcée dans prepare.html ; l'aligner sur le design
                   system, la porter de 4 à 6 étapes, brancher les journaux
                   de campagne
                   dépend de : [1][2][3][4]
                       │
                       ▼
              [6] Galerie de cartes
                   forge card-tile et card-preview sur le plus gros volume de
                   données, sans aucun risque de jeu. Valide la grille
                   virtualisée et le chargement paresseux
                   dépend de : [1][2][3]
                       │
                       ▼
              [7] Gestion de decks
                   réutilise card-tile, la grille et les filtres de [6]
                   dépend de : [6]
                       │
                       ▼
              [8] Replay et rapports
                   plus petites surfaces, réutilisent tout
                   dépend de : [1][2][3]
                       │
                       ▼
   ═══════════════ PLATEAU, trois blocs de risque croissant ═══════════════
                       │
              [9] Plateau A : restylage et interrupteur
                   marvel.html devient une coquille avec bascule ancien/nouveau
                   CSS seul sur le DOM existant : chrome des cartes, HUD,
                   invite, boutons, panneaux, lisibilité
                   ne touche pas js/marvel/
                   dépend de : [1][3]
                   risque : faible. Réversible par ?ui=old
                       │
              [10] Plateau B : session + modèle + layout
                   session.js (anti-corruption), model.js, layout.js avec la
                   table de zones par palier, render.js par diff, fx.js
                   remplace pos-area.css et move-card.js
                   apporte le responsive réel, dont le portrait mobile
                   dépend de : [9], et de [3] pour card-tile
                   risque : moyen. Le jeu doit rester jouable via l'interrupteur
                       │
              [11] Plateau C : couche d'interaction
                   interaction.js : machine à états de l'ask, affordances
                   ancrées sur les cartes, ciblage, paiement, failure_reason,
                   annulation, court-circuits
                   dépend de : [10]
                   risque : élevé. C'est ici qu'une erreur casse une partie
                       │
              [12] Nettoyage
                   suppression de scene.html, cards.html, deck.html,
                   css/legacy/, js/marvel/, bridge.css
                   dépend de : parité constatée sur tout
```

### Raisonnement sur l'ordre

- **[1] avant tout.** Les tokens sont le seul livrable qui améliore les six surfaces d'un coup, avant qu'aucune ne soit refondue. C'est aussi le contrat que tous les blocs suivants consomment : le produire après, c'est retoucher tout ce qui précède.
- **[2] et [3] en parallèle.** Aucune dépendance mutuelle. `core` est de la donnée, `ds` est de la présentation.
- **[4] Menu comme pilote, pas la préparation.** Le menu est la plus petite surface, la plus visible, et sans logique métier. C'est le bon endroit pour valider le shell, la navigation et le socle responsive avant de s'engager sur une surface complexe. La préparation, elle, porte le contrat `/new` : y découvrir en même temps un problème de design system et un problème de contrat moteur serait coûteux.
- **[6] Galerie avant [7] Decks.** La galerie est la forge du composant carte, sur le plus gros volume de données et sans aucun risque. Le deck builder consomme ensuite `card-tile`, la grille virtualisée et les filtres déjà éprouvés. L'ordre inverse ferait naître le composant carte dans un écran à état, ce qui est plus dur à stabiliser.
- **[9] avant [10].** Le restylage ne touche pas au JavaScript et livre l'essentiel de l'amélioration perçue sur le plateau pour un risque quasi nul. Il installe surtout l'interrupteur, qui est la condition de sécurité de [10] et [11].
- **[10] avant [11].** L'interaction a besoin du modèle et de la géométrie pour ancrer ses affordances sur des cartes positionnées. L'ordre inverse est impossible.
- **[11] en dernier sur le plateau.** C'est le seul bloc où un défaut rend une partie injouable. Il bénéficie d'avoir tout le reste validé, et de l'interrupteur comme filet.
- **[12] jamais avant la parité.** La contrainte du projet est explicite : les écrans actuels restent fonctionnels tant que leur remplaçant n'est pas prêt.

### Signaux d'alerte pour la roadmap

| Bloc | Pourquoi il mérite une recherche dédiée avant exécution |
|------|--------------------------------------------------------|
| [5] Préparation | Le contrat `/new?data=` et le vocabulaire des `rules` ne sont pas documentés. Les journaux de campagne des quatre formats (MTS, MG, NeXt, AoA) ont des clés différentes et une validation incomplète |
| [10] Plateau B | La table de zones par palier est une décision de conception, pas une traduction. La géométrie mobile portrait n'a aucun précédent dans le projet |
| [11] Plateau C | Le vocabulaire complet de `select_rule`, `ability_type` et `event_name` doit être inventorié depuis le moteur avant de concevoir l'UI. Un cas non couvert bloque une partie |
| [6] Galerie | Volume de données : mesurer avant de choisir la stratégie de virtualisation |

Les blocs [1], [2], [3], [4], [7], [8], [9] relèvent de patterns standards et ne devraient pas nécessiter de recherche supplémentaire.

## Confiance et lacunes

| Affirmation | Confiance | Base |
|-------------|-----------|------|
| Contraintes de routage statique par extension | HIGH | Lu dans `src/engine/network/web_server.py` |
| Protocole de jeu (WS, snapshot, ask, post, acquittement) | HIGH | Lu dans `server_sync.py`, `server_socket.py`, `client.js`, `buttons.js` |
| Anatomie des options d'ask et machine à états | HIGH | Lu dans `data.js`, `select.js`, `effect.js` |
| Échelle fixe 1920x1080 et calcul JS des positions | HIGH | Lu dans `scene.js`, `marvel.css`, `pos-area.css`, `move-card.js` |
| Étranglement déjà amorcé (`prepare.html` et `scene` coexistants) | HIGH | Lu dans `main.html`, `js/prepare/` |
| DOM plutôt que canvas pour ce projet | HIGH pour ce projet, MEDIUM comme conseil général | Mesures locales plus littérature contradictoire côté canvas |
| Tokens CSS comme socle partagé legacy et nouveau | HIGH | Pratique établie, support natif universel, plusieurs sources concordantes |
| Étranglement par façade de routage | HIGH sur le pattern, adaptation locale par nom de fichier | Azure Architecture Center, Thoughtworks |
| View Transitions same-document utilisable | HIGH | Baseline confirmée (Chrome 111+, Firefox 133+, Safari 18+) |
| Transitions cross-document | LOW, à éviter | Encore derrière un drapeau dans Firefox à ce jour |
| Zone sûre 16:9 plus adaptation par palier | MEDIUM | Une source détaillée (Space Ape Games) plus des sources généralistes concordantes |
| Seuils de lisibilité de carte (72 px, 110 px) | LOW | Estimation dérivée du ratio de carte et de la taille de texte, non validée par mesure. **À vérifier par test sur appareil réel avant de figer la table des paliers** |
| Nombre de cartes DOM simultanées (40 à 120) | MEDIUM | Déduit de la structure du `WorldDescriptor` et des zones, non mesuré en partie réelle. **Mesurable par un simple comptage en partie** |

**Lacunes assumées, à lever pendant l'exécution et non maintenant :**

- Vocabulaire complet de `select_rule`, `ability_type`, `event_name` et `game_area`, à extraire du moteur. Nécessaire pour [11], pas avant.
- Comportement exact du layout à 4 joueurs (focus exclusif contre vue condensée). Décision de conception à trancher au début de [10].
- Format précis des `rules` acceptées par `/new`. Contourné pour l'instant en réutilisant `launcher.js` tel quel.
- Performance réelle sur l'appareil mobile cible. Non mesurable sans l'appareil ; à mesurer dès [9], qui tourne sur le DOM existant.

## Sources

**Code source du projet (HIGH, lecture directe le 2026-07-28) :**
- `src/engine/network/web_server.py` (routage statique, ReadFile, auth, cache)
- `src/engine/device/web/server/` : `server_files.py`, `server_html.py`, `server_get.py`, `server_sync.py`, `server_socket.py`, `server_new_game.py`, `server.py`
- `src/engine/lib/mime_type.py`
- `launcher.py` (RELEASE=1, neutralisation auth et version)
- `public/marvel.html`, `public/main.html`, `public/prepare.html`, `public/scene.html`
- `public/js/marvel/` : `client.js`, `descriptor.js`, `data.js`, `select.js`, `buttons.js`, `cards.js`, `move-card.js`, `scene.js`, `marvel.js`, `canvas.js`
- `public/js/prepare/` : `api.js`, `launcher.js`
- `public/css/marvel/` : `card.css`, `scene.css`, `pos-area.css`, `area.css`, `index.css`, `marvel.css`
- `.planning/codebase/` : `ARCHITECTURE.md`, `STRUCTURE.md`, `STACK.md`, `CONCERNS.md`, `INTEGRATIONS.md`

Note de correction : `.planning/codebase/ARCHITECTURE.md` désigne `public/scene.html` comme le plateau de jeu. C'est inexact. Le plateau est `public/marvel.html` (63 feuilles de style, runtime `js/marvel/`), `scene.html` est l'écran de préparation. `CONCERNS.md` le décrit correctement.

**Patterns de domaine (MEDIUM) :**
- Strangler Fig Pattern, Azure Architecture Center : https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig
- Embracing the Strangler Fig pattern for legacy modernization, Thoughtworks : https://www.thoughtworks.com/insights/articles/embracing-strangler-fig-pattern-legacy-modernization-part-one
- Aspect Ratio Scaling, Mobile and Tablets, Space Ape Games : https://medium.com/the-space-ape-games-experience/aspect-ratio-scaling-mobile-and-tablets-d574ab20a943
- The Card Games UI Design of Fairtravel Battle, GDKeys : https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/
- Choosing the right rendering method for web games, Canvas versus HTML, Gamedev.js : https://gamedevjs.com/articles/choosing-the-right-rendering-method-for-web-games-a-comparison-of-canvas-and-html/
- Using the View Transition API, MDN : https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using
- Smooth transitions with the View Transition API, Chrome for Developers : https://developer.chrome.com/docs/web-platform/view-transitions
- The developer's guide to design tokens and CSS variables, Penpot : https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/
- Design tokens usage guide, GitLab Pajamas : https://design.gitlab.com/product-foundations/design-tokens-using/
- Client-Side Prediction and Server Reconciliation, Gabriel Gambetta : https://www.gabrielgambetta.com/client-side-prediction-server-reconciliation.html
- Building for Production, Vite : https://vite.dev/guide/build

---
*Architecture research for: client web de jeu de cartes piloté par moteur serveur*
*Researched: 2026-07-28*
