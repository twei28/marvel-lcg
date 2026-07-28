---
phase: 02-fondations-design-system
plan: 03
subsystem: infra
tags: [deploiement, rsync, wsl, bash, cache-busting, sha256, vite, serveur-python]

# Dependency graph
requires:
  - phase: 02-02
    provides: projet ui-app/ (npm run build, garde-fou verifier-sortie.mjs, dist/, styles/tokens.css)
  - phase: 02-01
    provides: 27 references visuelles qui prouvent l'absence de regression apres deploiement
provides:
  - ui-app/deployer.sh — commande unique build + garde-fou + rsync + tokens + empreintes
  - public/app/vitrine.html servie en 200 text/html par le serveur Python, sans modification backend
  - public/css/tokens.css en place, servie brute en 200 text/css (prete pour 02-05)
  - Fin des ?v=N tenus a la main : 5 occurrences remplacees par des empreintes de contenu
affects: [02-04, 02-05 branchement tokens, 02-06 tokenisation, 02-09 contenu de la vitrine, phase 3 ecrans pilotes, phase 5 plateau]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Franchissement Windows -> WSL par rsync en bash, jamais par Node (Node est le binaire Windows)"
    - "Cache-busting par empreinte de contenu (8 premiers caracteres du sha256), recalculee a chaque deploiement"
    - "Reecriture des references du plus profond vers le plus superficiel : un fichier a la fois cible et source est mis a jour avant que son empreinte ne soit lue"
    - "Aucune ecriture dans l'arborescence du jeu si le contenu ne change pas (ces fichiers vivent hors du depot git)"

key-files:
  created:
    - ui-app/deployer.sh
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/app/vitrine.html
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/app/assets/vitrine-B0-ceB0o.js
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/app/assets/vitrine-fnoB9GLi.css
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/css/tokens.css
  modified:
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/scene.html
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/prepare.html
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/prepare/app.js

key-decisions:
  - "Ordre de reecriture du plus profond vers le plus superficiel : les imports de app.js avant l'empreinte de app.js dans prepare.html, sinon deux deploiements seraient necessaires pour converger"
  - "Aucun fichier du jeu n'est reecrit si son contenu ne change pas : garde par grep puis comparaison, ecriture par redirection et jamais par mv (inode, droits et bit d'execution conserves)"
  - "vitrine.html n'entre pas dans ui-check/ecrans.ts a ce plan : une nouvelle reference passe par captures:valider, qui est un geste humain, et la page n'a pas encore son contenu (02-09)"

patterns-established:
  - "Un deploiement sans changement ne laisse aucune trace : mesurable par find -newer"
  - "Motifs sed ancres sur un nom de fichier precis, jamais un ?v= generique"
  - "Sauvegarde des fichiers du jeu hors depot dans ~/marvel-work/scratch/ avant toute reecriture"

# Metrics
duration: 7 min
completed: 2026-07-28
---

# Phase 2 Plan 03 : Deploiement et empreintes de contenu - Summary

**Une commande bash unique construit la nouvelle UI, la controle et la depose dans le codebase vivant ; le serveur Python sert `/app/vitrine.html` en 200 `text/html` avec React monte dedans, sans qu'une ligne de backend ait bouge, et les 5 `?v=N` tenus a la main sont remplaces par des empreintes de contenu recalculees a chaque deploiement.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-07-28T14:20:38Z
- **Completed:** 2026-07-28T14:28:12Z
- **Tasks:** 3
- **Files modified:** 1 dans le depot (`ui-app/deployer.sh`), 8 cote jeu (hors depot)

## Accomplishments

- **`bash ui-app/deployer.sh` fait tout en une commande** : `npm run build`, garde-fou d'extensions, `rsync -a --delete` de `dist/` vers `public/app/`, copie de `tokens.css`, recalcul des 5 empreintes. Sortie en code 0, message final en francais.
- **Le serveur Python sert la page React sans avoir ete touche.** `/app/vitrine.html` repond 200 `text/html`, ses deux assets 200 `application/javascript` et 200 `text/css`, et le bundle recu est **bit a bit identique** au fichier sur disque (190 782 octets) : pas de reponse-fantome 200-mais-vide.
- **React monte reellement dans la page servie**, verifie au navigateur sans tete : `#vitrine` ne contient plus « Chargement... » mais le texte rendu par React 19.2.8, avec **zero erreur console** et un titre qui n'est pas `Version Mismatch` (garde-fou anti `clean_cache.html`).
- **Critere 5 demontre en 4 temps** : empreinte de `wizard.css` a `83bb78a9` → ajout d'une ligne de commentaire au fichier → `bash ui-app/deployer.sh` → empreinte passee a `e00683aa`, egale au `sha256sum` du nouveau contenu. Retour au fichier original : l'empreinte revient a `83bb78a9`, `wizard.css` est byte a byte l'original.
- **Plus aucun `?v=` litteral dans le perimetre** : les 5 occurrences sont des empreintes de 8 caracteres hexadecimaux. La desynchronisation constatee par la recherche (`prepare.html` a `v=18` pendant que les imports de `app.js` etaient a `v=9` et `v=5`) ne peut plus se reproduire.
- **`font-awesome.css` intact** : ses 9 occurrences de `?v=4.7.0` dans des `url()` de polices n'ont jamais ete approchees (fichier non modifie depuis le 26/07).
- **Les 27 references visuelles restent vertes** (`npm run captures`, 1,2 min, 27 passed sur les 3 gabarits).
- **Le diff cote jeu est chirurgical** : exactement 5 lignes changees dans 3 fichiers, toutes des valeurs `?v=`. Rien d'autre.

## Task Commits

1. **Tache 1 : le script de deploiement** - `86d0c48` (feat)
2. **Tache 2 : prouver que le serveur Python sert la page** - aucun commit : tache de verification pure, ses artefacts (`public/app/`) vivent hors du depot git. La preuve est le tableau ci-dessous.
3. **Tache 3 : prouver le rechargement sans `?v=N` et l'absence de regression** - aucun commit : meme raison, les fichiers reecrits (`scene.html`, `prepare.html`, `app.js`) sont hors depot.

**Plan metadata:** voir commit `docs(02-03)`.

## Preuve du critere 1 : le serveur Python sert la nouvelle UI

Serveur `launcher_fast.py`, port 2345, **non relance** pendant tout le plan (aucune partie perdue).

| Requete | Code | Type MIME | Verdict |
|---|---|---|---|
| `/app/vitrine.html` | 200 | `text/html` | La page React est servie |
| `/app/assets/vitrine-B0-ceB0o.js` | 200 | `application/javascript` | 190 782 octets, identiques au disque |
| `/app/assets/vitrine-fnoB9GLi.css` | 200 | `text/css` | Feuille du bundle |
| `/css/tokens.css` | 200 | `text/css` | 814 octets, prete pour le plan 02-05 |
| `/main.html` | 200 | `text/html` | Page actuelle intacte |
| `/scene.html` | 200 | `text/html` | Page actuelle intacte |
| `/prepare.html` | 200 | `text/html` | Page actuelle intacte |
| `/cards.html` | 200 | `text/html` | Page actuelle intacte |
| `/deck.html` | 200 | `text/html` | Page actuelle intacte |
| `/replay.html` | 200 | `text/html` | Page actuelle intacte |

Controles complementaires :

| Controle | Attendu | Mesure |
|---|---|---|
| Marqueur `id="vitrine"` dans le corps servi | 1 | 1 |
| Extensions hors liste blanche dans `public/app/` | 0 | 0 |
| React monte (texte de `#vitrine` != « Chargement... ») | monte | « Vitrine du design system … Rendue par React 19.2.8. » |
| Erreurs console au chargement | 0 | 0 |
| Titre de page (garde-fou `clean_cache.html`) | pas `Version Mismatch` | « Vitrine du design system - Marvel Champions » |
| Fichiers modifies dans `src/` du jeu | 0 | 0 |
| Fichiers modifies dans `public/js/marvel/` | 0 | 0 |
| `git status` du depot | rien hors `ui-app/` | conforme |

## Preuve du critere 5 : les empreintes se recalculent seules

| Etape | `scene.html` | `sha256sum css/menu/wizard.css` |
|---|---|---|
| 1. Etat de depart | `wizard.css?v=83bb78a9` | `83bb78a9` |
| 2. Ajout de `/* empreinte */` en fin de fichier | inchange | `e00683aa` |
| 3. `bash ui-app/deployer.sh` | `wizard.css?v=e00683aa` | `e00683aa` |
| 4. Retour au fichier original + redeploiement | `wizard.css?v=83bb78a9` | `83bb78a9` |

Etat final des 5 references du perimetre, toutes des empreintes de 8 caracteres hexadecimaux :

| Fichier edite | Reference | Empreinte | Ancienne valeur tenue a la main |
|---|---|---|---|
| `scene.html` | `css/menu/wizard.css` | `83bb78a9` | `9` |
| `prepare.html` | `css/prepare/prepare.css` | `2f4ae465` | `18` |
| `prepare.html` | `js/prepare/app.js` | `eb512376` | `18` |
| `js/prepare/app.js` | `js/prepare/api.js` | `9c2a05b9` | `9` |
| `js/prepare/app.js` | `js/prepare/launcher.js` | `e5ad2f82` | `5` |

`grep -rnoE '\?v=[A-Za-z0-9.]+' scene.html prepare.html js/prepare/app.js | grep -vE '\?v=[0-9a-f]{8}$' | wc -l` → **0**.

## Files Created/Modified

**Dans le depot :**

- `ui-app/deployer.sh` (69 lignes) - build, garde-fou, `rsync -a --delete` vers `public/app/`, copie de `tokens.css`, recalcul des empreintes.

**Cote jeu (hors depot git) :**

- `public/app/vitrine.html` + `public/app/assets/*.js` + `public/app/assets/*.css` - la page React servie.
- `public/css/tokens.css` - copie des tokens servie brute aux pages anciennes (aucune page ne la reference encore : c'est le plan 02-05).
- `public/scene.html`, `public/prepare.html`, `public/js/prepare/app.js` - une valeur `?v=` chacun (2 pour `prepare.html` et `app.js`), rien d'autre.

Sauvegarde des 4 fichiers du jeu avant toute reecriture : `~/marvel-work/scratch/avant-02-03/` (ils vivent hors du depot, le re-zip vers `Fusion/` est leur seule autre sauvegarde).

## Decisions Made

- **L'ordre de reecriture va du plus profond vers le plus superficiel.** `app.js` est a la fois une cible (ses deux imports portent une empreinte) et une source (`prepare.html` porte l'empreinte de `app.js`). Dans l'ordre du plan, `prepare.html` recevait l'empreinte de la version *precedente* de `app.js` et il fallait deux deploiements pour converger. Inverse, la convergence est acquise en une passe : verifie, `eb512376` dans `prepare.html` est bien le `sha256sum` du `app.js` deja reecrit.
- **Un deploiement qui ne change rien ne laisse aucune trace.** Mesure par `find public -newer <marqueur>` : apres un deuxieme deploiement identique, zero fichier remue hors `public/app/`. Ces pages vivent hors du depot git ; les reecrire pour rien est un risque gratuit.
- **L'ecriture se fait par redirection (`cat > cible`) et jamais par `mv`.** L'inode, les droits et le bit d'execution sont conserves — `prepare.html` et `app.js` sont en `-rwxr-xr-x`, `scene.html` en `-rw-r--r--`, et ils le restent.
- **`vitrine.html` n'est pas ajoute a `ui-check/ecrans.ts` dans ce plan.** Deux raisons : une nouvelle reference ne peut naitre que par `npm run captures:valider`, qui est un geste humain (decision 01-02), et la page est encore un squelette dont le contenu arrive au plan 02-09. L'ajouter maintenant figerait une reference d'une page appelee a changer entierement.
- **`cache_max_age` de `launch.json` n'a pas ete touche**, conformement au plan : ce serait modifier la configuration du livrable pour un probleme de 5 lignes.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Ordre de reecriture des empreintes : `prepare.html` portait l'empreinte de la version precedente de `app.js`**

- **Found during:** Tache 1
- **Issue:** Le plan traite `prepare.html ← app.js` **avant** `app.js ← api.js` et `app.js ← launcher.js`. Or ces deux dernieres modifient `app.js`, donc changent son sha256. L'empreinte inscrite dans `prepare.html` etait celle du `app.js` d'avant reecriture : le navigateur aurait servi un `app.js` de cache alors que ses imports avaient change. Il aurait fallu deux deploiements pour converger.
- **Fix:** Les deux lignes visant `app.js` comme cible passent avant celle qui le lit comme source, avec un commentaire qui explique pourquoi l'ordre n'est pas libre.
- **Files modified:** `ui-app/deployer.sh`
- **Verification:** `eb512376` dans `prepare.html` == `sha256sum js/prepare/app.js | cut -c1-8` apres deploiement, en une seule passe.
- **Committed in:** `86d0c48`

**2. [Rule 2 - Missing Critical] `sed -i` reecrivait des pages du jeu qui n'avaient rien a y voir**

- **Found during:** Tache 1
- **Issue:** `sed -i` reecrit toujours sa cible, meme sans substitution. La boucle `tokens.css` visant 5 pages, chaque deploiement reecrivait `cards.html`, `deck.html` et `replay.html` alors qu'aucune ne reference `tokens.css`. Mesure : `find public -newer` remontait ces 3 fichiers apres un deploiement a vide. Contenu identique, mais ces fichiers vivent **hors du depot git** — les remuer sans raison est un risque gratuit, et cela masque quels fichiers un deploiement a reellement changes.
- **Fix:** Garde `grep -qE` (rien a remplacer = on ne touche pas), puis ecriture uniquement si le contenu differe, par redirection dans le fichier existant plutot que par `mv` d'un temporaire (inode, droits et bit d'execution conserves). Meme garde par `cmp -s` sur la copie de `tokens.css`.
- **Files modified:** `ui-app/deployer.sh`
- **Verification:** Deuxieme deploiement identique → `find public -newer <marqueur> | grep -v '^public/app/'` renvoie une liste vide.
- **Committed in:** `86d0c48`

---

**Total deviations:** 2 auto-corrigees (1 bug, 1 fonctionnalite critique manquante)
**Impact on plan:** Aucune derive de perimetre. Les deux corrections portent sur le meme fichier, `deployer.sh`, et vont dans le sens du plan : etre chirurgical sur des fichiers qui n'ont pas de filet git.

## Issues Encountered

- **Le controle `font-awesome.css` du plan attendait `grep -c` = 7, la mesure donne 3.** Ce n'est pas une regression : `grep -c` compte les **lignes**, pas les occurrences, et le fichier est partiellement minifie. Le compte reel est de **9 occurrences sur 3 lignes**, et le fichier n'a pas ete modifie (horodatage inchange depuis le 26/07, et aucune commande du plan ne le vise). Le chiffre 7 de la recherche etait un comptage d'occurrences approximatif ; c'est l'attendu du plan qui etait faux, pas le resultat.
- **Node ne lit pas un chemin absolu WSL, y compris pour son propre script d'entree.** `node /mnt/c/...` echoue en `Cannot find module 'C:\mnt\c\...'`. Le controle navigateur sans tete a du etre lance depuis `ui-check/` avec un chemin **relatif**. Piege deja connu pour les imports, il vaut aussi pour l'argument de `node` lui-meme.
- Le script de controle navigateur (montage de React, erreurs console) etait un jetable : ecrit dans `ui-check/`, execute, supprime. `ui-check/` est revenu a son etat d'origine (`git status` propre).

## User Setup Required

Aucun - aucune configuration de service externe.

## Next Phase Readiness

**Pret pour la suite de la phase 2.** Les criteres 1 et 5 de la phase sont demontres sur piece.

Ce qui est desormais disponible pour les plans suivants :

- **`bash ui-app/deployer.sh` est le seul chemin vers le jeu.** Tout plan qui modifie `ui-app/` se termine par cette commande. Ne jamais recopier `dist/` a la main, ne jamais editer `public/css/tokens.css` (c'est une copie, la source est `ui-app/styles/tokens.css`).
- **Le plan 02-05 n'a plus qu'a ajouter la balise.** `public/css/tokens.css` est servie en 200 `text/css` ; les lignes qui recalculeront son empreinte sont deja dans `deployer.sh` et attendent que la reference existe.

Points de vigilance transmis :

- **Toute nouvelle reference `?v=` doit etre declaree dans `deployer.sh`**, sinon elle reste tenue a la main et se desynchronise — exactement le bug que ce plan vient de fermer. Une ligne `remplacer` par couple (page, fichier reference), en respectant l'ordre du plus profond vers le plus superficiel.
- **`public/app/` est nouveau dans l'arborescence du jeu** : le prochain re-zip vers `Fusion/` doit l'emporter (c'est du livrable), au contraire de `ui-app/` et `ui-check/` qui restent dehors. A verifier au prochain rituel de livraison.
- **`vitrine.html` n'est toujours pas dans `ui-check/ecrans.ts`.** A ajouter avec le marqueur `#vitrine` au plan 02-09, quand la page aura son contenu definitif, via `npm run captures:valider`.
- **Le serveur n'a pas ete relance de tout le plan** : `public/` etant vu par `.game/public` (lien symbolique), les fichiers deposes sont servis a chaud. C'est ce qui permet de deployer sans couper une partie.

---
*Phase: 02-fondations-design-system*
*Completed: 2026-07-28*
