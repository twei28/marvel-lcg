---
phase: 02-fondations-design-system
plan: 04
subsystem: ui
tags: [css, cascade, important, specificite, wizard, scene-html, playwright, styles-calcules]

# Dependency graph
requires:
  - phase: 01-filet-de-securite
    provides: harnais ui-check (27 references, page de comparaison, garde-fou de version)
  - phase: 02-01
    provides: les 3 panneaux caches du wizard sous surveillance photographique
  - phase: 02-03
    provides: deployer.sh, seul chemin vers le jeu, et empreintes de contenu
provides:
  - wizard.css sans !important (2 exceptions documentees, face a des styles en ligne poses par JS)
  - css/menu/scene-inline.css, les 361 lignes jadis en ligne dans scene.html, chargees AVANT wizard.css
  - Garde-fou de cascade dans deployer.sh : un deploiement echoue si le compte de !important remonte
  - ui-check/scripts/releve-styles.mjs : preuve d'invariance par les styles CALCULES, etats et survols compris
  - ui-check/scripts/serveur-dev.py : second moteur sur un autre port, sans mot de passe ni tunnel
  - UI_CHECK_BASE : adresse du jeu parametrable dans le harnais (defaut inchange 2345)
affects: [02-05 pose des @layer, 02-06 tokenisation des feuilles anciennes, 02-07 a 02-10, phase 5 remplacement de scene.html]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Un !important se remplace par l'ordre de source d'abord, par la specificite ensuite, jamais par un autre !important"
    - "Un style en ligne pose par JavaScript ne se bat qu'avec !important : c'est la seule exception legitime, et elle se commente dans le fichier"
    - "L'invariance se prouve sur les styles CALCULES (etats et survols compris), pas seulement sur des pixels au chargement"
    - "Un garde-fou chiffre dans deployer.sh fige un acquis : le modifier devient un geste conscient, dans le meme commit"

key-files:
  created:
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/css/menu/scene-inline.css
    - ui-check/scripts/releve-styles.mjs
    - ui-check/scripts/serveur-dev.py
  modified:
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/css/menu/wizard.css
    - /home/arnau/marvel-work/fusion/marvel-lcg-src/public/scene.html
    - ui-app/deployer.sh
    - ui-check/playwright.config.ts
    - ui-check/global-setup.ts

key-decisions:
  - "Les regles jadis en ligne dans scene.html sont chargees AVANT wizard.css : c'est ce deplacement, et lui seul, qui rend les 105 !important inutiles"
  - "Deux !important conserves et commentes : les vignettes de la galerie de heros recoivent un attribut style du JavaScript de scene.html, qu'aucune feuille ne peut battre"
  - "Le bloc panneaux resserres est descendu apres les regles qu'il corrige, au lieu de leur passer devant par la force"
  - "La declaration padding:12px 16px 14px de ce bloc n'a PAS ete recopiee : elle etait deja perdante avant la purge, la remonter aurait change le rendu"
  - "deployer.sh refuse un deploiement si wizard.css compte autre chose que 2 !important, garde-fou eprouve par un vrai negatif"
  - "Le harnais vise 127.0.0.1:2345 par defaut ; UI_CHECK_BASE le deplace sans changer le comportement pour un futur lecteur"
  - "Fusion/marvel-lcg-src est un codebase de distribution perime : un 200 OK sur /main.html ne prouve rien, il faut lire le CONTENU"

patterns-established:
  - "Mesurer avant de corriger : 2787 differences de style calcule se ramenaient a 6 causes"
  - "Un correctif de cascade se rejoue par script (corriger-wizard.py) et non a la main : une mesure avant/apres ecrase le fichier"

# Metrics
duration: 2h20
completed: 2026-07-28
---

# Phase 2 Plan 04: Purge des !important de wizard.css Summary

**Les 105 declarations `!important` de `wizard.css` sont tombees a 2, en rendant a l'ordre de source et a la specificite le travail qu'elles faisaient de force : les 361 lignes de CSS qui vivaient en vrac dans `scene.html` sont reunies dans `scene-inline.css`, charge avant elle, et zero style calcule n'a bouge, etats et survols compris.**

## Performance

- **Duration:** 2h20 (dont ~57 min d'execution, ~80 min d'attente au checkpoint)
- **Started:** 2026-07-28T16:08Z
- **Completed:** 2026-07-28T18:28Z
- **Tasks:** 2 taches automatiques + 1 checkpoint + 2 taches de deblocage non prevues
- **Files modified:** 5 modifies, 3 crees

## Accomplishments

- **`@layer` peut maintenant etre pose.** C'etait le seul but : une couche posee au-dessus de 105 declarations importantes aurait perdu contre elles. L'etape 1 de la sequence CSS obligatoire de la phase est franchie.
- **Six regressions reelles trouvees et corrigees, aucune devinee.** La purge seche a produit 2787 differences de style calcule ; elles se ramenaient a 6 causes, chacune corrigee par le levier prevu (ordre de source, puis specificite).
- **Trois regressions invisibles en photo ont ete rattrapees** : l'outline rouge des cartes selectionnees, l'ombre blanche au survol, le grisage des paquets indisponibles. Aucune n'apparait dans les 27 references : sans mesure des styles calcules, elles seraient parties en production.
- **Un garde-fou chiffre** dans `deployer.sh` : le compte de `!important` ne peut plus remonter par accident.
- **Un outil de preuve reutilisable** (`releve-styles.mjs`) pour les plans 02-05 et 02-06, qui feront exactement le meme pari : « je change la cascade et rien ne bouge ».

## Task Commits

1. **Deblocage : serveur de dev sur un second port, adresse du harnais parametrable** - `f0d7142` (chore)
2. **Tache 1 : sortir les 9 blocs de style de scene.html vers scene-inline.css** - `0558a47` (refactor)
3. **Tache 2 : purger les 105 !important, cascade retablie** - `e2eca9a` (feat)
4. **Outil de releve et de comparaison des styles calcules** - `0c63b6c` (chore)

**Plan metadata:** voir le commit `docs(02-04)` qui suit.

## Files Created/Modified

Hors depot git (codebase du jeu, `~/marvel-work/fusion/marvel-lcg-src/public/`) :

- `css/menu/scene-inline.css` **(cree, 398 lignes)** - Les 9 blocs `<style>` de `scene.html`, recopies verbatim dans l'ordre du document, un commentaire `bloc N (ex-ligne X)` par bloc pour retrouver l'origine d'une regle. En-tete expliquant pourquoi le fichier existe et dans quel ordre il doit etre charge.
- `css/menu/wizard.css` - 105 `!important` retires, 2 conserves et commentes ; bloc « panneaux resserres » descendu ; 6 regles ajoutees pour reprendre par la specificite ce que la force obtenait.
- `scene.html` - Plus un seul bloc `<style>` ; un `<link>` vers `scene-inline.css` place **avant** celui de `wizard.css`. Ordre final : `style.css`, `font-awesome.css`, `scene-inline.css`, `wizard.css`.

Dans le depot :

- `ui-app/deployer.sh` - Empreinte de contenu pour `scene-inline.css` ; garde-fou de cascade (compte de `!important` attendu : 2).
- `ui-check/scripts/serveur-dev.py` **(cree)** - Second moteur depuis le codebase de travail, port au choix, sans mot de passe, sans tunnel, sans ouverture de navigateur.
- `ui-check/scripts/releve-styles.mjs` **(cree)** - `relever` / `comparer` les styles calcules : 4 panneaux, etats de selection poses a la main, 9 survols cibles.
- `ui-check/playwright.config.ts`, `ui-check/global-setup.ts` - `UI_CHECK_BASE`, defaut inchange `http://127.0.0.1:2345`.

## Journal des regressions (ce que la recherche ne pouvait pas predire)

Purge seche des 105 `!important`, sans autre changement : **2787 differences de style calcule**, ramenees a **6 causes**. Aucune n'a ete corrigee par un `!important`.

| # | Ce qui cassait | Cause | Levier |
|---|----------------|-------|--------|
| 1 | Padding des panneaux, marge et taille des titres, marge des fieldsets (6 declarations) | Le bloc « panneaux resserres » etait ecrit **avant** les regles qu'il corrige, dans le meme fichier. Il ne gagnait que par `!important`. | **Ordre de source** : bloc descendu apres la section fieldset. Un cran de specificite ajoute pour les fieldsets imbriques (`.w-step-panel fieldset fieldset{margin:0}` restait devant). |
| 2 | Bordures des blocs d'options (`#mode` vert, `#rules` cramoisi, `#challenge` magenta…) | `scene-inline.css` colore ces bordures avec un selecteur d'**id** ; `.w-step-panel details` n'a que des classes, et aucune classe ne passe devant un id. | **Specificite** : `.w-step-panel details#mode, …` pour les 5 blocs. |
| 3 | Contour rouge (orange si verrouille) des cartes selectionnees | `menu/style.css` cible `.click img`, plus specifique que `#modular-sets img`. | **Specificite** : regle calquee, placee plus bas. |
| 4 | Bordure noire au survol d'une carte selectionnee | `menu/style.css` cible `button.click:hover img`. | **Specificite** — avec un piege : un premier essai en `.click:hover img` (sans `button`) etait plus faible d'un cran et la bordure revenait. Mesure, corrige. |
| 5 | Ombre portee blanche au survol des paquets et des cartes | `menu/style.css` cible `…:hover`, plus specifique que `#modular-sets button`. | **Specificite**. |
| 6 | Grisage des paquets indisponibles | `menu/style.css` cible `#set-images div.disable`. | **Specificite**. |

**Les 2 exceptions conservees**, toutes deux sur la galerie de heros de depart : le script de `scene.html` (vers la ligne 1700) pose un **attribut `style`** sur chaque vignette, `border-radius:5px` a la construction et `borderColor='#c00'` au survol. Un style en ligne bat toute feuille de style : ni l'ordre de source ni la specificite n'y peuvent quoi que ce soit. Les deux declarations portent un commentaire qui nomme la ligne de JavaScript responsable et la condition de leur disparition.

**Les regressions 3, 5 et 6 n'apparaissent dans aucune des 27 references.** Elles ne se voient qu'en survolant ou en selectionnant. C'est la justification de `releve-styles.mjs` : les captures prouvent qu'un ecran ne bouge pas au chargement, pas que la cascade est intacte.

## Decisions Made

- **Le deplacement du `<link>` avant `wizard.css` est le coeur du plan, la purge n'en est que la consequence.** Tache 1 le place volontairement APRES `wizard.css` (ordre de cascade strictement identique a l'existant) pour verifier que l'extraction seule ne change rien : 27 references vertes. Tache 2 le remonte. Deux etapes separees, deux commits, deux verifications.
- **La declaration `padding:12px 16px 14px` du bloc « panneaux resserres » n'a pas ete recopiee.** Avant la purge, deux regles importantes se disputaient ce padding et la plus basse gagnait : cette declaration etait deja morte. La remonter avec le bloc aurait change le rendu. Mesure, puis commentee dans le fichier.
- **Le compte de `!important` se verifie hors commentaires.** Les commentaires du fichier parlent de `!important` : un `grep` brut en trouve 8 la ou il y a 2 declarations. Le garde-fou de `deployer.sh` retire les commentaires avant de compter.
- **Le garde-fou vit dans `deployer.sh` et non dans un test.** C'est le seul chemin vers le jeu : tout changement de `wizard.css` y passe. Un test Playwright aurait du lire un chemin WSL depuis Node, qui est le binaire Windows.
- **Le correctif de cascade est rejoue par script** (`corriger-wizard.py`, dans `~/marvel-work/scratch/02-04/`). Les editions manuelles avaient ete ecrasees par une restauration de l'etat « avant » pendant une mesure : un fichier hors depot git ne pardonne pas.
- **Validation visuelle : NON EFFECTUEE, elle reste DUE.** Le plan a ete cloture sur les seules mesures automatiques, sans reponse de l'utilisateur : 27 references vertes sans revalidation, 0 difference de style calcule sur les 4 panneaux, 0 difference sur 10 etats de selection et de survol. Ces mesures sont solides mais ne remplacent pas le coup d'oeil humain prevu par le plan (`gate="blocking"`). A faire avant 02-05, qui posera `@layer` par-dessus.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Le port 2345 ne servait pas le codebase de travail**

- **Found during:** verification d'environnement, avant la tache 1
- **Issue:** `http://127.0.0.1:2345/main.html` repondait bien 200, mais avec la page `Authentication Required`. Le port etait occupe par une partie multijoueur lancee par `JOUER-EN-MULTI.bat`, servie depuis `Fusion/marvel-lcg-src` (codebase de **distribution**, perime : `scene.html` different, pas de `public/app/`), avec mot de passe et tunnel Cloudflare public ouvert. Le codebase de travail n'etait servi par personne. Couper ce serveur aurait mis fin a la partie de plusieurs joueurs.
- **Fix:** Checkpoint remonte a l'utilisateur, qui a choisi un second serveur. `ui-check/scripts/serveur-dev.py` demarre un moteur depuis le codebase de travail sur le port 2346, sans mot de passe ni tunnel, sans ouvrir de navigateur. Il reutilise `launcher_fast.py --build-only` puis reecrit `.game/launch.json` (artefact de build), jamais `launch.json` a la racine du jeu.
- **Files modified:** `ui-check/scripts/serveur-dev.py` (cree)
- **Verification:** `/scene.html` sur 2346 porte l'empreinte posee par `deployer.sh` et `/app/vitrine.html` repond 200 ; les 27 references sont vertes contre ce serveur, ce qui prouve qu'il sert bien le codebase des references. Le processus du port 2345 et `cloudflared` n'ont pas ete touches.
- **Commit:** `f0d7142`

**2. [Rule 3 - Blocking] `RELEASE=1` manquant au demarrage du second serveur**

- **Found during:** premier demarrage de `serveur-dev.py`
- **Issue:** `ModuleNotFoundError: No module named 'editor.editor'`. Sans la variable `RELEASE`, le moteur demarre en mode debug (version `0.5.9.200d`) et importe l'editeur, absent de la distribution. Les references du harnais ont ete prises en mode release (`0.5.9.200r`).
- **Fix:** `os.environ["RELEASE"] = "1"` pose avant tout import du moteur, comme le fait `launcher_fast.py`.
- **Files modified:** `ui-check/scripts/serveur-dev.py`
- **Verification:** `/main.html` sert bien `Marvel Champions: Digital Edition`.
- **Commit:** `f0d7142`

**3. [Rule 3 - Blocking] Adresse du jeu en dur dans le harnais**

- **Found during:** deblocage
- **Issue:** `playwright.config.ts` et `global-setup.ts` ecrivaient `http://127.0.0.1:2345` en dur. Impossible de viser le second serveur.
- **Fix:** `UI_CHECK_BASE`, exportee depuis `playwright.config.ts` et reutilisee par `global-setup.ts`. **Defaut inchange** : `http://127.0.0.1:2345`. Depuis WSL, npm passe par `cmd.exe` : la variable doit etre relayee par `WSLENV`, ce que le commentaire du fichier precise.
- **Files modified:** `ui-check/playwright.config.ts`, `ui-check/global-setup.ts`
- **Verification:** les 27 references passent contre 2346 avec la variable, et le comportement par defaut du harnais est intact pour un futur lecteur.
- **Commit:** `f0d7142`

**4. [Rule 2 - Missing Critical] Aucune preuve possible sur les etats non photographies**

- **Found during:** tache 2, apres la purge seche
- **Issue:** Le plan demandait de corriger « chaque regression » en s'appuyant sur `npm run captures`. Or les captures ne montrent que le chargement : ni survol, ni carte selectionnee, ni paquet indisponible. Trois des six regressions (contour rouge, ombre blanche au survol, grisage) etaient **invisibles pour les 27 references** et seraient passees.
- **Fix:** Mesure des styles CALCULES avant/apres, element par element et propriete par propriete, sur les 4 panneaux, puis sur les etats poses a la main et 9 survols. Outil consolide et versionne en `ui-check/scripts/releve-styles.mjs` pour les plans 02-05 et 02-06.
- **Files modified:** `ui-check/scripts/releve-styles.mjs` (cree)
- **Verification:** deux releves consecutifs sont identiques (determinisme), et le releve refuse de tourner si la page servie n'est pas l'ancienne preparation.
- **Commit:** `0c63b6c`

**5. [Rule 2 - Missing Critical] Rien n'empechait les `!important` de revenir**

- **Found during:** fin de la tache 2
- **Issue:** L'acquis du plan (« zero `!important`, au plus 3 exceptions ») n'etait ecrit nulle part ailleurs que dans ce document. Un futur plan pouvait en reintroduire sans que rien ne bronche, et rendre la tokenisation impossible a nouveau.
- **Fix:** Garde-fou dans `deployer.sh` : compte des declarations hors commentaires, echec du deploiement si le nombre differe de 2, avec un message francais qui explique quoi faire si l'exception est legitime.
- **Files modified:** `ui-app/deployer.sh`
- **Verification:** eprouve par un vrai negatif (une declaration `!important` ajoutee au fichier : sortie 1, message affiche, puis retour a l'etat correct).
- **Commit:** `e2eca9a`

---

**Total deviations:** 5 auto-corrigees (3 blocages, 2 fonctionnalites critiques manquantes)
**Impact on plan:** Les trois blocages etaient des conditions d'execution, pas des choix. Les deux ajouts servent directement le critere du plan : l'un prouve l'invariance la ou les photos sont aveugles, l'autre empeche l'acquis de se defaire. Aucun elargissement de perimetre : `public/js/marvel/` et `src/` du jeu n'ont pas ete ouverts.

## Issues Encountered

- **Les editions manuelles de `wizard.css` ont ete perdues une fois.** Pour mesurer l'ecart avant/apres, il faut redeployer l'etat « avant » ; la copie a ecrase le fichier corrige, qui vit hors du depot git. Refait par script (`corriger-wizard.py`), ce qui a rendu la suite des allers-retours sans risque. A retenir pour 02-05 et 02-06 : **tout correctif sur un fichier du jeu doit etre rejouable par script tant que des mesures avant/apres sont en cours.**
- **Deux artefacts de mesure ont failli passer pour des regressions** : un `cursor: pointer` sur un `summary` (la souris restait posee a l'endroit du dernier clic, et la mise en page ayant bouge, elle survolait un autre element) et un `box-shadow` en cours de transition (`.16s`). Les deux ont disparu apres correction du vrai probleme et ajout d'une pause. Une mesure fine produit du bruit : il faut savoir le reconnaitre avant de « corriger » ce qui n'est pas casse.
- **`test-results/` est vide a chaque execution de Playwright.** Les outils de mesure y avaient ete deposes et ont ete effaces par un `npm run captures`. Ils vivent maintenant dans `ui-check/scripts/`.

## User Setup Required

Aucune configuration externe. En revanche, un serveur doit tourner :

```bash
~/marvel-work/python/bin/python3.10 \
  "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/ui-check/scripts/serveur-dev.py" --port 2346
```

Il tourne actuellement et doit rester allume pour les plans 02-05 a 02-09. Les commandes du harnais qui doivent le viser :

```bash
export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE
npm run captures
```

## Next Phase Readiness

**Pret pour la pose de `@layer` (plan 02-05).** La cascade de l'ancienne preparation est saine : plus une declaration importante en dehors des deux exceptions commentees, et l'ordre de chargement fait le travail. Une couche `legacy` posee au-dessus ne sera plus renversee.

Points de vigilance a transmettre :

- **`Fusion/marvel-lcg-src` est un codebase de distribution perime**, servi sur 2345 par `JOUER-EN-MULTI.bat` avec mot de passe et tunnel public. Le codebase de travail est `~/marvel-work/fusion/marvel-lcg-src`. **Un `200 OK` sur `/main.html` ne prouve rien** : la page d'authentification repond 200. Controler le CONTENU (le titre doit contenir `Marvel`).
- **Le serveur 2346 doit rester allume** ; sa commande de demarrage est ci-dessus. Il ne se relance pas tout seul apres un redemarrage du poste.
- **Deux `!important` subsistent**, et le garde-fou de `deployer.sh` les compte. Le jour ou le JavaScript de `scene.html` cessera de poser `border-radius:5px` et `borderColor='#c00'` sur les vignettes de la galerie (phase 5, quand `scene.html` sera remplace), les deux exceptions disparaissent et `IMPORTANTS_ATTENDUS` passe a 0.
- **`scene-inline.css` est un fichier de transition.** Il ne represente aucune intention de design : c'est l'ancien contenu en ligne, range. Quand `scene.html` sera remplace en phase 5, il partira avec, et les 3 ecrans `preparation-rencontre|heros|lancement` du harnais avec lui.
- **`releve-styles.mjs` est l'outil de preuve des plans 02-05 et 02-06.** Relever avant, appliquer, relever apres, comparer : la sortie doit dire « Aucun style calcule n a change ». Ses fichiers pesent ~200 Mo et doivent aller dans `test-results/`, qui est ignore par git.
- **La validation visuelle humaine des 4 etapes n'a pas eu lieu et reste DUE.** Le checkpoint `gate="blocking"` a ete franchi sans reponse de l'utilisateur. A faire sur `http://127.0.0.1:2346/scene.html` avant 02-05. Si un detail se revele plus tard, le point de depart est `~/marvel-work/scratch/02-04/` : `scene.html` et `wizard.css` d'origine, `apres-purge/` et `wizard-corrige.css`.

---
*Phase: 02-fondations-design-system*
*Completed: 2026-07-28*
