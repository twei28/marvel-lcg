---
phase: 01-filet-de-securite
plan: 01
subsystem: testing
tags: [playwright, visual-regression, screenshots, wsl, launcher-fast, chromium]

# Dependency graph
requires: []
provides:
  - "Commande unique `npm run captures` : 6 écrans × 3 gabarits comparés aux références"
  - "18 images de référence versionnées dans ui-check/references/"
  - "Table déclarative des écrans (ui-check/ecrans.ts), point d'entrée unique pour ajouter un écran"
  - "Contrainte d'intouchabilité de public/js/marvel/ actée dans PROJECT.md"
  - "Boucle de dev actée : launcher_fast.py, édition à chaud vérifiée"
  - "Scripts npm complets réservés pour les plans 01-02 à 01-05"
affects: [01-02-comparaison, 01-03-fixtures, 01-04-bascule-ui-old, 01-05-contrat-new, 02-fondations-vite, 05-plateau-restylage]

# Tech tracking
tech-stack:
  added: ["@playwright/test 1.62.0 (épinglé, sans ^)", "Chromium bundled Playwright v1234 (Chrome for Testing 151.0.7922.34)"]
  patterns:
    - "Table d'écrans déclarative : un écran = une ligne dans ecrans.ts, le spec boucle dessus"
    - "Harnais hors du livrable : ui-check/ vit dans le dépôt Desktop, jamais dans marvel-lcg-src/"
    - "Deux garde-fous avant toute capture : titre != page d'avertissement de cache, marqueur visible"
    - "Réseau externe bloqué et Math.random figé pendant les captures"

key-files:
  created:
    - ui-check/package.json
    - ui-check/playwright.config.ts
    - ui-check/ecrans.ts
    - ui-check/global-setup.ts
    - ui-check/tests/captures.spec.ts
    - ui-check/references/ (18 PNG)
    - .gitignore
  modified:
    - .planning/PROJECT.md

key-decisions:
  - "Marqueur de scene.html corrigé en #w-stepper : #mode est dans un panneau de wizard en display:none"
  - "Marqueur de replay.html renforcé en #replay-items au lieu de body : body ne prouve rien"
  - "Garde-fou anti clean_cache par le titre de page, indépendant du marqueur d'écran"
  - "prepare.html inclus comme 6e écran (preparation-nouvelle)"

patterns-established:
  - "Génération des références en 4 temps : chauffe jetée → génération → 2 contrôles verts consécutifs"
  - "Aucune montée de version de Playwright sans re-validation des 18 références"

# Metrics
duration: 12 min
completed: 2026-07-28
---

# Phase 01 Plan 01 : Socle du filet de sécurité — Summary

**`npm run captures` compare 6 écrans × 3 gabarits à 18 références figées avec Playwright 1.62.0 épinglé, et la boucle de dev est passée sur `launcher_fast.py` (édition à chaud prouvée).**

## Performance

- **Duration:** 12 min
- **Started:** 2026-07-28T10:34:43Z
- **Completed:** 2026-07-28T10:46:52Z
- **Tasks:** 3/3
- **Files modified:** 25 (7 fichiers de code/config + 18 PNG)

## Accomplishments

- **Les deux contraintes d'environnement sont écrites**, pas seulement connues : `public/js/marvel/` a le même statut d'intouchabilité que le moteur, et le serveur de développement est `launcher_fast.py`. Elles sont dans `## Constraints` et dans `## Key Decisions` de PROJECT.md.
- **L'édition à chaud est prouvée par mesure** : un fichier créé dans `public/` alors que le serveur tourne est servi en 200 avec son vrai contenu. Sous `launcher.py`, il aurait été en 404 silencieux.
- **Le filet de sécurité visuel fonctionne** : une commande unique, verte deux fois de suite, qui deviendra rouge dès qu'un pixel change sur l'un des 6 écrans.
- **Les 18 références sont sur le disque et versionnées**, toutes distinctes (aucune n'est la page d'avertissement de cache), aucune sous-dimensionnée sans explication.
- **Le harnais n'a aucune référence à `js/marvel`** : la contrainte d'intouchabilité est respectée dès le premier outil construit.

## Task Commits

1. **Tâche 1 : Acter les contraintes et basculer la boucle de dev** — `9a7666e` (docs)
2. **Tâche 2 : Installer ui-check/ et sa configuration** — `21f0925` (chore)
3. **Tâche 3 : Écrire le test de captures et figer les 18 références** — `0341cd7` (test)

## Files Created/Modified

- `.planning/PROJECT.md` — 2 contraintes ajoutées (runtime de partie, boucle de dev) + 1 décision clé
- `.gitignore` — 6 entrées ; `ui-check/references/` volontairement NON ignoré
- `ui-check/package.json` — Playwright épinglé `1.62.0` sans `^`, `private`, `type: module`, 6 scripts npm en français (dont 4 réservés aux plans suivants)
- `ui-check/playwright.config.ts` — 3 gabarits (pc 1920×1080, tablette 1180×820, mobile 390×844), `snapshotPathTemplate` lisible, `fullyParallel: false`, `maxDiffPixelRatio: 0.002`
- `ui-check/ecrans.ts` — table déclarative des 6 écrans, entièrement commentée en français : c'est le seul fichier à comprendre pour ajouter un écran
- `ui-check/global-setup.ts` — pose le cookie `app_version` via `/get_version`, refuse de démarrer avec un message en français si le jeu n'est pas lancé
- `ui-check/tests/captures.spec.ts` — boucle sur `ECRANS`, blocage du réseau externe, `Math.random` figé, 2 garde-fous puis `toHaveScreenshot`
- `ui-check/references/**.png` — 18 images (6 écrans × 3 gabarits), 5,3 Mo au total

## Decisions Made

- **Marqueur de `scene.html` : `#w-stepper` au lieu de `#mode`.** Mesuré sur le HTML réellement servi : `#mode` est un `<details>` enfermé dans une `section.w-step-panel` en `display: none` (le wizard ne montre que l'étape courante). Sa hauteur mesurée est 0. `#w-stepper` (la barre d'étapes) est le repère visible au chargement dans les 3 gabarits.
- **Marqueur de `replay.html` : `#replay-items` au lieu de `body`.** `body` existe aussi sur la page d'avertissement de cache : ce n'est pas un garde-fou. `#replay-items` est masqué dans le HTML initial mais affiché par le JS une fois la liste chargée, ce qui en fait une preuve d'affichage complet.
- **Garde-fou anti-cache indépendant du marqueur.** Le test vérifie d'abord que le titre de la page n'est pas `Version Mismatch` (titre de `clean_cache.html`), avec un message d'erreur explicite. Ce contrôle reste valable même pour un écran dont le meilleur marqueur serait faible.
- **`prepare.html` retenu comme 6e écran** (`preparation-nouvelle`), conformément à la recommandation de la recherche : coût marginal d'une ligne, et c'est la page déjà en cours d'étranglement.
- **Les 4 scripts npm des plans suivants (`comparer`, `valider`, `fixtures`, `bascule`, `lancement`) sont écrits dès maintenant**, même si leurs fichiers cibles n'existent pas : cela évite que plusieurs plans se disputent `package.json`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocage] Port 2345 en TIME_WAIT au redémarrage du serveur**

- **Found during:** Tâche 1 (bascule sur `launcher_fast.py`)
- **Issue:** Après l'arrêt de `launcher.py`, `launcher_fast.py` a crashé sur `AssertionError: ip='127.0.0.1', port=2345`. Cause identifiée dans `src/engine/network/net_lib.py:30-43` : `IsPortAvailable` fait un `bind()` sans `SO_REUSEADDR`, qui échoue tant que des connexions TIME_WAIT subsistent sur le port. Ce n'est pas un bug du jeu, c'est une conséquence normale de l'arrêt brutal.
- **Fix:** Script de démarrage qui attend la libération effective du port (sonde `bind` toutes les 2 s, 90 tentatives max) avant de lancer `launcher_fast.py`.
- **Files modified:** aucun fichier du dépôt (script jetable dans `/tmp`)
- **Verification:** `curl /main.html` → 200 après 7 tentatives ; processus `launcher_fast.py` en cours
- **Committed in:** `9a7666e` (Tâche 1)

**2. [Rule 1 - Bug] Marqueur `#mode` inopérant pour `scene.html`**

- **Found during:** Tâche 3 (passe de chauffe)
- **Issue:** Les 3 tests de `Préparation (ancienne)` échouaient : `#mode` résolu mais `hidden`. La table de RESEARCH datait d'avant la surcouche `wizard.css`, qui masque les panneaux d'étapes non courants. Un marqueur faux fait échouer 3 runs sur 18 en permanence.
- **Fix:** Sonde de la chaîne de parents via Playwright (`display: none` sur `section.w-step-panel` confirmé), puis remplacement par `#w-stepper`, vérifié visible en 1920×1080 et en 390×844.
- **Files modified:** `ui-check/ecrans.ts`
- **Verification:** 18/18 verts, deux runs consécutifs
- **Committed in:** `0341cd7` (Tâche 3)

**3. [Rule 2 - Manque critique] Garde-fou anti `clean_cache` renforcé**

- **Found during:** Tâche 2 (vérification des marqueurs contre le HTML servi)
- **Issue:** Le plan proposait `body` comme marqueur pour 3 écrans sur 6. Or `body` existe aussi sur `clean_cache.html` : le garde-fou censé empêcher de figer 18 fois la page d'avertissement ne garantissait rien pour ces écrans.
- **Fix:** (a) assertion universelle sur le titre de page (`!== 'Version Mismatch'`) avant chaque capture, avec message d'erreur explicite ; (b) marqueurs `body` remplacés par de vrais sélecteurs (`#found_cards`, `#deck_editor`, `#replay-items`).
- **Files modified:** `ui-check/tests/captures.spec.ts`, `ui-check/ecrans.ts`
- **Verification:** les 18 empreintes SHA-256 des références sont distinctes ; les images ont été inspectées visuellement
- **Committed in:** `0341cd7` (Tâche 3)

---

**Total deviations:** 3 auto-corrigées (1 blocage, 1 bug, 1 manque critique)
**Impact on plan:** Aucune dérive de périmètre. Les trois corrections étaient nécessaires pour que le filet de sécurité soit réellement fiable ; le plan demandait d'ailleurs explicitement de vérifier les marqueurs contre le HTML réel.

## Issues Encountered

- **Le contrôle `find references -name '*.png' -size -10k` remonte 2 fichiers** (`replay/mobile.png` 3,6 ko et `replay/tablette.png` 5,5 ko) là où le plan attendait aucune sortie. Ce n'est pas une capture ratée : l'écran Replays est réellement quasi vide tant qu'aucune partie n'a été enregistrée. Les deux images ont été ouvertes et inspectées : elles contiennent bien le bloc « Game Replay » rendu sur le fond sombre de la page. Le vrai contrôle anti-image-vide, l'unicité des 18 empreintes, passe. À garder en tête : la référence de cet écran devra être régénérée le jour où des replays existeront.
- Le serveur a été relancé, ce qui **coupe toute partie en cours**. L'avertissement prévu par le plan a été affiché avant l'opération.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**Prêt pour 01-02-PLAN.md** (page de comparaison avant/après + validation explicite des références) :

- `references/` est peuplé et versionné : `scripts/comparer.mjs` a de quoi comparer.
- Les scripts `captures:comparer` et `captures:valider` sont déjà déclarés dans `package.json`, il ne reste qu'à écrire les deux fichiers `scripts/*.mjs`.
- `ui-check/comparaison/` est déjà gitignoré.

**Points de vigilance à transmettre :**

- Le serveur doit tourner sous `launcher_fast.py` pour tous les plans suivants (fixtures, bascule `?ui=old` : ils ajoutent des fichiers dans `public/`, invisibles sous `launcher.py`).
- Toute montée de version de `@playwright/test` change le Chromium embarqué, donc le rendu, donc les 18 références. À traiter comme un événement qui exige une re-validation, jamais comme une mise à jour de routine.
- La référence de l'écran Replays est quasi vide par nature ; elle ne détectera de régression que sur le cadre de la page tant qu'aucun replay n'existe.

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*
