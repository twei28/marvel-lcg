# Refonte « Préparer une partie » — Analyse & Plan (Phase 0, sans code)

> Assistant 6 étapes : **Mode → Héros → Decks → Scénario → Difficulté → Récapitulatif**.
> Contrainte : **ne pas modifier les règles du moteur**. Garder l'écran actuel (`scene.html`) fonctionnel tant que la nouvelle version ne l'est pas.

---

## 1. Analyse de l'existant

### 1.1 Frontend actuel
- `public/main.html` — menu principal ; « New Game » → `scene`.
- `public/scene.html` — **écran de préparation monolithique** (HTML + CSS + JS inline, ~2000 l.). Récemment retravaillé en wizard 4 étapes (`wizard.css`, splash KAPOW).
- `public/css/menu/style.css` — vieux style partagé (cards.html, deck.html, replay.html, scene.html).
- `public/css/menu/wizard.css` — surcouche premium (chargée uniquement par scene.html).
- `public/js/module/` — **modules réutilisables** :
  - `card_statistics.js` → charge `cards.json`, expose `const_card_dict` (name, aspect, hp, traits, text…) et `sets_json`.
  - `card_info.js`, `card_preview.js` → rendu détaillé / aperçu d'une carte.
  - `set_info.js`.
- `public/js/marvel/` — runtime de la partie (hors périmètre de la préparation).
- Images : servies par routes serveur — `/<card_id>` (carte), `/sets/<extension>` (boîte), `/banner.svg`, `.svg` via `assets/textures`.

### 1.2 Schémas de données (réels, vérifiés)

**Scénario** (`data/scenarios/*.json`, 108 + 2 custom) — clés :
`name, version, expert(bool), villain[], schemes[], set_aside[], encounters[], encounter_sets[], modular_sets[]`
- `villain[]` = **étapes/vilains** (Ultron : 2 ; The Wrecking Crew : **0** → image via `schemes[0]`). ⚠️ Jamais supposer un seul vilain.
- `schemes[]` = **manigances principales** multi-étapes (chaque item = `"recto,verso"`).
- `encounter_sets[]` = sets de rencontre **obligatoires** (ex. `"standard"`).
- `modular_sets[]` = sets modulaires **recommandés**.
- Variante **Expert** = fichier séparé `*_expert.json`.

**Deck** (`deck/starter/*.json` = 65 decks de base ; + decks sauvegardés) — clés :
`name, version, metadata{url}, hero[], hero_deck[], player_deck[], obligations[], nemesis_set[], set_aside[]`
- `hero[]` = identité (recto/verso). `player_deck[]` = deck d'aspect. `nemesis_set[]`/`obligations[]` = némésis du héros.

**Set de rencontre** (`data/encounter_sets/*.json`, 148) : `name, version, encounters[]`.

**Extensions/Packs** (`data/sets_info.json`, 60 entrées) — clé = `"1. Core Set"`, valeur :
`name(code), scenarios[], heroes[], encounters[], max_id`. → **groupement officiel par extension** (onglets).

**Cartes** (`cards.json`, via `/get_cards_json`) : métadonnées (nom, type, aspect, hp, hand_size, traits, cost, set, text…).

### 1.3 Endpoints (tous déjà disponibles — aucun ajout moteur nécessaire pour lire)
| Endpoint | Rôle |
|---|---|
| `/get_sets_json` | `sets_info.json` (extensions) |
| `/list_scenarios` | fichiers de scénarios (+ custom) |
| `/get_scenario_json?<id>` | un scénario |
| `/list_encounter_sets` | sets de rencontre |
| `/get_encounter_set_json?<id>` | un set |
| `/list_starter_deck` | **65 decks de base** |
| `/list_deck` | **decks sauvegardés** |
| `/get_hero_json?<id>` | un deck (base ou sauvegardé) |
| `/get_cards_json` | toutes les métadonnées cartes |
| `/get_card_json?<id>` | une carte |
| `/get_completion_rate`, `/get_statistics` | options avancées / progression |
| `/get_gamers` | nb de joueurs de la partie en cours |

### 1.4 Contrat de lancement (**à préserver à l'identique**)
`GET /new?data=<NewGameDescriptor JSON encodé>` puis rejoindre via `/?p=<index>` ou `/?hot_seat`.
`NewGameDescriptor = { campaign_json, encounter_set_names[], hero_json[], seed, timeout, challenges[], rules[], campaign_log{} }`
- `campaign_json` = `JSON.stringify(scénario)` (objet scénario brut).
- `encounter_set_names[]` = sets réellement sélectionnés (standard/expert + modulaires).
- `hero_json[]` = `JSON.stringify(deck)` par joueur.
- `seed` = -1 pour aléatoire.

---

## 2. Composants / logique réutilisables
- ✅ `card_statistics.js` (dictionnaire de cartes : aspect, hp, hand_size, traits) → fiches héros, filtres aspect/équipe.
- ✅ `card_info.js` / `card_preview.js` → aperçu de carte au survol / fiche détaillée.
- ✅ Routes images (`/<id>`, `/sets/<ext>`) → portraits, tuiles, illustrations.
- ✅ Règle d'illustration « scénario » : `villain[0] || schemes[0]` (déjà utilisée).
- ✅ Constructeur de payload `/new` (extrait de `scene.html doCreateNewGame`) → à isoler dans un module `launcher`.
- ✅ Endpoints existants (aucun code moteur pour lire les données).

---

## 3. Nouveau modèle de données (interfaces TypeScript)

```ts
// ===== Types bruts (servis par le backend) =====
type CardId = string;              // "01001a" ou "01001a,01001b" (recto/verso)
type Aspect = 'aggression' | 'justice' | 'leadership' | 'protection' | 'basic' | 'pool';

interface Card {                   // /get_cards_json
  card_id: CardId; name: string; type: string;
  aspect?: Aspect; traits?: string[];
  hp?: number; hand_size?: number; cost?: number;
  set?: string; text?: string;
}

interface Extension {              // /get_sets_json (sets_info.json)
  key: string;                     // "1. Core Set"
  code: string;                    // "core"
  scenarios: string[]; heroes: string[]; encounters: string[];
  maxId: string;
}

interface Deck {                   // /get_hero_json, /list_starter_deck, /list_deck
  name: string; version: string; metadata?: { url?: string };
  hero: CardId[]; hero_deck: CardId[]; player_deck: CardId[];
  obligations: CardId[]; nemesis_set: CardId[]; set_aside: CardId[];
}
interface DeckRef {                // pour les listes
  id: string; name: string; heroCardId: CardId;
  source: 'base' | 'saved' | 'imported' | 'last';
  aspects: Aspect[];               // déduits de player_deck via cards.json
}

interface HeroSummary {            // dérivé (decks de base + cards.json)
  id: string;                      // "spider_man"
  heroCardId: CardId; name: string;
  extension: string;               // clé d'extension
  hp: number; handSize: number; traits: string[];
  team?: string;                   // Avengers / X-Men / Guardians… (via traits)
  baseDeckId: string;              // deck de base inclus
}

interface EncounterSet {           // /get_encounter_set_json
  name: string; displayName: string;
  encounters: CardId[]; size: number;
  kind: 'standard' | 'expert' | 'modular' | 'nemesis';
}

// ===== SCÉNARIO = objet central côté adversaire =====
interface Scenario {
  id: string;                      // "ultron", "the_wrecking_crew"
  name: string; version: string;
  extension: string;               // déduit via sets_info
  expert: boolean;                 // variante *_expert disponible/active

  villains: CardId[];              // 0..n étapes/vilains
  schemes: CardId[];               // 1..n manigances principales
  setAside: CardId[];

  encounterDeckBase: CardId[];         // encounters[]
  mandatoryEncounterSets: string[];    // encounter_sets[] (verrouillés)
  recommendedModularSets: string[];    // modular_sets[] (modifiables)

  // ---- Champs ÉTENDUS (absents des JSON actuels — voir §7 décision D2) ----
  modularSlots?: { min: number; max: number };
  specialDecks?: { name: string; cards: CardId[] }[];
  playerCountRules?: Record<number, string[]>;
  specialOptions?: ScenarioOption[];
  setupInstructions?: string[];
  compatibleModes?: GameModeId[];
}
interface ScenarioOption { id: string; label: string; description?: string; default?: boolean; }

// ===== Modes & difficulté =====
type GameModeId = 'solo' | 'hotseat' | 'lan' | 'online' | 'campaign';
interface GameMode { id: GameModeId; label: string; minPlayers: number; maxPlayers: number; }

interface DifficultyConfig {
  base: 'standard' | 'expert';     // charge le scénario ou sa variante *_expert
  skirmish: boolean;               // escarmouche
  heroic: number;                  // 0..8
  standardSet: 'I' | 'II' | 'III';
  modularConfig: 'recommended' | 'custom' | 'random';
  selectedModularSets: string[];   // résolu selon modularConfig + slots du scénario
  scenarioOptions: Record<string, boolean>;
}

// ===== État global de l'assistant =====
type PrepareStep = 0|1|2|3|4|5;    // Mode, Héros, Decks, Scénario, Difficulté, Récap
interface PlayerSlot {
  index: number;
  hero: HeroSummary | null;
  deck: Deck | null;
  deckSource: DeckRef['source'] | null;
}
interface PrepareState {
  step: PrepareStep;
  mode: GameMode;
  players: PlayerSlot[];           // 1..4
  scenario: Scenario | null;
  difficulty: DifficultyConfig;
  seed: number | null;             // null = aléatoire
  timeout: number;
  rules: string[];
  challenges: string[];
  campaignLog: Record<string, string>;
}

// ===== Contrat de lancement (INCHANGÉ) =====
interface NewGameDescriptor {
  campaign_json: string;
  encounter_set_names: string[];
  hero_json: string[];
  seed: number;                    // -1 = aléatoire
  timeout: number;
  challenges: string[];
  rules: string[];
  campaign_log: Record<string, string>;
}

// ===== Validation =====
interface ValidationError { code: string; message: string; step: PrepareStep; }
interface ValidationResult { ok: boolean; errors: ValidationError[]; }
```

**Règles de validation** (avant lancement) :
`EACH_PLAYER_HAS_HERO` · `EACH_HERO_HAS_VALID_DECK` · `SCENARIO_SELECTED` ·
`MANDATORY_SETS_PRESENT` · `MODULAR_COUNT_WITHIN_SLOTS` · `OPTIONS_COMPATIBLE`.

---

## 4. Wireframe textuel

### 4.1 Gabarit persistant (16:9)
```
┌──────────────────────────────────────────────────────────────────────┐
│  PRÉPARER UNE PARTIE     ①Mode ─ ②Héros ─ ③Decks ─ ④Scénario ─ ⑤Diff ─ ⑥Récap │  progress bar
├─────────────────────────────────────────────────┬────────────────────┤
│                                                  │  RÉCAPITULATIF       │
│              ZONE DE SÉLECTION (centre)          │  (persistant, droite)│
│              contenu de l'étape courante         │  Mode ……             │
│                                                  │  J1 ▸ héros ▸ deck    │
│                                                  │  Scénario ▸ vilains   │
│                                                  │  Difficulté ▸ sets    │
├─────────────────────────────────────────────────┴────────────────────┤
│  [◀ Retour]                  [🎲 Aléatoire]              [Continuer ▶] │  nav
└──────────────────────────────────────────────────────────────────────┘
```
Règles : le récap ne change **jamais de place** ; chaque info a une position fixe entre les étapes.

### 4.2 Étapes
1. **Mode** — grandes tuiles : Solo, Coop (hot-seat), Coop (LAN), Campagne. Choix du **nombre de joueurs (1–4)**. Détermine le nombre d'emplacements de héros.
2. **Héros** — `PlayerSlots` (1–4) · `HeroGrid` (portraits) · `SearchBar` · `FilterBar` (extension / équipe / favoris / récents) · `HeroDetail` (fiche : PV, main, traits, némésis). Pas d'explorateur de fichiers.
3. **Decks** — pour chaque joueur : onglets **Deck de base / Sauvegardés / Dernier utilisé / Importer** ; `DeckList` ; `DeckDetail` (aspects, courbe, taille). Le deck de base est proposé par défaut.
4. **Scénario** — `ExtensionTabs` (campagne/extension) · `ScenarioGrid` (grandes tuiles illustrées) · `ScenarioDetail` : nom, **vilain(s)**, extension, particularités de mise en place, sets recommandés, modes compatibles.
5. **Difficulté** — presets **Standard / Expert / Escarmouche / Héroïque** (combinaisons compatibles) · config modulaire **recommandée / personnalisée / aléatoire** (respecte les emplacements du scénario) · options propres au scénario · sélection aléatoire.
6. **Récapitulatif** — synthèse complète + **validation** (liste des blocages) + bouton **Lancer** (désactivé tant qu'invalide).

---

## 5. Arborescence des composants
```
<PrepareApp>                     // racine : détient PrepareState + routing d'étapes
 ├─ <ProgressBar>                // 6 étapes, retour possible aux étapes validées
 ├─ <StepStage>                  // centre : rend l'étape active
 │   ├─ <StepMode>               //   └ <ModeTile> <PlayerCount>
 │   ├─ <StepHeroes>             //   └ <PlayerSlots> <HeroGrid><HeroCard> <SearchBar> <FilterBar> <HeroDetail>
 │   ├─ <StepDecks>              //   └ <DeckSourceTabs> <DeckList><DeckCard> <DeckDetail>
 │   ├─ <StepScenario>           //   └ <ExtensionTabs> <ScenarioGrid><ScenarioTile> <ScenarioDetail>
 │   ├─ <StepDifficulty>         //   └ <DifficultyPresets> <ModularConfig><ModularSetPicker> <ScenarioOptions>
 │   └─ <StepSummary>            //   └ <SummaryReview> <ValidationList> <LaunchButton>
 ├─ <RecapPanel>                 // droite, persistant
 └─ <NavBar>                     // bas : Retour / Aléatoire / Continuer

Partagés : <CardPreview> (survol) · <CardImage> · <Portrait> · <Illustration> · <Tag/AspectBadge> · <Kapow> (splash optionnel)

Services (non visuels) :
 - api.ts        → client des endpoints GET (+ cache cards.json / sets_info)
 - catalog.ts    → construit HeroSummary[] / Scenario[] / EncounterSet[] depuis les données brutes
 - state.ts      → store PrepareState (observable) + navigation
 - validation.ts → règles de §3
 - launcher.ts   → construit NewGameDescriptor + appelle /new + rejoint la partie
 - prefs.ts      → localStorage (favoris, récents, dernier deck)
```

---

## 6. Plan de migration (progressif, l'ancien reste fonctionnel)
- **Phase 0 — Analyse & design** *(ce document, aucun code).*
- **Phase 1 — Fondations** : `public/prepare.html` (coquille) + couche données (`api/catalog/state/types`), **sans toucher** à `scene.html`. « New Game » pointe encore sur `scene`.
- **Phase 2 — Gabarit** : shell (ProgressBar + RecapPanel + NavBar) + navigation d'étapes vide, testable.
- **Phase 3 — Étapes** (une par une, testables) : Mode → Héros → Decks → Scénario → Difficulté → Récap.
- **Phase 4 — Lancement** : `launcher.ts` produit exactement le même `/new?data=` que `scene.html` (test de parité), + validation.
- **Phase 5 — Bascule** : `main.html` « New Game » → `prepare.html` ; `scene.html` gardé en repli (`/scene`).
- **Phase 6 — Finition & retrait** : animations, tokens de design, puis retrait de `scene.html`.

Chaque phase = livrable testable en direct sur le jeu.

---

## 7. Fichiers à créer / modifier
**Créer :**
- `public/prepare.html` — coquille (servie automatiquement par la route `.html`, **aucun code serveur**).
- `public/css/prepare/…` — tokens de design + composants (fond bleu nuit, panneaux ardoise, accents rouge vilain / bleu-doré héros, coins coupés, anim 150–250 ms).
- Front applicatif (voir §8 pour le choix de stack), ex. :
  `types.ts, api.ts, catalog.ts, state.ts, validation.ts, launcher.ts, prefs.ts, components/*` → bundle `public/js/prepare.bundle.js`.

**Modifier (Phase 5 seulement) :**
- `public/main.html` — « New Game » → `prepare.html`.

**Ne PAS toucher :** moteur Python, `scene.html` (jusqu'au retrait final), `menu/style.css`.

---

## 8. Décisions à confirmer avant de coder
- **D1 — Stack.** Recommandé : **TypeScript + esbuild** → 1 bundle statique (`prepare.bundle.js`), composants en **Web Components** (natif, sans framework runtime). Alternative sans build : ESM vanilla + types JSDoc.
- **D2 — Champs scénario étendus** (emplacements modulaires, decks spéciaux, règles par nb de joueurs, options, instructions de mise en place) : **absents des JSON actuels**. Options : (a) dériver le dérivable (étapes = `villains.length`, emplacements ≈ `recommendedModularSets.length` ou règle standard), (b) ajouter des **clés optionnelles** aux scénarios au fil de l'eau, (c) fichier de métadonnées compagnon. Proposition : (a) maintenant + (b) plus tard.
- **D3 — Favoris / récents / dernier deck** : `localStorage` côté client (aucun endpoint requis). OK ?
- **D4 — Palette.** Passer du thème rouge sombre actuel à **bleu nuit / ardoise / rouge-vilain / bleu-doré-héros** comme demandé. OK ?
- **D5 — Modes** exacts à proposer à l'étape 1 (Solo, Hot-seat, LAN, Campagne ?).
