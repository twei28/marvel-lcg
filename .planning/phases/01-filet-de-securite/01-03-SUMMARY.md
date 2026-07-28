---
phase: 01-filet-de-securite
plan: 03
subsystem: testing
tags: [fixtures, get_world, autoplay, playwright, esm, descripteur, plateau]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Harnais ui-check (Playwright 1.62.0, script npm `fixtures` déjà déclaré), serveur sous launcher_fast.py, contrainte d'intouchabilité de public/js/marvel/"
provides:
  - "34 états de jeu complets issus de vraies parties, sous forme de modules ESM (public/js/fixtures/)"
  - "dump_get_world.py : copie instrumentée de test_autoplay.py, dump par prédicat, mode --controle"
  - "Preuve mesurée : le descripteur lu pendant un ask est bit à bit celui que /get_world renvoie"
  - "public/fixtures.html : affichage d'un plateau complet sans lancer de partie"
  - "npm run fixtures : les 34 états rejoués et vérifiés automatiquement"
affects: [01-04-bascule-ui-old, 02-fondations-vite, 05-plateau-restylage, 06-plateau-layout, 07-plateau-interactions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Le nouveau code est une fonction pure de get_world : une fixture importée -> un rendu, zéro appel au runtime existant"
    - "Fixtures stockées en .js (export default) et non .json : .json n'est pas dans la liste blanche de routage du serveur"
    - "Sélection par prédicat sur le descripteur, un dump par cas et par partie, anti-doublon par empreinte de contenu"
    - "Le catalogue est exposé par la page (window.FIXTURES) : le test n'a pas à connaître l'emplacement du jeu sur le disque"

key-files:
  created:
    - /home/arnau/marvel-work/tools/dump_get_world.py
    - /home/arnau/marvel-work/tools/run_dump.sh
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/fixtures/ (34 modules + index.js)
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/fixtures.html
    - ui-check/tests/fixtures.spec.ts
  modified: []

key-decisions:
  - "Dossier de jeu du bot = .game (dossier compilé par launcher_fast.py) et non marvel-lcg-src : c'est le seul dossier importable, et il porte exactement le code servi par le serveur"
  - "Stub winsound injecté en mémoire par le dumper au lieu d'écrire un fichier dans le dossier du jeu"
  - "Fin de partie : le dumper rejoue World.OnGameOver après GameLoop, étape que test_autoplay.py ne fait pas"
  - "Doublons exacts supprimés (34 fixtures et non 40) : la diversité prime sur la répétition"
  - "Les decks volumineux sont rendus repliés (<details>) mais restent dans le DOM : lisible ET comptable par le test"

patterns-established:
  - "Contrôle de fraîcheur avant toute génération de masse : prouver l'équivalence mémoire/HTTP, puis produire"
  - "Un port TCP distinct par run d'autoplay, avec attente active de libération (run_dump.sh)"

# Metrics
duration: 14 min
completed: 2026-07-28
---

# Phase 01 Plan 03 : Fixtures get_world — Summary

**34 états de jeu complets, extraits de 5 vraies parties automatiques sur 4 scénarios, rejouables dans le navigateur via `/fixtures.html` sans qu'aucune partie ne tourne — et la preuve mesurée que ces états sont bit à bit ce que `/get_world` renvoie.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-07-28T10:54:52Z
- **Completed:** 2026-07-28T11:09:30Z
- **Tasks:** 3/3
- **Files modified:** 39 (1 outil + 1 script de lancement + 34 fixtures + 1 catalogue + 1 page + 1 test)

## Accomplishments

- **La question ouverte n°1 de la recherche est tranchée par la mesure.** Le mode `--controle` sérialise `game.world.render.descriptor` pendant un ask, interroge dans le même processus `GET /get_world?p=0`, décompresse le gzip et compare les deux JSON : `CONTROLE OK render_id=30 (phase='Resolve Mulligans', 36138 octets comparés)`. Tout le travail des phases 5 à 7 repose sur cette équivalence : elle n'est plus une hypothèse.
- **34 états couvrent 4 scénarios (rhino, klaw, god_of_lies, absorbing_man), 5 héros et 10 moments de jeu distincts** : mise en place, début de partie, main la plus remplie, sbire en jeu, complot annexe, cartes de statut, cartes mises de côté, défausse de rencontre chargée, vilain au stade 2, fin de partie. Tous les cas exigés par le plan sont présents.
- **`/fixtures.html` affiche un plateau complet (83 à 106 cartes selon l'état) sans qu'aucune partie ne tourne** : vilain et sbires avec PV/ATQ/COMP, complot principal avec sa menace (5/7), statuts attachés, ennemis engagés, identité, alliés, améliorations, main, decks repliés, et le dernier message de la partie. Zéro dépendance, zéro ligne de `public/js/marvel/`.
- **`test_autoplay.py` est bit à bit intact** (md5 `59fe6f37d7bef387b6175c8688f5cdad` avant et après) et les 5 parties se terminent avec **0 traceback**, y compris sur les logs des campagnes précédentes.
- **`npm run fixtures` passe en 20 s** et refuse toute erreur console : le catalogue est désormais sous filet de sécurité, comme les 18 captures d'écran.

## Task Commits

1. **Tâche 1 : Contrôle de fraîcheur et dumper** — pas de commit de code : `dump_get_world.py` et `run_dump.sh` vivent dans `~/marvel-work/tools/`, hors du dépôt.
2. **Tâche 2 : Génération des 34 fixtures** — pas de commit de code : les fixtures vivent dans `~/marvel-work/fusion/marvel-lcg-src/public/js/fixtures/`, hors du dépôt.
3. **Tâche 3 : Page de relecture et test automatisé** — `bbeca1c` (test) pour `ui-check/tests/fixtures.spec.ts` ; `public/fixtures.html` est hors du dépôt.

**Note :** ce plan produit l'essentiel de ses livrables dans le codebase vivant (`~/marvel-work/`), qui n'est pas versionné ici. Le seul fichier du dépôt est le test Playwright. La procédure de régénération complète tient en une commande, documentée en tête de `index.js`.

## Files Created/Modified

Hors dépôt (codebase vivant `~/marvel-work/`) :

- `tools/dump_get_world.py` — copie de `test_autoplay.py` + bloc de dump (~130 lignes ajoutées) : prédicats, maxima du run, anti-doublon, mode `--controle`, stub winsound, présentation de la fin de partie
- `tools/run_dump.sh` — lance un run en attendant la libération effective du port TCP
- `fusion/marvel-lcg-src/public/js/fixtures/*.js` — 34 modules `export default {...}` (1,9 Mo), en-tête « Généré par dump_get_world.py — ne pas éditer à la main »
- `fusion/marvel-lcg-src/public/js/fixtures/index.js` — catalogue en français : fichier, titre, description, scénario, héros, cas
- `fusion/marvel-lcg-src/public/fixtures.html` — 285 lignes, page autonome (HTML + CSS + module ESM inline), rendu texte structuré par zone

Dans le dépôt :

- `ui-check/tests/fixtures.spec.ts` — ouvre les 34 états un par un, vérifie ≥ 10 cartes affichées, la cohérence du compteur, et l'absence d'erreur console

## Decisions Made

- **Le dossier de jeu passé au bot est `.game`, pas `marvel-lcg-src`.** Le plan proposait `marvel-lcg-src`, qui ne contient pas de modules importables (`src/` n'est pas sur le `sys.path` du moteur). `.game` est le dossier compilé par `launcher_fast.py` : c'est exactement le code que sert le serveur sur 2345, et ses `data/`, `deck/`, `public/` sont des liens vers les dossiers vivants. Les fixtures reflètent donc le contenu réellement servi, pas une copie datée (les `boot_sub*` historiques ont des données du 26/07).
- **Le stub `winsound` est injecté en mémoire par le dumper.** Les dossiers `boot_sub*` embarquent un fichier `winsound.py` ; `.game` non (le lanceur l'injecte lui-même). Plutôt qu'écrire un fichier dans le dossier du jeu, le dumper reproduit l'injection du lanceur.
- **Le dumper écrit `statistics: false` dans le `launch.json` qu'il modifie**, pour ne pas concurrencer le serveur en cours sur le fichier de statistiques. Le fichier a été restauré à l'identique en fin de plan, et `launcher_fast.py` le recopie de toute façon à chaque démarrage.
- **Format `.js` et non `.json`** (confirmé par mesure) : la liste blanche de routage du serveur ne connaît pas `.json`, qui tombe dans le fourre-tout et renvoie une image JPEG avec un code 200.
- **Les decks (rencontre, joueur, défausses) sont rendus dans un `<details>` replié.** Ils restent dans le DOM — donc comptés et vérifiables — sans noyer la lecture : un état contient 80 à 110 cartes dont 60 dans les pioches.
- **La page expose `window.FIXTURES`.** Le test Playwright tourne sous Node Windows et ne peut pas lire les chemins WSL ; il lit donc le catalogue depuis la page elle-même. Effet de bord utile : le test ne connaît pas l'emplacement du jeu sur le disque.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocage] Dossier de jeu et stub `winsound`**

- **Found during:** Tâche 1 (premier lancement du contrôle)
- **Issue:** La commande du plan (`$PY $D $GAME 8801 ...` avec `$GAME=marvel-lcg-src`) échoue : `ModuleNotFoundError: No module named 'winsound'`, et `marvel-lcg-src` n'expose pas les modules du moteur.
- **Fix:** Dossier de jeu = `marvel-lcg-src/.game` ; stub `winsound` injecté dans `sys.modules` par le dumper, comme le fait `launcher_fast.py`.
- **Files modified:** `tools/dump_get_world.py`
- **Verification:** `CONTROLE OK` puis 5 parties complètes, 0 traceback
- **Committed in:** hors dépôt (voir note ci-dessus)

**2. [Rule 3 - Blocage] Port en TIME_WAIT entre deux runs**

- **Found during:** Tâche 2 (premier run complet, juste après le contrôle sur le même port)
- **Issue:** `AssertionError: ip='127.0.0.1', port=8801` — `IsPortAvailable` fait un `bind()` sans `SO_REUSEADDR` ; le port reste inutilisable quelques dizaines de secondes. Piège déjà rencontré en 01-01 sur le port 2345.
- **Fix:** `tools/run_dump.sh` sonde le port toutes les 3 s (60 tentatives) avant de lancer, et chaque run utilise un port distinct.
- **Files modified:** `tools/run_dump.sh` (nouveau)
- **Verification:** 6 lancements successifs sans échec de bind
- **Committed in:** hors dépôt

**3. [Rule 1 - Bug] Le prédicat `mise-en-place` ne se déclenchait jamais**

- **Found during:** Tâche 1 (premier run complet)
- **Issue:** Le prédicat de la recherche est `phase == 'Scenario Setup'`. Or la mise en place ne pose **aucune** question au joueur : le premier ask arrive en phase `Resolve Mulligans`. Le cas le plus important du lot n'était jamais capturé.
- **Fix:** `mise-en-place` = premier ask du run (ou phase `Scenario Setup` si elle se présente), placé en tête de la table de priorité.
- **Files modified:** `tools/dump_get_world.py`
- **Verification:** `mise-en-place` présent pour les 5 couples ; l'état montre bien les 6 cartes en main avant le premier tour
- **Committed in:** hors dépôt

**4. [Rule 1 - Bug] Le prédicat `fin-de-partie` ne se déclenchait jamais non plus**

- **Found during:** Tâche 1 (même run)
- **Issue:** Deux causes cumulées : (a) la fin de partie n'est suivie d'aucun ask, donc un hook posé dans `auto_input` ne la voit pas ; (b) le texte `--- Game Over ---` est présenté par `Game.SetGameOverInternal` → `World.OnGameOver`, étape que `test_autoplay.py` n'exécute pas puisqu'il appelle `GameSetup`/`GameLoop` directement. Le dernier état capturé était « le complot est achevé », sans message de fin.
- **Fix:** Le dumper rejoue `World.OnGameOver(world.game_over)` après `GameLoop` (sous `try/except`, uniquement si la partie est réellement finie et pas quittée), puis tente un dernier dump depuis `finish()`.
- **Files modified:** `tools/dump_get_world.py`
- **Verification:** `prompt_last_text='\n--- Game Over ---\nThe Main Scheme was Completed (The Break-In!)\nFalse'` ; `fin-de-partie` présent pour les 5 couples
- **Committed in:** hors dépôt

**5. [Rule 1 - Bug] 6 fixtures étaient des doublons exacts**

- **Found during:** Tâche 2 (contrôle d'unicité par md5 après génération)
- **Issue:** Les cas « maximum du run » tombaient souvent sur un état déjà enregistré : la main est la plus remplie au tout premier ask (donc identique à `mise-en-place`), et la défausse de rencontre est la plus fournie au dernier (identique à `fin-de-partie`). 40 fichiers pour 34 états réels.
- **Fix:** Garde anti-doublon par empreinte du contenu dans le dumper (message `[FIXTURE] x ignoré (identique à y)`), et suppression des 6 doublons déjà écrits.
- **Files modified:** `tools/dump_get_world.py`, dossier `public/js/fixtures/`
- **Verification:** 34 fichiers, 34 empreintes distinctes
- **Committed in:** hors dépôt

**6. [Rule 3 - Blocage] `test.skip(({}, testInfo) => ...)` au niveau du fichier**

- **Found during:** Tâche 3 (premier `npm run fixtures`)
- **Issue:** La forme proposée par le plan lève `TypeError: Cannot read properties of undefined (reading 'project')` sur les 3 gabarits : au niveau du fichier, le callback de `test.skip` ne reçoit pas `testInfo` dans Playwright 1.62.
- **Fix:** Filtre par projet déplacé dans un `test.beforeEach(({}, testInfo) => test.skip(...))`.
- **Files modified:** `ui-check/tests/fixtures.spec.ts`
- **Verification:** 1 test passé (pc), 2 ignorés (tablette, mobile)
- **Committed in:** `bbeca1c`

---

**Total deviations:** 6 auto-corrigées (3 blocages, 3 bugs)
**Impact on plan:** Aucune dérive de périmètre. Les deux bugs de prédicat (3 et 4) touchaient précisément les deux cas que le plan exigeait nommément — sans correction, le lot aurait été livré avec un trou au milieu.

## Issues Encountered

- **Les cas `zone-victoire`, `deck-rencontre-vide` et `stade-3` ne sont pas dans le lot.** Les 5 parties se sont toutes soldées par une défaite des joueurs (le bot joue correctement mais pas bien), donc aucune zone de victoire ni troisième stade. Ce ne sont pas des cas exigés par le plan. Le dumper sait les capturer : il suffira de relancer sur d'autres couples le jour où le plateau aura besoin de ces états.
- **Node est le binaire Windows** (`node -> /mnt/c/Program Files/nodejs/node.exe`) : il ne sait pas ouvrir un chemin WSL. Le contrôle d'import ESM des 34 fixtures s'est fait via le chemin UNC `file://wsl.localhost/Ubuntu/...` (34 imports, 0 échec), et le test Playwright lit le catalogue depuis la page plutôt que depuis le disque.
- **Le serveur n'a pas été redémarré**, conformément à la contrainte : les fixtures et `fixtures.html` sont servis à chaud (`200 application/javascript` et `200 text/html` vérifiés). Aucune partie en cours n'a été interrompue.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**Prêt pour 01-04-PLAN.md** (bascule `?ui=old`) : rien de ce plan ne le bloque, et le précédent « nouveau fichier dans `public/` servi à chaud » est confirmé une deuxième fois.

**Ce que ce plan débloque pour les phases 5 à 7 :**

- Le contrat est posé et prouvé : *une fixture importée → un rendu*. `fixtures.html` monte aujourd'hui un rendu texte ; à partir de la phase 5, la même page montera le composant React à sa place, sans changer le contrat d'entrée.
- Les noms de champs réellement utiles pour le plateau sont identifiés dans les états : `info.health` (PV restants), `info.attack` / `info.scheme` / `info.recover`, `info.k_threat` et `info.target_threat` (menace posée / seuil), `info.printed_stage`, `is_ready` (prêt/épuisé), `is_face_up`, `bind_object_id` (attachement), `card_type` (`EncounterVillain`, `Minion`, `StatusCard`, `AlterEgo`, `Upgrade`, `Ally`, `Support`, `MainScheme`…), et les jetons préfixés `k_`.

**Points de vigilance à transmettre :**

- **Ne jamais éditer une fixture à la main** : elles sont générées, l'en-tête le dit. Toute correction passe par `run_dump.sh` puis mise à jour du catalogue.
- `index.js` est tenu à la main : une régénération qui change les cas produits exige de le remettre à jour (le test échoue sinon, ce qui est le comportement voulu).
- Le dumper dépend de deux détails internes du moteur : le hook `DeviceManager.DoGetInput` et l'appel `World.OnGameOver`. Une évolution du moteur les casserait — mais le moteur est intouchable, donc le risque est théorique.
- Régénérer les fixtures avec un serveur de jeu arrêté est possible (le bot lance son propre serveur sur son port), mais la vérification `curl` du type MIME exige que le serveur 2345 tourne.

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*
