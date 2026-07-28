---
phase: 01-filet-de-securite
verified: 2026-07-28T13:03:54Z
status: passed
score: 4/4 vérités observables vérifiées (26/26 must_haves des 6 plans confirmés dans le code réel)
---

# Phase 1 : Filet de sécurité et boucle de dev — Vérification

**Objectif de la phase** : Disposer d'un moyen objectif de détecter toute régression visuelle ou fonctionnelle avant la première ligne de refonte.
**Vérifié le** : 2026-07-28
**Statut** : passed
**Vérification humaine** : 3 checkpoints bloquants déjà approuvés pendant l'exécution (page de comparaison avant/après ; aller-retour `?ui=old` + partie jouable de bout en bout ; contrôle de livraison finale). Non re-signalés ici.

## Méthode

Vérification goal-backward, à partir du code réellement présent sur disque (pas des SUMMARY) :
- Lecture directe de tous les fichiers produits (harnais `ui-check/`, codebase vivant `~/marvel-work/fusion/marvel-lcg-src/public/`, outils `~/marvel-work/tools/`).
- **Exécution réelle** des 4 commandes du filet contre le serveur `launcher_fast.py` déjà en marche (`npm run captures`, `npm run fixtures`, `npm run bascule`, `npm run lancement`) — pas seulement lecture du code des tests.
- Contrôle du livrable zippé par inspection `zipfile` (pas de `unzip` disponible dans cet environnement).
- Contrôle md5 de `test_autoplay.py` (intouchabilité moteur).
- Recherche exhaustive de toute référence à `public/js/marvel/` dans les fichiers ajoutés (contrainte d'intouchabilité étendue).
- Scan anti-patterns (TODO/FIXME/placeholder/stub) sur tous les fichiers livrés par la phase : aucun trouvé.

## Goal Achievement

### Vérités observables (critères de succès de la phase)

| # | Vérité | Statut | Preuve |
|---|--------|--------|--------|
| 1 | Une commande unique capture les écrans actuels (6 écrans × 3 gabarits) et signale toute différence visuelle | ✓ VERIFIED | `npm run captures` exécuté en direct : **18/18 tests verts** (32.8s) contre le serveur réel sur le port 2345. `ecrans.ts` déclare 6 écrans (menu, préparation ancienne, préparation nouvelle, cartes, decks, replays) ; 18 PNG de référence présents sur disque, un par couple écran/gabarit, aucun n'est la page `clean_cache` (garde-fou "Version Mismatch" présent dans `captures.spec.ts` et `global-setup.ts`). Note : ROADMAP.md mentionne encore "5 écrans" dans le texte du critère d'origine — le harnais en couvre 6 (l'écran "préparation-nouvelle" a été ajouté en 01-04), ce qui est une sur-couverture, pas une régression. |
| 2 | 20 à 40 fixtures `get_world` issues de l'autoplay sont rejouables hors partie | ✓ VERIFIED | 34 modules `.js` dans `public/js/fixtures/` (+`index.js` catalogue), issus de 5 couples scénario/héros (rhino/spider_man, rhino/daredevil, klaw/captain_marvel, absorbing_man/she_hulk, god_of_lies/hercules). Couverture confirmée : mise-en-place, side-scheme, sbire-en-jeu, statuts, fin-de-partie présents pour plusieurs couples, plus cas spécifiques (main-pleine, stade-2, carte-mise-de-cote, défausse-rencontre-pleine). `npm run fixtures` exécuté en direct : **1/1 test vert** (19.2s, boucle sur les 34 entrées du catalogue, ≥10 cartes affichées et 0 erreur console à chaque fois). `dump_get_world.py` prouvé identique à `/get_world` via `game.world.render.descriptor` (même expression que le serveur, cf. commentaire ligne 8-9 du fichier). `test_autoplay.py` intact — md5 `59fe6f37d7bef387b6175c8688f5cdad` confirmé. |
| 3 | Sur toute page en cours de migration, `?ui=old` ramène à l'ancienne version et le jeu reste jouable de bout en bout | ✓ VERIFIED | `npm run bascule` exécuté en direct : **4/4 tests verts** (aiguillage sans préférence, `?ui=old` bascule, mémorisation sans paramètre, bandeau ramène à la nouvelle version). Aiguillage inline en tête du `<head>` de `prepare.html` (`location.replace('/scene.html'...)`), `ui-switch.js` posé sur les deux pages avec `data-role` opposés. Le "jeu reste jouable de bout en bout" depuis l'ancienne version a été vérifié par l'utilisateur au checkpoint bloquant 01-04 (non re-testé ici, déjà humain-validé). |
| 4 | Un test automatisé vérifie qu'une partie se lance depuis l'écran de préparation actuel et atteint le plateau, contrat `/new?data=` gelé | ✓ VERIFIED | `npm run lancement` exécuté en direct : **2/2 tests verts** (3.4s) : le contrat rejoué seul crée une partie, et le parcours complet dans le navigateur intercepte la vraie requête `/new?data=`, la compare aux 8 clés typées de `contrat-nouvelle-partie.json` (`campaign_json`, `campaign_log`, `challenges`, `encounter_set_names`, `hero_json`, `rules`, `seed`, `timeout`), puis prouve l'arrivée au plateau via `/get_world`. Avertissement en français présent dans le test ("cette commande lance une NOUVELLE partie..."). |

**Score : 4/4 vérités vérifiées.**

### Artefacts requis (par plan)

| Plan | Artefact | Existe | Substantiel | Câblé | Statut |
|------|----------|--------|-------------|-------|--------|
| 01-01 | `.planning/PROJECT.md` (intouchabilité `public/js/marvel/` + `launcher_fast.py`) | ✓ | ✓ (mentions lignes 20, 46, 60-61, 73) | ✓ | ✓ VERIFIED |
| 01-01 | `ui-check/package.json` (Playwright 1.62.0 épinglé) | ✓ | ✓ | ✓ | ✓ VERIFIED |
| 01-01 | `ui-check/playwright.config.ts` (3 gabarits, snapshotPathTemplate) | ✓ | ✓ (65 lignes) | ✓ (globalSetup référencé) | ✓ VERIFIED |
| 01-01 | `ui-check/ecrans.ts` (table ECRANS) | ✓ | ✓ | ✓ (importé par captures.spec.ts) | ✓ VERIFIED |
| 01-01 | `ui-check/global-setup.ts` (cookie app_version) | ✓ | ✓ (`get_version` présent) | ✓ | ✓ VERIFIED |
| 01-01 | `ui-check/tests/captures.spec.ts` | ✓ | ✓ | ✓ | ✓ VERIFIED |
| 01-01 | `ui-check/references/` (18 PNG) | ✓ | ✓ (18 fichiers confirmés, 6×3) | ✓ (consommés par toHaveScreenshot) | ✓ VERIFIED |
| 01-02 | `ui-check/scripts/comparer.mjs` | ✓ | ✓ (336 lignes) | ✓ (script npm `captures:comparer`) | ✓ VERIFIED |
| 01-02 | `ui-check/scripts/valider.mjs` | ✓ | ✓ (167 lignes, gate `OUI` confirmé ligne 123) | ✓ (script npm `captures:valider`, **non exécuté** volontairement sur consigne explicite) | ✓ VERIFIED |
| 01-02 | Mode démo `UI_CHECK_DEMO` | ✓ | ✓ (présent dans captures.spec.ts) | ✓ | ✓ VERIFIED |
| 01-03 | `~/marvel-work/tools/dump_get_world.py` | ✓ | ✓ (`render.descriptor` présent) | ✓ | ✓ VERIFIED |
| 01-03 | `public/js/fixtures/index.js` (catalogue) | ✓ | ✓ (34 entrées exportées) | ✓ (consommé par fixtures.html) | ✓ VERIFIED |
| 01-03 | `public/fixtures.html` | ✓ | ✓ (284 lignes) | ✓ (servi en 200, testé par fixtures.spec.ts) | ✓ VERIFIED |
| 01-03 | `ui-check/tests/fixtures.spec.ts` | ✓ | ✓ | ✓ | ✓ VERIFIED |
| 01-04 | `public/js/ui-switch.js` | ✓ | ✓ (substantiel, documenté) | ✓ (chargé par prepare.html et scene.html) | ✓ VERIFIED |
| 01-04 | `public/prepare.html` (aiguillage) | ✓ | ✓ (`localStorage` + `location.replace` présents) | ✓ | ✓ VERIFIED |
| 01-04 | `public/scene.html` (bandeau retour) | ✓ | ✓ (`ui-switch.js` chargé en fin de body) | ✓ | ✓ VERIFIED |
| 01-04 | `ui-check/tests/bascule.spec.ts` | ✓ | ✓ | ✓ | ✓ VERIFIED |
| 01-05 | `ui-check/contrat-nouvelle-partie.json` | ✓ | ✓ (8 clés typées + doc) | ✓ | ✓ VERIFIED |
| 01-05 | `ui-check/tests/lancement-partie.spec.ts` | ✓ | ✓ | ✓ | ✓ VERIFIED |
| 01-06 | `Fusion/marvel-lcg-src-fusion.zip` | ✓ | ✓ (92 Mo, contient 34 fixtures + index.js + fixtures.html + ui-switch.js + prepare.html + scene.html ; 0 entrée `ui-check`) | ✓ | ✓ VERIFIED |
| 01-06 | `.planning/STATE.md` | ✓ | ✓ (phase 1 marquée terminée 6/6) | ✓ | ✓ VERIFIED |

### Vérification des liens clés

| De | Vers | Via | Statut |
|----|------|-----|--------|
| `captures.spec.ts` | `ecrans.ts` | `import { ECRANS } from '../ecrans'` | ✓ WIRED |
| `playwright.config.ts` | `global-setup.ts` | `globalSetup: './global-setup.ts'` | ✓ WIRED |
| `captures.spec.ts` | `references/` | `toHaveScreenshot` + `snapshotPathTemplate` | ✓ WIRED (18/18 exécutés avec succès) |
| `comparer.mjs` | `references/` + `test-results/` | lecture des PNG réels | ✓ WIRED |
| `valider.mjs` | `playwright test --update-snapshots` | gate `OUI` | ✓ WIRED |
| `dump_get_world.py` | `game.world.render.descriptor` | hook autoplay | ✓ WIRED |
| `fixtures.html` | `public/js/fixtures/index.js` | import ESM dynamique | ✓ WIRED (34/34 fixtures chargées avec succès) |
| `fixtures.spec.ts` | `/fixtures.html` | navigation Playwright | ✓ WIRED |
| `prepare.html` | `/scene.html` | `location.replace` si `ui=old` | ✓ WIRED (test bascule vert) |
| `scene.html` | `js/ui-switch.js` | balise `data-role="ancienne"` | ✓ WIRED |
| `bascule.spec.ts` | `localStorage 'ui'` | vérification mémorisation | ✓ WIRED |
| `lancement-partie.spec.ts` | `/new?data=` | `page.waitForRequest` | ✓ WIRED (contrat respecté) |
| `lancement-partie.spec.ts` | `contrat-nouvelle-partie.json` | comparaison clés/types | ✓ WIRED |
| `lancement-partie.spec.ts` | `/get_world?p=0` | attente du plateau | ✓ WIRED |
| `Fusion/marvel-lcg-src-fusion.zip` | `~/marvel-work/fusion/marvel-lcg-src` | re-zip après vérification | ✓ WIRED |

### Contrainte d'intouchabilité (`public/js/marvel/`)

Recherche exhaustive de `js/marvel/` dans tous les fichiers ajoutés par la phase (`public/js/fixtures/*.js`, `public/fixtures.html`, `public/js/ui-switch.js`, `public/prepare.html`, `public/scene.html`) : **aucune occurrence**. Contrainte respectée.

### Couverture des exigences

| Exigence | Statut | Remarque |
|----------|--------|----------|
| FOUND-01 | ✓ SATISFIED | Les 3 volets (captures, fixtures, `?ui=old`) + l'extension "contrat `/new?data=`" sont tous vérifiés en direct. Note mineure : `REQUIREMENTS.md` liste encore FOUND-01 comme "Pending" (case à cocher non mise à jour) — écart cosmétique, sans impact sur le résultat de la phase. |

### Anti-patterns recherchés

Scan de tous les fichiers livrés par la phase (`ui-check/tests/*.spec.ts`, `ui-check/scripts/*.mjs`, `ui-check/ecrans.ts`, `ui-check/global-setup.ts`, `ui-check/playwright.config.ts`, `public/js/ui-switch.js`, `public/fixtures.html`, `public/js/fixtures/index.js`) pour TODO/FIXME/XXX/HACK/placeholder/"not implemented"/"coming soon" : **aucune occurrence trouvée**. Aucun blocage.

### Vérification humaine

Aucune nouvelle demande — les 3 checkpoints bloquants prévus par les plans (page de comparaison 01-02, aller-retour `?ui=old` + partie jouable 01-04, contrôle de livraison finale 01-06) ont déjà été approuvés par l'utilisateur pendant l'exécution de la phase, comme documenté dans les SUMMARY correspondants.

### Résumé des écarts

Aucun écart bloquant. Deux observations mineures, non bloquantes, à corriger en toile de fond si l'occasion se présente (pas dans le cadre de cette vérification) :
- `ROADMAP.md` mentionne encore "5 écrans" dans le texte du critère de succès n°1, alors que le harnais en couvre 6 (sur-couverture bénéfique, pas une régression).
- `REQUIREMENTS.md` liste encore FOUND-01 comme "Pending" malgré la satisfaction complète de l'exigence.

---

*Vérifié le : 2026-07-28*
*Vérificateur : Claude (gsd-verifier)*
