---
phase: 01-filet-de-securite
plan: 06
subsystem: infra
tags: [livraison, zip, autoplay, non-regression, launcher-fast, playwright, zipfile, winsound]

# Dependency graph
requires:
  - phase: 01-01
    provides: "npm run captures (18 references), boucle de dev sous launcher_fast.py"
  - phase: 01-02
    provides: "npm run captures:comparer / captures:valider, seul chemin vers references/"
  - phase: 01-03
    provides: "34 fixtures get_world + public/fixtures.html + npm run fixtures ; dossier de jeu .game"
  - phase: 01-04
    provides: "public/js/ui-switch.js, bascule ?ui=old memorisee, npm run bascule"
  - phase: 01-05
    provides: "contrat /new?data= gele, npm run lancement"
provides:
  - "Livrable Fusion/marvel-lcg-src-fusion.zip a jour : 5749 fichiers, les 3 ajouts de la phase inclus, harnais et caches exclus"
  - "Preuve de non-regression moteur apres la phase 1 : autoplay 0 traceback sur 2 couples"
  - "Passe complete du filet enchainee en une session apres relance du serveur (4 commandes, exit 0)"
  - "Recette de re-zip reproductible (structure du livrable documentee : entrees a la racine, 3 exclusions)"
  - "Validation utilisateur du filet complet : fixtures, sortie de secours, partie jouable comme avant"
affects: [02-fondations-vite, 03-pilotes-carte, 04-preparation, 05-plateau-restylage, 06-plateau-layout, 07-plateau-interactions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Rituel de livraison en 3 temps : non-regression moteur -> re-zip -> relance serveur + passe complete du filet"
    - "Re-zip par le module zipfile de Python (zip/unzip absents), structure de l'archive calquee sur la precedente"
    - "Diff de listes entre l'ancien et le nouveau zip avant remplacement : on prouve ce qu'on ajoute et ce qu'on retire"
    - "Dependance Windows manquante (winsound) fournie par PYTHONPATH, jamais en ecrivant dans le dossier du jeu"

key-files:
  created:
    - /mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src-fusion.zip.bak-avant-phase1
    - /home/arnau/marvel-work/scratch/ecartes-01-06/scene.html.bak-avant-ui
  modified:
    - /mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src-fusion.zip
    - .planning/STATE.md
    - .planning/ROADMAP.md

key-decisions:
  - "Le zip est reconstruit avec zipfile (Python) : ni zip ni unzip ne sont installes dans cet environnement"
  - "Structure du livrable preservee : entrees a la racine de l'archive, sans prefixe marvel-lcg-src/ (la commande du plan l'aurait changee)"
  - "Exclusions du livrable figees : .game/, __pycache__/, originals_pyc/ (calquees sur le zip precedent)"
  - "scene.html.bak-avant-ui deplace hors du dossier servi plutot que supprime : ecarte definitivement, jamais perdu"
  - "Dossier de jeu du bot = .game et winsound fourni par PYTHONPATH : test_autoplay.py reste bit a bit intact"
  - "statistics: false pendant les runs autoplay, launch.json restaure a l'identique ensuite"

patterns-established:
  - "Toute livraison verifie le zip par assertions nommees (3 ajouts presents, 0 entree ui-check/.game/__pycache__/originals_pyc)"
  - "Le zip precedent est sauvegarde avant remplacement (.bak-avant-<etape>), ce qui rend la livraison reversible"
  - "Les 4 commandes du filet s'enchainent en une seule session apres relance, lancement toujours en dernier"

# Metrics
duration: 24 min
completed: 2026-07-28
---

# Phase 01 Plan 06 : Livraison et vérification d'ensemble — Summary

**La phase 1 est livrée et prouvée verte de bout en bout : autoplay 0 traceback sur deux couples, livrable `Fusion/` reconstruit à 5 749 fichiers (+37 ajouts de la phase, −1 sauvegarde morte, 0 fichier du harnais), les quatre commandes du filet enchaînées en une session après relance du serveur, et l'utilisateur a constaté de ses yeux que le jeu se joue exactement comme avant.**

## Performance

- **Duration:** 24 min (dont ~14 min d'attente au checkpoint)
- **Started:** 2026-07-28T12:30:08Z
- **Completed:** 2026-07-28T12:54:50Z
- **Tasks:** 2/2 (1 automatique + 1 checkpoint validé)
- **Files modified:** 5 (1 zip regénéré, 1 zip de sauvegarde, 1 fichier déplacé hors du dossier servi, STATE.md, ROADMAP.md)

## Accomplishments

- **La phase 1 n'a rien cassé, et c'est mesuré, pas supposé.** Deux parties automatiques complètes (rhino/spider_man en 150 asks, klaw/captain_marvel en 55 asks) se terminent sur un game over avec **0 traceback**, après tous les ajouts de la phase. Les ajouts étant purement statiques dans `public/`, c'était attendu — mais le rituel de livraison du projet exige la preuve, pas l'attente.
- **Les trois artefacts de la phase qui vivaient hors du dépôt git sont désormais sauvegardés.** `public/fixtures.html`, `public/js/ui-switch.js` et les 35 modules de `public/js/fixtures/` ne existaient que dans le codebase vivant ; le re-zip est leur seule sauvegarde, et `ui-switch.js` est la sortie de secours elle-même. Ils sont dans le livrable, vérifiés nommément.
- **Le livrable a été reconstruit sans changer de forme.** L'inspection de l'ancien zip a révélé que ses entrées sont à la racine de l'archive, sans préfixe `marvel-lcg-src/` : la commande proposée par le plan aurait produit une archive de structure différente. Le diff avant/après est exact et connu : **+37 fichiers, −1, 5 712 entrées communes**.
- **Le filet fonctionne dans les conditions réelles.** `npm run captures && npm run fixtures && npm run bascule && npm run lancement` sort en 0 dans une seule session, **après** relance du serveur — donc sur le code réellement recompilé par `launcher_fast.py`, pas sur un serveur chaud depuis deux heures. Aucune des 18 images de référence n'a bougé.
- **La sortie de secours et la visionneuse ont été validées à la main.** L'utilisateur a parcouru les états enregistrés, emprunté `?ui=old`, puis lancé une vraie partie : elle se joue comme avant. C'est le critère qui autorise à toucher au plateau à partir de la phase 5.

## Task Commits

1. **Tâche 1 : Non-régression moteur et re-zip du livrable** — `51b80ec` (chore)
2. **Tâche 2 : Checkpoint de vérification humaine** — validé (pas de commit de code)

**Plan metadata:** `docs(01-06): complete delivery plan`

_Note : le zip et le codebase vivant sont hors du dépôt git. Le commit de tâche ne porte que `STATE.md`, mais il embarque l'empreinte SHA-256 du livrable et le décompte exact des ajouts/retraits, ce qui rend la livraison traçable depuis l'historique._

## Files Created/Modified

**Hors dépôt :**

- `Fusion/marvel-lcg-src-fusion.zip` — regénéré depuis `~/marvel-work/fusion/marvel-lcg-src`. 5 749 fichiers, 92,4 Mo, sha256 `c8ef207057223ccb1536c5db15e071a69e7faaff2c0d2908c29118f8803313e9`. Intégrité CRC vérifiée (`testzip`).
- `Fusion/marvel-lcg-src-fusion.zip.bak-avant-phase1` — sauvegarde du livrable précédent (5 713 fichiers, 92,2 Mo). Elle contient encore `scene.html.bak-avant-ui`, donc rien n'est perdu.
- `~/marvel-work/scratch/ecartes-01-06/scene.html.bak-avant-ui` — sauvegarde morte antérieure à la surcouche wizard, sortie du dossier `public/` servi par le serveur.
- `~/marvel-work/fusion/marvel-lcg-src/.game/launch.json` — `statistics` remis à `true` et `server_addresses` à `127.0.0.1:2345` : fichier restauré à l'identique après les runs.

**Dans le dépôt :**

- `.planning/STATE.md` — position, métriques, quatre acquis de structure de la phase, structure du livrable, pièges d'environnement (`zip`/`unzip` absents, `winsound`), continuité de session.
- `.planning/ROADMAP.md` — 01-06 cochée, phase 1 marquée terminée (6/6).

## Decisions Made

- **Le re-zip passe par `zipfile` (Python), pas par la commande `zip`.** Ni `zip` ni `unzip` ne sont installés. Plutôt qu'installer un paquet système pour une opération unique, l'archive est construite et inspectée avec la bibliothèque standard du Python du projet. Effet secondaire précieux : lire l'ancien zip par programme a permis de découvrir sa vraie structure avant de la reproduire.
- **La structure de l'archive est préservée à l'identique : entrées à la racine, sans préfixe.** La commande du plan (`zip -rq ... marvel-lcg-src`) aurait ajouté un dossier `marvel-lcg-src/` en tête de chaque entrée. Le livrable aurait changé de forme sans que personne ne l'ait demandé, et toute procédure de décompression existante en aurait souffert.
- **Les exclusions sont calquées sur le zip précédent, pas inventées** : `.game/` (dossier compilé par le lanceur, régénéré à chaque démarrage), `__pycache__/` et `originals_pyc/`. Les sauvegardes `data/*.bak-*` sont **conservées** : elles étaient déjà dans la livraison précédente, les retirer aurait été une décision hors périmètre.
- **`scene.html.bak-avant-ui` est déplacé, pas supprimé.** Le plan laissait le choix entre supprimer et exclure. Le déplacer hors du dossier servi rend l'exclusion permanente (aucun re-zip futur n'a à s'en souvenir) tout en le gardant accessible à deux endroits : `~/marvel-work/scratch/ecartes-01-06/` et le zip de sauvegarde.
- **La vérification du zip se fait par assertions nommées**, pas par un coup d'œil : 3 ajouts présents (`fixtures.html`, `ui-switch.js`, `fixtures/index.js`), 4 absences (`ui-check`, `scene.html.bak-avant-ui`, `.game/`, `__pycache__`, `originals_pyc`), plus le diff complet des listes ancien/nouveau. Un livrable se contrôle comme un test.
- **La passe du filet a été jouée deux fois** : une fois commande par commande (pour lire chaque sortie), une fois enchaînée par `&&` (la forme exacte demandée par la vérification du plan). Les deux sortent en 0.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocage] `zip` et `unzip` ne sont pas installés**

- **Found during:** Tâche 1, étape 2 (inspection de l'ancien zip)
- **Issue:** `unzip: command not found`, puis `zip` absent également. Les trois commandes de re-zip et les trois contrôles `unzip -l` du bloc de vérification étaient inexécutables tels quels.
- **Fix:** Un script `zipfile` (bibliothèque standard, Python 3.10 du projet) construit l'archive et un second l'inspecte. Aucune installation de paquet système.
- **Files modified:** aucun fichier du dépôt (scripts jetables dans `/tmp/nonreg/`)
- **Verification:** `ZipFile.testzip()` → intégrité CRC OK ; diff des listes ancien/nouveau → +37 / −1 / 5 712 communs ; les 3 ajouts relus depuis l'archive avec leur taille et la présence de la balise `ui-switch.js`.
- **Committed in:** `51b80ec` (Tâche 1)

**2. [Rule 1 - Bug de plan] La commande de re-zip aurait changé la structure du livrable**

- **Found during:** Tâche 1, étape 2 (conséquence directe de la déviation 1)
- **Issue:** Le plan demandait `zip -rq <cible> marvel-lcg-src`, qui préfixe toutes les entrées par `marvel-lcg-src/`. Or l'inspection de l'archive existante montre ses entrées **à la racine** (`src/`, `public/`, `launcher.py`…). Livrer une archive de structure différente sous le même nom aurait été une régression silencieuse du livrable.
- **Fix:** Le script écrit les chemins relatifs à `marvel-lcg-src`, sans préfixe, en `ZIP_DEFLATED` et sans entrée de répertoire — exactement la forme de l'archive précédente. La structure est désormais documentée dans STATE.md pour les livraisons suivantes.
- **Files modified:** aucun fichier du dépôt
- **Verification:** les 5 712 entrées communes ont un chemin identique dans les deux archives ; seuls les 37 ajouts et le retrait diffèrent.
- **Committed in:** `51b80ec` (Tâche 1)

**3. [Rule 3 - Blocage] `test_autoplay.py` ne démarre pas sur le dossier indiqué par le plan**

- **Found during:** Tâche 1, étape 1 (préparation du run de non-régression)
- **Issue:** Deux obstacles cumulés, déjà rencontrés en 01-03 pour le dumper. (a) `marvel-lcg-src` n'expose pas les modules du moteur : le dossier importable est `marvel-lcg-src/.game`, celui que compile `launcher_fast.py` et que sert réellement le serveur. (b) `.game` n'embarque pas `winsound` (module Windows) : le lanceur l'injecte lui-même en mémoire, `test_autoplay.py` non.
- **Fix:** Dossier de jeu = `.game`. `winsound` fourni par `PYTHONPATH` pointant sur une copie de `~/marvel-work/boot/winsound.py` déposée dans `/tmp` — **aucune écriture dans le dossier du jeu**, et `test_autoplay.py` reste bit à bit intact (md5 `59fe6f37d7bef387b6175c8688f5cdad`, identique à celui relevé en 01-03). En complément, `statistics` a été mis à `false` le temps des runs pour ne pas concurrencer le serveur en cours sur `statistics.json`, puis `launch.json` a été restauré à l'identique.
- **Files modified:** aucun fichier du dépôt ni du jeu (script jetable dans `/tmp/nonreg/`)
- **Verification:** `exit=0` et `grep -c Traceback` = 0 sur les deux logs ; `[BOT] GameLoop terminé (game over)` dans les deux ; `launch.json` relu après restauration (`['127.0.0.1:2345']`, `statistics: True`).
- **Committed in:** `51b80ec` (Tâche 1)

---

**Total deviations:** 3 auto-corrigées (2 blocages d'environnement, 1 bug de plan)
**Impact on plan:** Aucune dérive de périmètre. Les trois déviations portent sur *comment* exécuter le rituel, jamais sur *quoi* livrer. La deuxième est la plus utile à retenir : sans elle, le livrable aurait silencieusement changé de forme.

## Issues Encountered

- **`fixtures.html` a d'abord été pris pour un écran de jeu.** Au checkpoint, l'utilisateur a cru que la page servait à lancer une partie ; il a fallu préciser que c'est une **visionneuse en lecture seule** d'états enregistrés. La confusion levée, la vérification s'est déroulée normalement. **Signal UX à garder** : quand cette page accueillera le composant React du plateau (phase 5), son rôle doit être annoncé dans la page elle-même — un titre et une phrase du type « visionneuse d'états enregistrés, aucune partie n'est en cours ». Le rendu texte actuel ne dit pas ce qu'il est.
- **La relance du serveur coupe la partie en cours**, comme prévu et annoncé. Elle est indispensable ici : la passe du filet doit tourner sur le code recompilé, pas sur un serveur démarré avant les ajouts de la phase.
- **Le port 2345 s'est libéré dès la première sonde** cette fois-ci (le piège TIME_WAIT documenté en 01-01 n'a pas mordu), mais l'attente active a été conservée dans le script de relance : le piège est intermittent, pas résolu.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**La phase 1 est complète et validée. Le projet peut entrer en phase 2.**

Ce qui est acquis et disponible pour toute la suite :

- **Détection de régression visuelle** : `npm run captures` (18 références, 6 écrans × 3 gabarits), avec `captures:comparer` / `captures:valider` comme seul chemin vers `references/`.
- **Travail hors partie** : 34 états `get_world` réels et `fixtures.html` — le plateau se travaille sans jouer, et le contrat « une fixture importée → un rendu » est prouvé bit à bit.
- **Réversibilité** : `?ui=old` mémorisée dans `localStorage`, démontrée sur le couple `prepare.html` ↔ `scene.html`, avec la recette de câblage écrite pour toute page migrée ensuite.
- **Non-régression fonctionnelle** : contrat `/new?data=` gelé (8 clés typées) et `npm run lancement` qui prouve l'arrivée au plateau.
- **Livraison** : le rituel est rodé et documenté (non-régression → re-zip → relance → passe du filet), et la structure du livrable est écrite dans STATE.md.

**Points de vigilance à transmettre à la phase 2 :**

- **Séquence CSS obligatoire** : captures de référence → purge des `!important` de `wizard.css` (67 sur 165) → `@layer` → tokens. Inverser aggrave la cascade.
- **Routage serveur par extension en liste blanche stricte** : tout asset de build hors liste échoue silencieusement (200 OK, contenu vide). C'est le premier écueil concret d'un build Vite servi par le serveur Python.
- **Toute montée de version de Playwright exige une re-validation des 18 références** (le Chromium embarqué change le rendu). Version épinglée `1.62.0` sans `^`.
- **Le codebase vivant n'est pas versionné** : chaque étape livrée doit repasser par le re-zip, sinon les fichiers ajoutés dans `public/` n'ont aucune sauvegarde.
- **Signal UX de la visionneuse** (voir Issues) : à traiter quand `fixtures.html` accueillera le composant React.

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*
