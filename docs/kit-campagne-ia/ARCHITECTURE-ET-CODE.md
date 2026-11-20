# Architecture et code du projet « Narwhal Champions » (Marvel Champions LCG)

> **État au 20/10/2026**, écrit pour être donné à une autre IA qui doit **comprendre où vit chaque chose** avant de
> toucher à un fichier. Tout ce qui est affirmé ici a été **lu dans le dépôt** à cette date (chemins, routes,
> comptes). Le code intégral n'est pas dans ce fichier : il pèse ≈ 72 Mo (≈ 18 M de tokens). Ce fichier est la
> **carte** ; l'**index de l'API du moteur** (`I-index-api-moteur.md`, ≈ 50 000 tokens) est le **plan détaillé** ; le code
> d'une partie précise s'obtient par les **tomes de code** (voir §13).

## 1. Ce que c'est

Un jeu **Marvel Champions : le jeu de cartes** jouable dans un navigateur, solo ou à plusieurs, avec les cartes
officielles et du contenu **fan-made**. Il repose sur le **moteur open source `irefrixs/marvel-lcg`** (Python,
v0.5.9), étendu par le projet (campagnes, mode manuel, multijoueur par sièges, plateau React, scans français,
hauts faits, déroulé de la phase du méchant, etc.). Trois programmes coopèrent :

| Programme | Langage | Dossier | Rôle |
|---|---|---|---|
| **Le moteur** | Python 3.10 | `Fusion/marvel-lcg-src/src/` | les **règles** : monte une partie, résout les capacités de chaque carte, sert HTTP + WebSocket |
| **Les pages du lanceur** | JavaScript (modules ES, sans framework) | `Fusion/marvel-lcg-src/public/` | accueil, préparation de partie, campagnes, deck-builder, galerie, hauts faits… |
| **Le plateau** | TypeScript / React 19 / Vite | `ui-app/` (sources) → `public/app/` (build) | **la table de jeu** : affiche le monde envoyé par le moteur et renvoie les choix du joueur |

Autour : `site/` (l'**orchestrateur** du site en ligne : comptes, salons, un moteur par partie), `navigateur/` (une
version qui fait tourner le moteur **dans le navigateur** via Pyodide), `deploiement/` (scripts de mise en ligne),
`outils/` (outils du dépôt), `ui-check/` (tests d'interface Playwright), `docs/` (documentation).

**Principe de conception : le moteur calcule, l'interface ne connaît aucune règle.** Le moteur sérialise l'état de
la partie en **descripteurs JSON** ; le plateau les dessine et renvoie une réponse à chaque question posée (`ask`).

## 2. L'arborescence du dépôt (racine `Marvel LCG/`)

```
Marvel LCG/
├── CLAUDE.md                     règles du projet pour l'assistant Claude (processus carte, héros, mots-clés)
├── Fusion/marvel-lcg-src/        LE JEU : la SEULE copie vivante du moteur (voir §3)
├── ui-app/                       le plateau React (sources) ; ui-app/deployer.sh le construit dans Fusion/.../public/app
├── ui-check/                     tests d'interface Playwright (130 fichiers de test) + pilotes
├── outils/                       outils du dépôt (palettes, pochettes, uniformiser les scans, vérifier-*.mjs, ce kit)
├── docs/                         la documentation (README.md = l'index) : reference/, rapports/, packs/, superpowers/
├── deploiement/                  mise en ligne (scripts, services systemd, Caddyfile) — secrets exclus du kit
├── site/                         l'orchestrateur du site en ligne (Python) : orchestrateur.py, static/, base de comptes
├── navigateur/                   « play. » : le moteur dans le navigateur (Pyodide), construire.py, publier.py
├── .planning/                    notes de travail : plans, spécifications de chaque pack, journaux, captures
├── LANCEUR-LINUX.sh, JOUER-*.bat lanceurs (Linux / Windows / macOS)
└── medias/, paquets-cartes/      gros binaires et paquets fournis, HORS dépôt (git les ignore)
```

## 3. Le dossier du jeu : `Fusion/marvel-lcg-src/`

```
Fusion/marvel-lcg-src/
├── launcher_fast.py     construit `.game/` (compilation incrémentale + liens symboliques) puis lance le moteur
├── launch.json          la CONFIGURATION du moteur (adresse, dossiers, traduction, serveurs d'images)
├── src/                 le moteur Python (voir §4)
├── data/                les DONNÉES du jeu (voir §5)
├── deck/starter/        un deck de départ par héros (152 fichiers) — c'est lui qui fait apparaître un héros
├── assets/              images (pics = scans EN, pics-fr = scans FR, pics-hd, vignettes), sons, textures
├── public/              les pages et scripts servis au navigateur (voir §7)
├── campagnes/           les campagnes EN COURS du joueur (écrites par /save_campagne)
├── tools/               142 outils et harnais de test Python (voir §10)
├── puzzle/, replays/    positions de test, sauvegardes de parties
├── .game/               ARTEFACT de build (liens + bytecode), jamais une source
└── .game-src/           dossier de TEST : des liens vers src/ + son propre launch.json, sur un port dédié
```

**Pourquoi `.game/` ?** `launcher_fast.py` compile les ≈ 4 500 `.py` une fois puis ne recompile que ce qui a changé,
et lie `data`, `deck`, `public`, `assets` au lieu de les recopier : une modification de `public/` est vue **sans
relancer**, une modification d'un `.py` **exige** de relancer. Les outils de test visent `.game-src/` (jamais
`.game/`, qui ne contient que du bytecode figé).

## 4. Le moteur Python (`src/`)

| Dossier | Contenu | Détail |
|---|---|---|
| `src/main.py`, `engine/engine.py` | point d'entrée : `Engine.Initialize()` → `Engine.EngineRun()` → `Engine.Shutdown()` | cycle de vie du processus |
| `src/engine/` | **la plate-forme** : configuration (`config.py`), journal, utilisateurs, tâches/jobs asynchrones, fichiers, réseau, **le serveur web** | `device/web/server/*.py` |
| `src/game/` | **les règles** | voir ci-dessous |
| `src/cards/` | **les capacités de chaque carte** (≈ 4 600 modules) | `cards/pack/<pack>/<set>/<card_id>.py` |
| `src/core/` | types, utilitaires (checksum de dictionnaire, `Unused`, énumérations) | |
| `src/editor/` | l'éditeur web de cartes (désactivé hors mode développement) | |

### 4.1 Les couches de `src/game/`

| Dossier | Rôle |
|---|---|
| `world/` | **`World`** : l'état d'une partie (phase, zones, joueurs, deck de rencontre, pile de victoire…) et `Initialize()` — **la mise en place en 16 étapes** |
| `scene/` | **`Scene`** : ce qu'on charge pour monter une partie (`loader.py` : scénario, héros, règles, carnet) |
| `game_run/` | `GameSession`, `NewGameDescriptor`, état de la partie en cours |
| `card/` | les **cartes** : `Paper` (la donnée imprimée), `Card`, `CardFace` et ses sous-classes (`Hero`, `Villain`, `Minion`, `MainScheme`, `Upgrade`…), `factory.py` (génère une carte, charge un set, `RandomPick`) |
| `player/` | `Player` : identité, deck, main, ressources, actions |
| `message/` | le **bus de messages** : chaque événement du jeu est un `Message` (`Message.WhenCampaignSetup`, `WhenUnitWouldAttack`…) émis en couple « Would » (annulable) puis « After » |
| `effect/` | `Effect` : un contexte de résolution (`this`, `targets`, initiateur, source) |
| `ability/` | `Ability` (coût + déclencheur + effet), `AbilityType`, `cost_func.py`, `condition/`, et **`factory/`** : les fabriques que les scripts de cartes appellent |
| `operate/` | **les opérations de haut niveau** : `Faces`, `Worlds`, `Search`, `Players`, `CampaignLog`, `Stores`, `SetupCards`… |
| `selector/` | le choix de cibles (`SetTarget`, `range`, filtres) |
| `event/` | le gestionnaire d'événements, l'enregistrement des règles de jeu |
| `render/` | **`to_descriptor.py`** : sérialise le monde en JSON pour le plateau |
| `puzzle/` | l'API `Puzzle.*` : monter une position de test |
| `rule/`, `buff/`, `deck/`, `element/`, `object/`, `statistics/`, `cheat/` | règles optionnelles, bonus temporaires, decks, ressources/coûts, objets du monde, statistiques, triches de debug |

### 4.2 Le serveur (`src/engine/device/web/server/`)

`GameServer` hérite de **dix mixins**, un par famille de routes. Routes (relevées dans le code) :

| Fichier | Routes |
|---|---|
| `server_new_game.py` | `/new` (le **descripteur** de nouvelle partie), `/new_debug`, `/load_replay`, `/load_puzzle`, `/new_game_online`, `/new_game_lan`… |
| `server_sync.py` | `/get_world`, `/get_ask`, `/post` (la réponse du joueur), `/client_updated`, `/debug` |
| `server_socket.py` | `/ws` (WebSocket : pousse l'état aux clients) |
| `server_get.py` | ≈ 60 routes de lecture : `/get_cards_json`, `/get_scenario_json`, `/get_hero_json`, `/get_sets_json`, `/list_scenarios`, `/list_encounter_sets`, `/list_starter_deck`, `/get_achievements`, `/sandbox_command`, routes du **mode manuel**, du **déroulé** (`/set_etape`…) |
| `server_campagne.py` | les 10 routes de campagne (chapitre 9 du manuel) |
| `server_files.py` | images : `/`, `/sets/…`, `/vignette/…`, `/hd/…`, et le fourre-tout `/{path}` |
| `server_html.py` | pages : `/main`, `/replay`, `/salon.html`, `/claim_seat`, `/spectateur`, `/host`, `/peerjs` |
| `server_upload.py`, `server_blueprints.py`, `server_essais.py` | partage de sauvegardes, blueprints multi, essais par compte |

### 4.3 La vie d'une partie, de bout en bout

```
 navigateur                       moteur (aiohttp)                         jeu
 ──────────                       ────────────────                         ───
 GET /new?data=<descripteur>  ──► server_new_game.new_game
                                    NewGameDescriptor(campaign_json, encounter_set_names,
                                                     hero_json[], seed, rules[], campaign_log{})
                                    └► SceneLoader.NewFromJson ──► Scene
                                    └► GameSession ──► World(scene).Initialize()   ◄── 16 étapes (§7 du manuel)
 WebSocket /ws ◄─────────────────  push « le monde a changé »
 GET /get_world  ──────────────►  render/to_descriptor → JSON du monde  (cartes, zones, jetons, ask en cours)
 POST /post {réponse} ─────────►  le Controller résout la réponse ──► Messages ──► Capacités des cartes
                                    └► le monde change ──► nouveau descripteur ──► /ws
 fin de partie ────────────────►  Message.WhenGameOver ──► (campagne) campaign_log_last.json
```

**Le contrat de lancement** (`GET /new?data=…`) est figé dans `ui-check/contrat-nouvelle-partie.json` : clés
`campaign_json`, `campaign_log`, `challenges`, `encounter_set_names`, `hero_json`, `rules`, `seed`, `timeout`
(+ `campaign_json_2`, `encounter_set_names_2`, `teams` pour la bataille).

**Les règles du moteur** sont des listes de drapeaux dans `rules` (`mode_campaign`, `mode_skirmish`,
`mode_heroic_N`, `mode_manuel`, `mode_competitive`, `v16_all`, `v18_all`, `confirm_main_scheme`…).

### 4.4 Comment une carte agit

```
 le joueur joue une carte / un événement se produit
   └► un Message est émis (ex. Message.WhenUnitWouldTakeDamage)
        └► le gestionnaire d'événements interroge toutes les Ability enregistrées pour ce type de message
             └► chaque Ability vérifie ses conditions puis, si elle part, s'exécute : opération(effect, message)
                  └► l'opération appelle des opérations de haut niveau (Faces.DiscardAll, Worlds.FindVillain, player.DrawUp…)
```

Un **script de carte** (`cards/pack/<pack>/<set>/<card_id>.py`) ne fait que **construire** une liste d'`Ability` avec
les fabriques de `game/ability/factory/` ; le moteur les enregistre à la génération de la carte. Le module est
trouvé par `cards/database.py` (voir §6.1 du manuel : set nettoyé puis racine du pack).

## 5. Les données

| Chemin (sous `Fusion/marvel-lcg-src/`) | Contenu |
|---|---|
| `data/cards.json` | **toutes les cartes** (7 713 entrées, 170 packs) + `checksum` |
| `data/cards_custom.json` | un second catalogue (anciennes cartes d'auteurs) |
| `data/sets_info.json` | l'index des packs (168 entrées) : scénarios, héros, sets, `max_id` |
| `data/scenarios/*.json` | 230 scénarios (+ `scenarios_custom/`) |
| `data/encounter_sets/*.json` | 239 sets de rencontre ; `data/nemesis/` 81 sets némésis ; `data/challenges/` 25 défis |
| `data/campagnes/*.json` | les **12 descriptions de campagne** |
| `data/translate_fr.json` | la narration du moteur, traduite par gabarit |
| `data/decks_aspect.json`, `data/identites.json`, `data/palettes-heros*.json`, `data/arts_alternatifs.json`, `data/images_cartes.json` | decks d'aspect, annuaire des identités, couleurs de héros, arts alternatifs, relevé des illustrations |
| `deck/starter/*.json` | 152 decks de départ |
| `assets/pics/` | ≈ 8 100 scans anglais ; `pics-fr/` scans français ; `pics-hd/` ; `vignettes/` ; `sounds/`, `textures/` |

## 6. Les pages du lanceur (`public/`)

| Page / module | Rôle |
|---|---|
| `prepare.html` + `js/prepare/` | **l'assistant de préparation** (accueil, mode, héros, decks, scénario, difficulté) ; `launcher.js` construit le descripteur `/new` ; `catalog.js`, `cards.js`, `api.js`, `langue.js`, `dico-en.js`, `heros-info.js`, `mechants-info.js` |
| `campagne.html` + `js/campagne/` | **l'écran des campagnes** (chapitre 9) : `app.js`, `ordre-libre.js`, `livre-pages.js`, `api-campagne.js`, `brouillon.js` ; `css/campagne/` |
| `deck-builder.html` + `js/deckbuilder/` | le constructeur de decks (règles d'aspect, import marvelcdb/o8d) |
| `galerie.html`, `cards.html`, `achievements.html`, `credits.html`, `nouveautes.html` | galerie, hauts faits, crédits, nouveautés |
| `salon.html`, `rejoindre.html`, `js/salon/` | le **multijoueur par sièges** (un siège = une personne ; `claim_seat`) |
| `app/board.html` | **le plateau** (build de `ui-app/`) |
| `js/traduction/` | copies JS **générées** de la traduction posée sur les scans anglais (`outils/generer-traduction-public.mjs`) |
| `stories/<code>/` | les planches de livret de chaque campagne |
| `releve-images.html`, `palettes-heros.html`, `puzzle_editor.html`, `sandbox.html` | outils réservés (relevé des illustrations, palettes, éditeur de positions, bac à sable) |

## 7. Le plateau (`ui-app/`)

React 19 + TypeScript + Vite, **254 fichiers sources et 359 fichiers de test** (vitest). `ui-app/src/board.tsx` est
le composant racine ; `ui-app/src/board/` contient ≈ 250 modules : la table (`zones.ts`, `Board.tsx`,
`card-model.ts`), les **fenêtres** (réglages, journal, aperçu), **le déroulé de la phase du méchant**
(`DeroulePhase.tsx`, `CartouchePhase.tsx`, « Sur la table »), **le mode manuel** (`manuel/`), **le panneau de
récompenses de campagne** (`campagne/`), le **texte français posé sur les scans anglais** (`TraductionPosee.tsx`),
les **affichages** (Normal, Coloré, Sobre : `affichage.ts`, `styles/affichage-epure.css`). `ui-app/deployer.sh`
construit (`vite build`) et dépose le résultat dans `public/app/`.

Le plateau **ne connaît aucune règle** : il lit `/get_world`, dessine, et répond aux `ask`. Les textes français du
plateau passent par `t()` (dictionnaire `dico-en.ts`).

## 8. Les campagnes dans cette architecture

Voir les chapitres 2, 7, 8 et 9 du manuel (`KIT-CAMPAGNE-COMPLET.md`) : trois couches (données, moteur, description
JSON) + l'écran (`public/js/campagne`) + le panneau (`ui-app/src/board/campagne`) + les routes
(`server_campagne.py`). Le **carnet** est le seul lien entre deux parties.

## 9. Le multijoueur

* **Hot seat** (une machine) et **coop en ligne par sièges** : le siège `p=0` est l'**hôte**, `p=1..3` les invités ;
  un siège est une **personne** (jamais de rotation d'ordre). `salon-etat.js` fait la conversion index technique ↔
  « Joueur N ».
* **Spectateur** (`/spectateur`), **bataille** (`mode_competitive`, deux tables), **mode manuel** (comme OCTGN : le
  moteur ne conduit plus).
* En ligne, **l'orchestrateur** (`site/orchestrateur.py`) lance **un moteur par partie** ; redémarrer le service
  **emporte toutes les parties en cours** (d'où le bandeau de préavis `annonce.js` / `annonce.ts`).

## 10. Les outils et les tests

| Dossier | Contenu |
|---|---|
| `Fusion/marvel-lcg-src/tools/` | **142** outils Python : harnais `test_capacites.py` (+ `cas/*.py`), `test_campagnes.py`, `epreuves_campagnes.py`, `sonde_campagne.py`, `autoplay.py` (un bot joue des parties), `verifier_*.py`, `recalculer_checksums.py`, `importer_*.py` (imports d'auteurs), `generer_vignettes.py`, `pages_livret.py`, `livret_fr.py` |
| `Fusion/marvel-lcg-src/tools/tests-lanceur/` | tests Node des modules purs du lanceur |
| `ui-app/src/**/*.test.ts(x)` | tests vitest du plateau |
| `ui-check/` | tests Playwright : écrans réels dans un navigateur, contre un moteur lancé |
| `outils/` | outils transversaux (palettes, pochettes, scans, vérifications `.mjs`, **ce kit**) |

**Le moteur est un singleton** : un cas de test = un processus. Les harnais ouvrent un port par cas ; ne jamais
laisser la plage atteindre 49152.

## 11. Conventions du dépôt

* Commentaires, journaux et documentation **en français** ; noms de données en anglais.
* **Toute divergence volontaire** avec le moteur d'origine est commentée `# CORRECTIF` (ou `AJOUT`), avec date : sinon
  elle se perd à la prochaine synchro avec `irefrixs/marvel-lcg`.
* Une **gate** n'est une preuve que si on l'a vue échouer.
* Rien de secret dans le dépôt de code : les clés, les mots de passe et l'adresse du serveur n'ont **rien à faire** dans
  ce qu'on donne à une autre IA.

## 12. Les tailles (mesurées le 20/10/2026)

| Partie | Lignes | Taille | Tokens estimés (÷4) |
|---|---|---|---|
| Moteur Python (`engine`, `game`, `core`, `editor`) | 76 548 | 3,3 Mo | 0,8 M |
| Scripts de cartes (`src/cards`) | 264 689 | 9,7 Mo | 2,4 M |
| Plateau React (`ui-app/src` + styles) | 166 198 | 8,1 Mo | 2,0 M |
| Pages du lanceur (`public/js`, `css`, html) | 188 686 | 6,9 Mo | 1,7 M |
| Outils Python (`tools/`) | 122 576 | 6,6 Mo | 1,6 M |
| Données (`data/*.json`) | 173 111 | 33 Mo | 8,3 M |
| Documentation (`docs/*.md`) | 83 644 | 4,2 Mo | 1,1 M |
| **Total** | ≈ 1 M de lignes | ≈ 72 Mo | **≈ 18 M** |

## 13. Comment obtenir « tout le code »

Aucune IA ne lit 18 M de tokens. Trois niveaux, du plus léger au plus lourd :

1. **Ce fichier** (la carte) + **`I-index-api-moteur.md`** (≈ 4 250 classes, fonctions et méthodes publiques du moteur, ≈ 200 Ko, ≈ 50 000 tokens) : à donner à
   **toute** IA qui doit écrire du code pour ce projet.
2. **Le code de ce qui touche à une tâche**, en fichiers séparés (c'est ce que contient `commun/` du kit pour les
   campagnes).
3. **Les tomes de code** : `python3 outils/construire-tomes-code.py --cible moteur` découpe le **code** en tomes
   Markdown de taille réglable (`--taille-ko`, 600 Ko ≈ 150 000 tokens par défaut), à donner un par un. Mesuré le
   20/10/2026, **sans** les données, les images, les fichiers générés, les tests ni les secrets :

| Cible | Fichiers | Taille | Tokens estimés | Tomes de 600 Ko |
|---|---|---|---|---|
| `moteur` (`engine`, `game`, `core`, `editor`, helpers de `cards`) | 468 | 3,3 Mo | 0,8 M | 6 |
| `plateau` (`ui-app/src`, sans tests, + styles) | 301 | 3,8 Mo | 0,9 M | 7 |
| `lanceur` (`public/js`, `css`, `*.html`) | 213 | 2,7 Mo | 0,7 M | 5 |
| `outils` (`tools/*.py`, `outils/`) | 156 | 4,7 Mo | 1,2 M | 4 |
| **Total du code, hors scripts de cartes** | **1 138** | **14,5 Mo** | **≈ 3,6 M** | **22** |

   Les scripts de cartes se donnent **par pack** (`--cible cartes --pack web_of_deceit`). Les données (`data/*.json`,
   33 Mo) ne se donnent **jamais** en bloc : on cite les fichiers utiles ; leurs formats sont décrits dans le manuel.
