---
phase: 01-filet-de-securite
plan: 04
subsystem: ui
tags: [localstorage, bascule-ui, etranglement, playwright, non-regression-visuelle, francais, ux-non-technique]

# Dependency graph
requires:
  - phase: 01-01
    provides: "18 references figees, ecran preparation-nouvelle deja surveille, script npm bascule deja declare"
  - phase: 01-02
    provides: "npm run captures:comparer et captures:valider : seul chemin autorise vers references/"
provides:
  - "`public/js/ui-switch.js` : script partage de bascule nouvelle/ancienne version, pilote par data-attributs"
  - "Aiguillage inline en tete de `prepare.html` : `?ui=old` / `?ui=new`, sans clignotement"
  - "Bandeau de retour sur `scene.html`, affiche uniquement si la preference vaut 'old'"
  - "`npm run bascule` : 4 comportements prouves (sans preference, entree ?ui=old, memorisation, retour durable)"
  - "Convention `public/legacy/<page>.html` documentee pour les pages dont la nouvelle version reprendra le nom de l'ancienne"
affects: [01-05-contrat-new, 01-06-livraison, 02-fondations-vite, 03-pilotes-carte, 04-preparation, 05-plateau-restylage, 06-plateau-layout, 07-plateau-interactions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Bascule 100 % cote client : le serveur ignore les query strings sur les .html, zero modification backend"
    - "Preference d'interface dans localStorage cle 'ui' ('old'/'new'), jamais dans un cookie ni dans l'adresse"
    - "Aiguillage inline synchrone en tete de <head> de la NOUVELLE page : la redirection precede tout affichage"
    - "Script generique configure par data-attributs sur sa propre balise : une seule ligne a ajouter par page migree"
    - "L'ancienne page reste STRICTEMENT identique tant que la preference n'est pas posee (ses references ne bougent pas)"

key-files:
  created:
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/ui-switch.js
    - ui-check/tests/bascule.spec.ts
  modified:
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/prepare.html
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/scene.html
    - ui-check/package.json
    - ui-check/references/preparation-nouvelle/{pc,tablette,mobile}.png

key-decisions:
  - "localStorage et non query string : le parametre est perdu au lancement d'une partie (launcher.js fait location.href = '/?hot_seat')"
  - "localStorage et non cookie : le serveur pose deja session_token et app_version, on ne s'en approche pas"
  - "Aiguillage inline et non dans ui-switch.js : un fichier externe s'attend, la nouvelle UI clignoterait avant de basculer"
  - "Bandeau et lien poses EN TETE DU FLUX : mesure faite, toute position flottante recouvre un bouton dans au moins un gabarit"
  - "npm run bascule limite au gabarit pc : on verifie une navigation, pas une apparence"
  - "Contexte navigateur cree depuis .auth/state.json : cookie de version present, stockage local vide"

patterns-established:
  - "Un ecran migre = une balise ui-switch.js en fin de body + (sur la nouvelle page) l'aiguillage inline en tete de head"
  - "Quand la nouvelle version reprend le nom de l'ancienne : copie VERBATIM dans public/legacy/<page>.html, jamais retouchee ensuite"
  - "Un changement visuel voulu passe par captures -> captures:comparer -> captures:valider, et on verifie ensuite que SEUL l'ecran attendu a bouge"

# Metrics
duration: 41 min
completed: 2026-07-28
---

# Phase 01 Plan 04 : Bascule vers l'ancienne version — Summary

**Sur l'écran de préparation, `?ui=old` bascule sur l'ancienne version sans clignotement, le choix est retenu dans `localStorage` (il survit donc au lancement d'une partie, qui perd l'adresse), et le retour se fait d'un clic depuis un bandeau en français — le tout sans une ligne de code serveur et sans qu'aucune des 17 autres images de référence ne bouge.**

## Performance

- **Duration:** 41 min (dont ~12 min d'attente au checkpoint)
- **Started:** 2026-07-28T13:24:00Z
- **Completed:** 2026-07-28T14:05:00Z
- **Tasks:** 3/3 (2 automatiques + 1 checkpoint validé sans réserve)
- **Files modified:** 8 (2 créés, 6 modifiés dont 3 PNG de référence)

## Accomplishments

- **La refonte est désormais réversible d'un clic, et c'est prouvé, pas supposé.** Le couple `prepare.html` ↔ `scene.html` sert de précédent à toutes les pages migrées ensuite : une balise `<script>` en fin de `<body>`, plus l'aiguillage inline en tête de `<head>` sur la nouvelle page. C'est le mécanisme qui autorise à toucher au plateau en phases 5 à 7.
- **Le point qui comptait vraiment est couvert** : le choix survit à une navigation. `launcher.js` fait `window.location.href = "/?hot_seat"` au lancement d'une partie, ce qui efface toute query string. Une bascule par paramètre d'adresse seul aurait relâché l'utilisateur sur la nouvelle version dès sa première partie. Le test 3 de `npm run bascule` rejoue exactement ce scénario.
- **L'ancienne page ne bouge pas d'un pixel tant que personne n'a rien demandé.** Les 15 captures des 5 autres écrans (dont `scene.html` dans les 3 gabarits) sont restées vertes après l'ajout de la balise : c'est la preuve mesurée que le bandeau ne s'affiche que sur préférence explicite.
- **Le premier usage réel de la boucle de validation s'est déroulé comme prévu** : `npm run captures` rouge sur le seul écran attendu → `captures:comparer` → `captures:valider` avec `OUI` → 18/18 verts, et `git status references/` ne montre que les 3 images de `preparation-nouvelle`.
- **Zéro modification backend, zéro contact avec `public/js/marvel/`.** Mesuré au plan de recherche : le serveur ignore les query strings sur les `.html`, la bascule est donc 100 % côté client.
- **La sortie de secours mène à une partie jouable**, vérifié à la main par l'utilisateur au checkpoint (lancement depuis l'ancienne version → arrivée au plateau → la partie se joue).

## Task Commits

1. **Tâche 1 : Le script partagé de bascule** — `066b050` (feat)
2. **Tâche 2 : Câbler prepare.html et scene.html, puis prouver l'absence de régression visuelle** — `fac8ed5` (test)
3. **Tâche 3 : Checkpoint de vérification humaine** — validé sans réserve (pas de commit)

## Files Created/Modified

**Dans le codebase vivant** (`/home/arnau/marvel-work/fusion/marvel-lcg-src`, hors dépôt git) :

- `public/js/ui-switch.js` (198 lignes, créé) — script classique, configuré par `data-role` / `data-ancienne` / `data-nouvelle` sur sa propre balise. En-tête commenté : où est rangé le choix et pourquoi, la convention `public/legacy/<page>.html`, et la règle absolue « sans préférence, on ne change rien ». Tous les accès à `localStorage` sont sous `try/catch` (navigation privée). Les styles ne sont injectés que si quelque chose s'affiche.
- `public/prepare.html` — aiguillage inline placé avant toute feuille de style et tout autre script (lecture de `?ui=`, écriture de la préférence, `location.replace('/scene.html' + location.hash)`), plus la balise `ui-switch.js` `data-role="nouvelle"` en fin de `<body>`.
- `public/scene.html` — **une seule ligne ajoutée** (2251 → 2252), la balise `ui-switch.js` `data-role="ancienne"`.

**Dans le dépôt** :

- `ui-check/tests/bascule.spec.ts` (129 lignes, créé) — 4 vérifications. La première dans un navigateur neuf ; les trois suivantes dans un `describe.serial` partageant un même contexte, parce que la mémorisation n'a aucun sens dans trois navigateurs neufs. Les contextes sont créés depuis `.auth/state.json` (cookie de version présent, stockage local vide).
- `ui-check/package.json` — `bascule` limité à `--project=pc`.
- `ui-check/references/preparation-nouvelle/{pc,tablette,mobile}.png` — revalidées par la boucle avant/après.

## Decisions Made

- **La préférence vit dans `localStorage`, pas dans l'adresse.** Mesuré : `js/prepare/launcher.js` fait `window.location.href = "/?hot_seat"` au lancement d'une partie, ce qui perd toute query string. Un utilisateur qui aurait demandé l'ancienne version serait revenu sur la nouvelle dès sa première partie terminée.
- **`localStorage` et pas un cookie.** Le serveur pose déjà `session_token` et `app_version` ; ajouter un cookie côté client, c'est risquer d'interférer avec un mécanisme qu'on s'interdit de toucher.
- **L'aiguillage est inline dans `prepare.html`, pas dans `ui-switch.js`.** Un fichier externe, même en tête de `<head>`, doit être téléchargé : la nouvelle préparation aurait eu le temps de s'afficher avant de basculer. Le bloc inline est de 12 lignes, ASCII, et il est le premier script de la page.
- **Le bandeau et le lien sont posés en tête du flux du document, pas en position flottante.** Décision prise après mesure (voir déviations) : c'est la seule position qui ne recouvre aucun bouton dans les 3 gabarits. Effet secondaire heureux : « la bascule est toujours en haut de la page » se retient sans mode d'emploi, et le même repère vaudra pour toutes les pages migrées.
- **Le bandeau pousse le contenu au lieu de flotter par-dessus.** `scene.html` a déjà une barre d'étapes en `position: sticky; top: 0`. Un bandeau `sticky` au même endroit aurait obligé à décaler cette barre, donc à modifier la mise en page de l'ancienne version — exactement ce qu'on s'interdit.
- **`npm run bascule` ne tourne que sur le gabarit `pc`** (`--project=pc`). Ce test vérifie une mécanique de navigation, pas une apparence ; l'apparence est le métier de `npm run captures`. 4 tests au lieu de 12, pour la même information.
- **Le lien de la nouvelle version est un vrai `<a href>`** (avec `preventDefault` sur le clic) et non un `<button>` : il reste sélectionnable au clavier et son adresse de destination est visible au survol.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Le lien « Revenir à l'ancienne version » recouvrait les étapes 5 et 6 de l'assistant**

- **Found during:** Tâche 2 (contrôle visuel avant de lancer `npm run captures`)
- **Issue:** Le plan demandait « un lien discret en bas de page ». Première implémentation : flottant (`position: fixed`) en haut à droite. Captures prises dans les 3 gabarits : le lien passait **par-dessus les boutons d'étape 5 (Difficulté) et 6 (Récap)** de la barre de progression, en 1920, en 1180 et en 390. En bas, il tombait sur la barre de boutons fixe (`.nav` : « Retour », « Aléatoire », « Continuer »/« Lancer la partie »), y compris au téléphone où les trois boutons occupent toute la largeur. Un lien de secours qui masque des commandes du jeu est un bug, pas un détail.
- **Fix:** Le lien est placé dans une fine bande en tête du flux du document, alignée à droite, insérée avant le premier enfant de `<body>` — comme le bandeau de l'ancienne version. Elle ne recouvre rien.
- **Files modified:** `public/js/ui-switch.js`
- **Verification:** Captures des 3 gabarits relues après correction : les 6 étapes sont de nouveau visibles, aucune commande masquée. Le motif de la décision est commenté dans le code pour éviter qu'on « corrige » l'emplacement plus tard.
- **Committed in:** `fac8ed5` (Tâche 2)
- **Validé par l'utilisateur au checkpoint**, tel quel.

**2. [Rule 1 - Bug, cosmétique] La nouvelle préparation peut désormais défiler de ~45 px**

- **Found during:** Tâche 2 (mesure de l'effet de la bande sur la mise en page)
- **Issue:** `#app` de `prepare.html` porte `min-height: 100vh`. Ajouter 33 px de bande en tête du flux rend le document plus haut que la fenêtre : `scrollHeight` mesuré à 1125 px pour 1080 px de fenêtre. La page tenait pile dans l'écran, elle défile maintenant très légèrement.
- **Fix:** Aucun. Corriger demanderait de faire connaître la hauteur de la bande à la feuille de style de la page, donc de coupler un script générique à une page précise — le remède serait pire que le mal, et la nouvelle préparation sera refaite en phase 4. Le compromis a été présenté à l'utilisateur au checkpoint.
- **Files modified:** aucun
- **Verification:** Mesure `scrollHeight` / `clientHeight` avant et après ; les 3 références de `preparation-nouvelle` intègrent la bande et sont figées.
- **Committed in:** `fac8ed5` (Tâche 2), documenté dans le message de commit
- **Accepté par l'utilisateur au checkpoint**, sans réserve.

**3. [Rule 3 - Blocage] `npm run bascule` tournait sur les 3 gabarits**

- **Found during:** Tâche 2
- **Issue:** Le script déclaré au plan 01-01 était `playwright test tests/bascule.spec.ts`, sans projet : 12 tests là où le plan en attendait 4, et 3 fois la même vérification de navigation.
- **Fix:** `--project=pc` ajouté au script (commande unique, compatible `cmd.exe`).
- **Files modified:** `ui-check/package.json`
- **Verification:** `npm run bascule` → « 4 passed », exit 0.
- **Committed in:** `fac8ed5` (Tâche 2)

**4. [Rule 3 - Blocage] Commit de tâche sans contenu pour la tâche 1**

- **Found during:** Tâche 1
- **Issue:** `ui-switch.js` vit dans le codebase du jeu, qui n'est pas suivi par git (le dépôt ne contient que `.planning/` et `ui-check/`). La tâche 1 ne produisait donc aucun fichier committable, ce qui aurait cassé la règle « un commit par tâche ».
- **Fix:** Commit `--allow-empty` décrivant l'artefact, son chemin, son nombre de lignes et l'empreinte SHA-256 de son contenu, avec la raison explicite du commit vide. Le plan 01-03 avait rencontré la même situation pour les fixtures et n'avait rien tracé.
- **Files modified:** aucun
- **Verification:** `git log --oneline` : `066b050` daté et documenté.
- **Committed in:** `066b050` (Tâche 1)

---

**Total deviations:** 4 auto-corrigées (2 bugs, 2 blocages)
**Impact on plan:** Aucune dérive de périmètre. La seule déviation visible pour l'utilisateur (l'emplacement du lien) lui a été présentée au checkpoint avec la mesure qui la justifie, et il l'a acceptée telle quelle.

## Issues Encountered

- **`npm run captures:valider` reste inutilisable en pipe.** Confirmation du point hérité de 01-02 : sous `cmd.exe`, une entrée redirigée n'atteint pas le script, qui annule (comportement sûr). La validation de cette tâche est donc passée par `printf 'OUI\n' | node scripts/valider.mjs`, appel direct documenté par 01-02. En usage réel, l'utilisateur tape au clavier et la commande npm fonctionne normalement.
- **`node --check` ne lit pas un chemin WSL.** Node étant le binaire Windows, la vérification de syntaxe de `public/js/ui-switch.js` demande la forme UNC `//wsl.localhost/Ubuntu/home/arnau/...`. À retenir pour tout contrôle statique sur un fichier du jeu.
- **Un fichier `public/scene.html.bak-avant-ui` traîne dans le codebase** (sauvegarde antérieure à la surcouche wizard, ~180 lignes de moins). Il n'a pas été touché. À signaler avant le re-zip du plan 01-06 : il n'a rien à faire dans une livraison.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**Prêt pour 01-05-PLAN.md** (contrat `/new?data=` gelé et arrivée au plateau vérifiée automatiquement) :

- Le va-et-vient entre les deux préparations est prouvé et validé à la main, y compris le lancement d'une partie depuis l'ancienne version.
- Le script `lancement` est déjà déclaré dans `ui-check/package.json` ; il ne reste qu'à écrire `tests/lancement-partie.spec.ts`. Penser à le limiter à `--project=pc` comme `bascule` s'il ne vérifie pas d'apparence.
- Le bouton « Préparer une partie » du menu principal pointe sur `prepare.html` : il respecte donc la préférence mémorisée. Le second bouton du menu pointe directement sur `scene`, sans passer par l'aiguillage — c'est voulu, il reste un accès direct à l'ancienne version.

**Points de vigilance à transmettre :**

- **Toute page migrée ensuite se câble en deux gestes** : l'aiguillage inline en TOUT PREMIER dans le `<head>` de la nouvelle page (sinon elle clignote), et une balise `ui-switch.js` en fin de `<body>` de chacune des deux versions. Rien d'autre.
- **Quand la nouvelle version reprendra le nom de l'ancienne** (`marvel.html`, phase 5) : déposer d'abord une copie VERBATIM de l'ancienne page dans `public/legacy/<page>.html`, ne plus jamais la retoucher, et faire pointer `data-ancienne` dessus. La convention est écrite en tête de `ui-switch.js`.
- **La règle qui protège le filet de sécurité** : sans préférence, une page migrée doit rester identique au pixel près. Toute future modification de `ui-switch.js` doit être suivie d'un `npm run captures` vert sur les écrans anciens.
- **`ui-switch.js`, `prepare.html` et `scene.html` vivent hors du dépôt git**, comme les fixtures de 01-03. Le re-zip vers `Fusion/` (plan 01-06) est leur seule sauvegarde. `ui-switch.js` étant la sortie de secours elle-même, sa perte serait coûteuse.

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*
