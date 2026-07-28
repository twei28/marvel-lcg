---
phase: 02-fondations-design-system
plan: 01
subsystem: testing
tags: [playwright, captures-visuelles, wizard, scene-html, css-important, filet-de-securite]

# Dependency graph
requires:
  - phase: 01-filet-de-securite
    provides: harnais ui-check (ecrans.ts, captures.spec.ts, 18 references, page de comparaison)
provides:
  - 3 ecrans surveilles de plus (panneaux 2, 3 et 4 du wizard de scene.html)
  - 9 images de reference supplementaires (27 au total)
  - Mecanisme reutilisable d'ouverture d'etape du wizard avant capture (champ etape)
  - Mecanisme reutilisable de depliage de contenu replie avant capture (champ depliages)
  - Garde-fou de preuves : refus de photographier un panneau dont le contenu n'est pas visible
affects: [02-04 purge des !important de wizard.css, 02-05 pose des @layer, 02-06 tokenisation des feuilles anciennes, toute modification future de scene.html]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ouverture d'un panneau masque par window.wizardShow(i) et non par un clic sur .w-step (le clic est conditionne par canPass[cur]())"
    - "Champ 'preuves' : un ecran refuse d'etre photographie si le contenu attendu n'est pas visible"
    - "Champ 'depliages' : ce que la page replie par defaut est ouvert avant la photo, sinon il echappe a la surveillance"
    - "Selecteur de bouton par son onclick et non par son libelle (resistant a une traduction)"

key-files:
  created:
    - ui-check/references/preparation-rencontre/{pc,tablette,mobile}.png
    - ui-check/references/preparation-heros/{pc,tablette,mobile}.png
    - ui-check/references/preparation-lancement/{pc,tablette,mobile}.png
  modified:
    - ui-check/ecrans.ts
    - ui-check/tests/captures.spec.ts

key-decisions:
  - "Ouverture d'etape par window.wizardShow(i) et jamais par un clic sur .w-step : le clic est conditionne par canPass[cur]() et ne fait rien tant que l'etape courante n'est pas valide"
  - "Les 3 nouveaux ecrans reutilisent le marqueur #w-stepper et le masque #seed_div de l'entree 'preparation' existante, laissee intacte"
  - "Un ecran qui ouvre une etape doit declarer des 'preuves' : sans elles, une photo d'entete vide passerait pour une reference valide"
  - "Le contenu replie par defaut (#modular-sets) est deplie avant la photo : sinon la moitie des !important du panneau reste hors champ"
  - "Les 9 references sont nees d'une absence (Playwright ecrit une reference manquante), sans jamais appeler --update-snapshots : la regle du plan 01-02 tient"

patterns-established:
  - "Un ecran d'ecrans.ts peut decrire une INTERACTION (etape, depliages) et pas seulement une URL"
  - "Toute nouvelle reference est controlee sur son CONTENU (lecture de l'image), pas seulement sur son existence"

# Metrics
duration: 12 min
completed: 2026-07-28
---

# Phase 2 Plan 01: Captures des panneaux caches du wizard Summary

**Les 3 panneaux de `scene.html` masques au chargement sont desormais photographies dans les 3 gabarits, via `window.wizardShow`, avec preuve de contenu et depliage des sets modulaires : `npm run captures` verifie 27 images au lieu de 18.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-07-28T14:03:13Z
- **Completed:** 2026-07-28T14:15:19Z
- **Tasks:** 2
- **Files modified:** 2 modifies, 9 crees

## Accomplishments

- **La purge des `!important` n'est plus aveugle.** Les ~45 declarations de `wizard.css` qui visent les panneaux 1, 2 et 3 (sur 105) sont maintenant sous surveillance photographique. C'etait l'etape zero de la sequence CSS obligatoire de la phase.
- **Un mecanisme d'ouverture d'etape reutilisable**, pose dans `captures.spec.ts` et pilote depuis `ecrans.ts` : un ecran peut decrire une interaction, pas seulement une URL.
- **Un garde-fou de contenu** : le test refuse de photographier un panneau dont les elements attendus ne sont pas visibles. Une reference d'entete vide ne peut plus etre figee par accident.
- **Un blocage reel trouve et corrige** : les sets modulaires etaient replies par defaut, la premiere photo de l'etape 2 n'en montrait aucun.

## Task Commits

1. **Tache 1 : Declarer les 3 panneaux caches et savoir les ouvrir** - `b48e5e7` (feat)
2. **Deviation trouvee en tache 2 : depliage des sets modulaires** - `80b66ca` (fix)
3. **Tache 2 : Generer et controler les 9 nouvelles references** - `0ec3f00` (test)

## Files Created/Modified

- `ui-check/ecrans.ts` - Type `Ecran` etendu de 3 champs optionnels (`etape`, `depliages`, `preuves`) et 3 entrees ajoutees apres `preparation`, avec le commentaire expliquant pourquoi elles existent. 9 ecrans au total.
- `ui-check/tests/captures.spec.ts` - Garde-fou 3 : ouverture du panneau via `page.evaluate(wizardShow)`, verification de la classe `on`, depliages, verification des preuves, attente du defilement `smooth`.
- `ui-check/references/preparation-rencontre/{pc,tablette,mobile}.png` - Sets standard (6 cartes) et sets modulaires deplies.
- `ui-check/references/preparation-heros/{pc,tablette,mobile}.png` - Bloc Heroes, 4 emplacements de deck, galerie de heros de depart.
- `ui-check/references/preparation-lancement/{pc,tablette,mobile}.png` - Game Start, Modes of Play, Rule, Challenges, Other, Reset to default, barre de lancement. Le champ Seed est masque en rose.

## Decisions Made

- **`window.wizardShow(i)` plutot qu'un clic sur `.w-step`.** Verifie dans le HTML servi (ligne 2228) : le gestionnaire de clic est garde par `if(t <= cur || canPass[cur]())`. Un clic sur l'etape 4 depuis l'etape 1 ne fait donc rien tant que le scenario et les heros ne sont pas choisis. `wizardShow` est expose globalement (ligne 2209) et bascule les classes `on` sans condition. Le message d'erreur du garde-fou nomme explicitement cette dependance, pour le jour ou `scene.html` cesserait d'exposer la fonction.
- **Preuves choisies dans le panneau, jamais dans l'entete.** `#encounter-sets button` et `#modular-sets button` (etape 2), `.w-step-panel[data-panel="2"] legend` (etape 3), `#play-buttons` et `#game-start` (etape 4). Toutes verifiees presentes dans le HTML reellement servi avant d'ecrire une ligne.
- **Le masque `#seed_div` est conserve sur les 3 nouveaux ecrans**, alors qu'il n'est reellement visible que sur l'etape 4 : c'est le meme filet que l'entree `preparation` d'origine, et il coute zero.
- **Les references sont nees d'une absence.** Playwright ecrit une reference manquante au premier passage et sort en echec ; le second passage est vert. Aucun appel a `--update-snapshots` : le controle `grep -rn "update-snapshots" ui-check/` ne remonte toujours que `scripts/valider.mjs`.
- **Titres sans accent** (`Preparation ancienne - etape 2 Rencontre`) : ils servent de noms de tests Playwright, donc de noms de dossiers dans `test-results/`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Depliage des sets modulaires avant la photo de l'etape 2**

- **Found during:** Tache 2, au controle du CONTENU de `references/preparation-rencontre/pc.png`
- **Issue:** Le plan exigeait que la photo montre « les sets de rencontre **et** les sets modulaires ». Elle ne montrait que les sets de rencontre. Cause mesuree : `#modular-sets` porte la classe `hide-not-click` au chargement, et la regle en ligne de `scene.html` (ligne 132) masque tout bouton `:not(.click)`. Aucun set n'etant selectionne, la zone etait vide. Or `wizard.css` consacre l'essentiel de ses regles de ce panneau a `#modular-sets button` et `#modular-sets img` (lignes 130, 143, 253, 262, 264, 270, 302, 311, 313, 316, 320) : la purge de la phase serait passee a cote.
- **Fix:** Champ optionnel `depliages?: string[]` sur le type `Ecran` (boutons a cliquer avant la photo), boucle de clics dans `captures.spec.ts` entre l'ouverture de l'etape et la verification des preuves. Le bouton est vise par `button[onclick*="hide-not-click"]`, c'est-a-dire par son comportement et non par son libelle « Expand », qui pourrait etre traduit. Preuves renforcees en consequence : `#encounter-sets button` et `#modular-sets button`.
- **Files modified:** `ui-check/ecrans.ts`, `ui-check/tests/captures.spec.ts`
- **Verification:** Les 3 references `preparation-rencontre` regenerees montrent une trentaine de sets modulaires ; `npm run captures` vert deux fois de suite, donc la liste est deterministe.
- **Commit:** `80b66ca`

---

**Total deviations:** 1 auto-corrigee (1 fonctionnalite critique manquante)
**Impact on plan:** La correction sert le critere d'acceptation du plan lui-meme (« la photo montre reellement le contenu du panneau »). Elle ajoute un champ optionnel, sans toucher aux garde-fous existants ni au mode demonstration. Aucun elargissement de perimetre.

## Issues Encountered

Aucun. Le panneau 3 (Heros) affiche sa galerie de heros de depart sans intervention : le meme doute que pour les sets modulaires a ete leve par lecture de l'image, pas par supposition.

## User Setup Required

Aucune configuration externe.

## Next Phase Readiness

**Pret pour la purge des `!important`.** Les 4 panneaux de l'ancienne preparation sont sous surveillance, dans les 3 gabarits. Une modification de `wizard.css` qui casserait un panneau masque devient detectable par `npm run captures`.

Points de vigilance a transmettre :

- **Le harnais depend maintenant de deux details internes de `scene.html`** : `window.wizardShow` doit rester expose, et le bouton de depliage des sets modulaires doit garder un `onclick` contenant `hide-not-click`. Les deux ont un message d'erreur en francais qui le dit. Le jour ou `scene.html` sera remplace (phase 5), ces 3 ecrans devront etre revus ou retires.
- **Les sets modulaires sont dans un conteneur a defilement** (`max-height:44vh; overflow-y:auto`) : la photo n'en montre que la premiere partie. C'est deterministe et suffisant pour detecter un changement de style de tuile, mais ce n'est pas un inventaire exhaustif.
- **Le principe est generalisable** : tout contenu replie par defaut echappe a la surveillance. `scene.html` en contient d'autres (les `<details>` `#rules` et `#challenge` de l'etape 4 sont fermes). Si la purge touche leurs styles internes, il faudra les ajouter aux `depliages`.
- **La regle du plan 01-02 reste intacte** : `captures:valider` demeure le seul chemin volontaire vers `references/`, `grep -rn "update-snapshots" ui-check/` ne remonte que `scripts/valider.mjs`.

---
*Phase: 02-fondations-design-system*
*Completed: 2026-07-28*
