---
phase: 01-filet-de-securite
plan: 02
subsystem: testing
tags: [playwright, visual-regression, html-report, node-esm, cli, francais, ux-non-technique]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Harnais ui-check, 18 références figées, scripts npm captures:comparer et captures:valider déjà déclarés"
provides:
  - "`npm run captures:comparer` : page HTML française autonome montrant les 18 couples écran/gabarit avant/après"
  - "`npm run captures:valider` : promotion des références derrière une saisie OUI, sans aucun drapeau de contournement"
  - "Mode démonstration `UI_CHECK_DEMO` : provoque une vraie détection de changement de bout en bout"
  - "`ui-check/scripts/commun.mjs` : lecture de ecrans.ts et des images de test-results, partagée par les deux commandes"
affects: [01-04-bascule-ui-old, 01-06-livraison, 02-fondations-vite, 03-pilotes-carte, 05-plateau-restylage, 06-plateau-layout]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Validation visuelle par page HTML maison, pas par le rapport natif de Playwright (celui-ci n'affiche que les échecs, en anglais)"
    - "Page de comparaison autonome : images copiées dans comparaison/images/, CSS et JS en ligne, zéro requête réseau"
    - "Une seule commande a le droit d'écrire dans references/, et seulement après une saisie OUI"
    - "Scripts Node ESM sans dépendance, messages entièrement en français"

key-files:
  created:
    - ui-check/scripts/comparer.mjs
    - ui-check/scripts/valider.mjs
    - ui-check/scripts/commun.mjs
  modified:
    - ui-check/tests/captures.spec.ts
    - ui-check/package.json

key-decisions:
  - "captures:comparer appelle directement comparer.mjs, qui relance lui-même la vérification : npm passe par cmd.exe où « ; » n'enchaîne pas deux commandes"
  - "Teinte de démonstration = inversion de luminosité à teintes conservées : un simple hue-rotate ne dépasse pas le seuil de tolérance sur les écrans sombres"
  - "readline en forme callback et non promises : la forme promises ne rend jamais la main sur une entrée fermée"
  - "Entrée fermée sans réponse = refus (comportement sûr par défaut)"
  - "comparer.mjs sort en code 0 même quand des écrans ont changé : la page EST le rapport, une différence n'est pas une panne"

patterns-established:
  - "Garde-fous en cascade avant toute écriture dans references/ : mode démo actif, page absente, page plus vieille que test-results"
  - "Contre-vérification systématique après promotion : un écran instable est signalé au lieu d'être figé en silence"
  - "Preuve du chemin d'acceptation par substitution : remplacer une référence par une autre image, valider, vérifier le retour bit à bit"

# Metrics
duration: 37 min
completed: 2026-07-28
---

# Phase 01 Plan 02 : Page de comparaison et validation explicite — Summary

**`npm run captures:comparer` fabrique une page HTML française autonome où les 18 couples écran/gabarit s'affichent avant/après avec curseur de superposition, et `npm run captures:valider` est le seul chemin capable de toucher `references/` — uniquement après une saisie `OUI`.**

## Performance

- **Duration:** 37 min (dont ~10 min d'attente au checkpoint)
- **Started:** 2026-07-28T10:47:00Z
- **Completed:** 2026-07-28T11:24:00Z
- **Tasks:** 3/3 (2 automatiques + 1 checkpoint validé)
- **Files modified:** 5 (3 créés, 2 modifiés)

## Accomplishments

- **Le format de validation demandé dans le CONTEXT existe** : l'utilisateur voit ses écrans avant/après côte à côte dans son navigateur, en français, sans vocabulaire technique. Les écrans inchangés sont visibles eux aussi, avec un badge vert « Aucun changement » : on ne voit pas que les échecs, contrairement au rapport natif de Playwright.
- **La mise à jour silencieuse d'une référence est devenue impossible.** Une seule commande sait écrire dans `references/`, elle pose une question, et toute réponse autre que `OUI` en majuscules annule. Aucun drapeau `--yes` / `--force`, aucune lecture de `process.argv` : la question n'est pas contournable.
- **Le chemin d'acceptation est prouvé, pas supposé.** J'ai remplacé `references/menu/mobile.png` par une autre image, la vérification l'a détectée, `OUI` a régénéré exactement cette image (1 sur 18) et les 18 références sont revenues **bit pour bit** identiques au commit (`git status` vide).
- **Trois garde-fous couvrent les façons réalistes de se tromper** : valider pendant une démonstration, valider sans avoir regardé la page, valider une page périmée. Les trois sortent en code 1 avec un message en français qui dit quoi faire.
- **Le mode démonstration montre une vraie détection de bout en bout** : 18 écrans sur 18 changent, chacun avec son triptyque Avant / Après / Ce qui a changé et son curseur de superposition. L'utilisateur a vu à quoi ressemblera une régression avant qu'il y en ait une.

## Task Commits

1. **Tâche 1 : Page de comparaison avant/après et mode démonstration** — `bd501cf` (feat)
2. **Tâche 2 : Validation explicite des nouvelles références** — `ac376e3` (feat)
3. **Tâche 3 : Checkpoint de vérification humaine** — validé sans réserve par l'utilisateur (pas de commit)

## Files Created/Modified

- `ui-check/scripts/comparer.mjs` (336 lignes) — relance la vérification puis fabrique `comparaison/index.html` : mode d'emploi de 3 lignes, compteur en tête, une section par écran, une ligne par gabarit ; couple inchangé = image de référence + badge vert, couple modifié = Avant / Après / Ce qui a changé + curseur de superposition. Toutes les images sont copiées dans `comparaison/images/`, le CSS et le JS sont en ligne : la page s'ouvre en `file://` sans aucune requête réseau. N'écrit jamais dans `references/`.
- `ui-check/scripts/valider.mjs` (167 lignes) — 3 garde-fous, liste des écrans concernés avec leurs titres français, question, puis `--update-snapshots=changed` suivi d'une contre-vérification. Seul fichier du dépôt contenant `update-snapshots`.
- `ui-check/scripts/commun.mjs` (130 lignes) — lecture de `ecrans.ts` (import natif du TypeScript par Node, avec repli par lecture de fichier), repérage des `-actual.png` / `-diff.png` dans `test-results/`, table des 3 gabarits.
- `ui-check/tests/captures.spec.ts` — mode démonstration `UI_CHECK_DEMO` injecté par `addInitScript` (le `beforeEach` s'exécute avant le `goto`, `addStyleTag` n'aurait rien eu à styler).
- `ui-check/package.json` — `captures:comparer` corrigé en `node scripts/comparer.mjs`.

## Decisions Made

- **`captures:comparer` appelle directement `comparer.mjs`, qui relance lui-même la vérification.** Le script déclaré au plan 01-01 enchaînait deux commandes avec `;`. Ici npm exécute ses scripts via `cmd.exe` (Node est le binaire Windows, `process.platform === 'win32'`), où `;` est un délimiteur d'arguments et non un séparateur de commandes. Mesuré : `spawnSync('a ; b', {shell:true})` livre `[";", "b"]` en arguments de `a`. Faire orchestrer par le script Node est en plus portable, et garantit que la page est toujours plus récente que `test-results/` (ce dont dépend le garde-fou de fraîcheur).
- **Teinte de démonstration = inversion de luminosité à teintes conservées** (`invert(1) hue-rotate(180deg)`), et non `hue-rotate(40deg)`. Mesuré : le `hue-rotate` seul ne fait échouer que 4 écrans sur 18, puis 7 sur 18 avec du sépia. Un `hue-rotate` ne change rien sur un pixel gris, et sur un fond très sombre l'écart reste sous le seuil de tolérance de 0,2 %. Le filtre retenu fait bouger les 18 écrans et donne un rendu lisible (l'équivalent d'un thème clair), pas une bouillie.
- **`readline` en forme callback et non `readline/promises`.** Mesuré : la forme promises ne résout jamais sa promesse quand l'entrée est fermée sans réponse — le script restait bloqué puis sortait en code 13 (« unsettled top-level await »). La forme callback avec un écouteur `close` traite l'entrée fermée comme un refus.
- **Entrée fermée sans réponse = refus.** C'est le comportement sûr : dans le doute, on ne touche pas aux références. Effet de bord constaté : quand la commande passe par `npm` sous `cmd.exe`, une entrée redirigée n'est pas transmise au script, qui annule donc systématiquement. En usage réel (clavier, terminal interactif) la question fonctionne normalement.
- **`comparer.mjs` sort en code 0 même quand des écrans ont changé.** Une différence n'est pas une panne du script : c'est le résultat qu'on va regarder. Le code 1 est réservé aux vraies erreurs (jeu éteint, page introuvable), avec un message qui renvoie vers le message rouge du terminal.
- **Accents dans les textes affichés, y compris dans le terminal.** Vérifié que Node écrit bien de l'UTF-8 ; sur une vraie console Windows il passe par `WriteConsoleW`, donc l'affichage est correct indépendamment de la page de code. Écrire « Vérification » plutôt que « Verification » compte pour un utilisateur non technique.
- **`scripts/commun.mjs` créé** plutôt que de dupliquer ~60 lignes de plomberie entre les deux commandes.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocage] Script npm `captures:comparer` inopérant (`;` sous cmd.exe)**

- **Found during:** Tâche 1
- **Issue:** Le script déclaré au plan 01-01 était `playwright test tests/captures.spec.ts; node scripts/comparer.mjs`. npm exécute ses scripts avec `process.env.ComSpec` (`C:\WINDOWS\system32\cmd.exe`) parce que Node est le binaire Windows. Sous `cmd.exe`, `;` est un délimiteur d'arguments : `comparer.mjs` n'aurait jamais été exécuté, et Playwright aurait reçu trois arguments parasites.
- **Fix:** `captures:comparer` devient `node scripts/comparer.mjs` ; le script relance lui-même la vérification par `spawnSync(process.execPath, [cli, 'test', ...])`.
- **Files modified:** `ui-check/package.json`, `ui-check/scripts/comparer.mjs`
- **Verification:** `npm run captures:comparer` exécute bien les 18 tests puis produit la page ; comportement de `;` mesuré isolément avant correction.
- **Committed in:** `bd501cf` (Tâche 1)

**2. [Rule 1 - Bug] Le mode démonstration ne déclenchait presque rien**

- **Found during:** Tâche 1
- **Issue:** Le `hue-rotate(40deg)` prévu par le plan ne faisait échouer que 4 écrans sur 18 (puis 7 sur 18 avec du sépia). Un `hue-rotate` est neutre sur un pixel gris, et sur un fond quasi noir l'écart reste sous `maxDiffPixelRatio: 0.002`. Une démonstration qui ne montre rien sur les deux tiers des écrans ne remplit pas son rôle.
- **Fix:** Filtre remplacé par `invert(1) hue-rotate(180deg)` (inversion de luminosité, teintes conservées).
- **Files modified:** `ui-check/tests/captures.spec.ts`
- **Verification:** 18 écrans sur 18 détectés comme changés ; sans la variable d'environnement, 18/18 verts.
- **Committed in:** `bd501cf` (Tâche 1)

**3. [Rule 1 - Bug] `readline/promises` bloquait le script sur une entrée fermée**

- **Found during:** Tâche 2
- **Issue:** `await dialogue.question(...)` ne se termine jamais quand l'entrée est fermée sans qu'une ligne ait été lue. Le script sortait en code 13 avec « Detected unsettled top-level await ». Un outil de validation qui se fige au lieu de dire non est un mauvais outil.
- **Fix:** Passage à `node:readline` (forme callback) avec un écouteur `close` qui résout une réponse vide, c'est-à-dire un refus.
- **Files modified:** `ui-check/scripts/valider.mjs`
- **Verification:** `printf 'non\n' | node scripts/valider.mjs` → annule, code 0 ; `printf '' | ...` → annule ; `printf 'OUI\n' | ...` → fige.
- **Committed in:** `ac376e3` (Tâche 2)

**4. [Rule 2 - Manque critique] Contre-vérification après promotion des références**

- **Found during:** Tâche 2
- **Issue:** Le plan demandait de relancer la vérification après `--update-snapshots`, sans dire quoi faire si elle est rouge. Or ce cas a un sens précis : un écran instable (animation, date, nombre aléatoire) vient d'être figé sur une image qu'il ne reproduira pas. Sans traitement, on figeait un piège pour tous les runs suivants.
- **Fix:** Si la contre-vérification échoue, le script sort en code 1 avec un message qui nomme la cause probable et demande de la signaler avant de figer.
- **Files modified:** `ui-check/scripts/valider.mjs`
- **Verification:** Chemin nominal exercé (contre-vérification verte, 18/18) lors du test de substitution.
- **Committed in:** `ac376e3` (Tâche 2)

**5. [Rule 2 - Manque critique] Garde-fous supplémentaires côté validation**

- **Found during:** Tâche 2
- **Issue:** Le plan prévoyait un refus si la page manque, si elle est périmée, et si la démo est active. Deux trous restaient : aucun écran changé (rien à figer, mais le script posait quand même la question), et suppression du dossier `comparaison/` par `comparer.mjs` sans vérifier son nom.
- **Fix:** Sortie propre en code 0 avec « Aucun écran n'a changé : il n'y a rien à figer » ; garde-fou sur le nom du dossier avant tout `rmSync` récursif.
- **Files modified:** `ui-check/scripts/valider.mjs`, `ui-check/scripts/comparer.mjs`
- **Verification:** Les deux chemins exercés.
- **Committed in:** `ac376e3` (Tâche 2)

**6. [Rule 3 - Blocage, périmètre outillage] `scripts/commun.mjs` ajouté**

- **Issue:** ~60 lignes de plomberie (lecture de `ecrans.ts`, repérage des images de `test-results/`, table des gabarits) auraient été dupliquées entre les deux commandes.
- **Fix:** Extraites dans un troisième module, importé par les deux.
- **Files modified:** `ui-check/scripts/commun.mjs` (créé), `ui-check/scripts/comparer.mjs`
- **Verification:** `node --check` sur les trois fichiers ; les deux commandes fonctionnent.
- **Committed in:** `ac376e3` (Tâche 2)

---

**Total deviations:** 6 auto-corrigées (2 blocages, 2 bugs, 2 manques critiques)
**Impact on plan:** Aucune dérive de périmètre. Les deux blocages empêchaient purement et simplement la commande de fonctionner ; les deux bugs auraient rendu l'outil inutilisable au moment où on en aurait eu besoin ; les deux manques critiques protègent le seul chemin capable d'écrire dans `references/`.

## Issues Encountered

- **Les titres d'écrans sont sans accents dans la page** (« Preparation (ancienne) », « Galerie de cartes »). Ils viennent de `ecrans.ts`, écrit en ASCII au plan 01-01, et servent aussi de titres de tests Playwright — donc de noms de dossiers dans `test-results/`. Tout le reste de la page est accenté. Les corriger touche `ecrans.ts`, fichier hors du périmètre de ce plan et susceptible d'être partagé avec d'autres plans : reporté. À faire en une ligne quand `ecrans.ts` sera de nouveau ouvert.
- **Une entrée redirigée n'atteint pas le script quand on passe par `npm`** (`printf 'OUI\n' | npm run captures:valider`) : `cmd.exe` ne la transmet pas, le script voit une fin d'entrée et annule. Sans conséquence en usage réel (l'utilisateur tape au clavier), mais à savoir pour tout test automatisé futur : il faut appeler `node scripts/valider.mjs` directement.
- **Le compteur de la page compte les couples écran/gabarit, pas les écrans** : « 18 écrans sur 18 » désigne les 6 écrans × 3 formats. Formulation conservée telle que demandée par le plan.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**Prêt pour la suite de la phase 1.** Le filet de sécurité est désormais complet côté écrans statiques : détection (01-01), lecture du résultat (01-02), états de plateau rejouables (01-03).

- Toute phase de refonte visuelle dispose maintenant du rituel complet : `npm run captures` pour détecter, `npm run captures:comparer` pour montrer, `npm run captures:valider` pour figer après accord.
- Le format de validation est validé par l'utilisateur lui-même, sur pièces : il a vu la page normale (18 « Aucun changement ») et la page de démonstration (18 changements avec triptyque et curseur), sans demander de modification.

**Points de vigilance à transmettre :**

- **`npm run captures:valider` est le seul chemin autorisé vers `references/`.** Aucun plan futur ne doit appeler `--update-snapshots` directement, ni ajouter un drapeau de contournement : `grep -rn "update-snapshots" ui-check/` doit continuer à ne remonter que `valider.mjs`.
- **Les titres d'écrans de `ecrans.ts` servent de noms de dossiers dans `test-results/`.** Les renommer casse le repérage des images par `commun.mjs` le temps d'un run (le suivant repart proprement) ; ce n'est pas grave, mais il faut le savoir.
- **Node est le binaire Windows et npm exécute ses scripts via `cmd.exe`.** Ni `;` ni `&&` POSIX, ni variables d'environnement passées en préfixe depuis WSL (il faut `WSLENV`). Tout script npm de ce dépôt doit rester une commande unique.
- La référence de l'écran Replays reste quasi vide par nature (point hérité de 01-01).

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*
