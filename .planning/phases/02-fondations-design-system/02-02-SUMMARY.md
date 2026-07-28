---
phase: 02-fondations-design-system
plan: 02
subsystem: infra
tags: [vite, react, typescript, rolldown, build, css-layers, tokens]

# Dependency graph
requires:
  - phase: 01-filet-de-securite
    provides: contraintes d'environnement mesurees (Node Windows, npm via cmd.exe, routage serveur par extension)
provides:
  - Projet ui-app/ avec React 19.2.8 + TypeScript 6.0.3 + Vite 8.1.5
  - Build multi-pages vitrine.html -> dist/ avec base /app/
  - Garde-fou d'extensions verifier-sortie.mjs (liste blanche .html/.js/.css)
  - styles/tokens.css, source unique des tokens avec la declaration d'ordre des couches
affects: [02-03 deploiement, 02-05 branchement tokens sur pages anciennes, 02-06 tokenisation, 02-09 contenu de la vitrine, phase 3 ecrans pilotes]

# Tech tracking
tech-stack:
  added: [react@19.2.8, react-dom@19.2.8, vite@8.1.5, typescript@6.0.3, "@vitejs/plugin-react@6.0.4", vite-plugin-checker@0.14.5, "@types/react@19", "@types/react-dom@19"]
  patterns:
    - "Build multi-pages Vite avec entrees HTML a la racine du projet (sortie plate)"
    - "assetsInlineLimit force a true : aucun asset binaire ne peut sortir du build"
    - "Garde-fou d'extensions execute apres chaque build, avant tout deploiement"
    - "tokens.css : une source, deux destinations (bundle Vite + copie servie brute)"

key-files:
  created:
    - ui-app/package.json
    - ui-app/tsconfig.json
    - ui-app/.gitignore
    - ui-app/vite.config.ts
    - ui-app/vitrine.html
    - ui-app/src/vitrine.tsx
    - ui-app/styles/tokens.css
    - ui-app/outils/verifier-sortie.mjs
  modified: []

key-decisions:
  - "TypeScript 6.0.3 et jamais 7.x : la 7 est latest sur npm mais expediee sans API compilateur publique"
  - "vite-plugin-checker retenu : il s'installe sans conflit de peer avec Vite 8, le repli par script typecheck enchaine n'a pas ete necessaire"
  - "build.rolldownOptions (Vite 8) et non build.rollupOptions : aucun avertissement de depreciation au build"
  - "Le garde-fou echoue aussi sur dossier absent ou vide : un build qui ne produit rien ne doit pas passer au vert"
  - "Pas d'aiguillage ui-switch.js sur vitrine.html : cette page n'a pas d'ancienne version"

patterns-established:
  - "Chaque script npm reste une commande unique (npm passe par cmd.exe depuis WSL)"
  - "Le build ecrit dans ui-app/dist (chemin Windows natif), jamais dans l'arborescence WSL du jeu"
  - "Ordre des couches CSS declare une seule fois, en tete de tokens.css : socle, legacy, base, composants, utilitaires"

# Metrics
duration: 4 min
completed: 2026-07-28
---

# Phase 2 Plan 02 : Chaine de build de la nouvelle UI - Summary

**Projet `ui-app/` en React 19.2.8 + TypeScript 6.0.3 + Vite 8.1.5, build multi-pages sous `base: '/app/'` qui ne peut produire que du `.html`, du `.js` et du `.css`, prouve par un garde-fou d'extensions teste sur un vrai intrus.**

## Performance

- **Duration:** 4 min
- **Started:** 2026-07-28T14:04:13Z
- **Completed:** 2026-07-28T14:08:30Z
- **Tasks:** 3
- **Files created:** 9 (dont `package-lock.json`)

## Accomplishments

- `npm run build` construit `dist/vitrine.html` + un `.js` et un `.css` haches, en 1 s, sans le moindre avertissement de depreciation sur `rollupOptions`.
- Les chemins d'assets ecrits dans le HTML construit commencent bien par `/app/` : `/app/assets/vitrine-B0-ceB0o.js` et `/app/assets/vitrine-fnoB9GLi.css`. C'est exactement ce que le serveur Python sait router.
- **Une erreur de type arrete reellement le build** : verifie en injectant `const faux: number = "texte"` dans `src/vitrine.tsx`. Le build sort en code 2 avec `error TS2322`, ligne et colonne. Le fichier a ete restaure ensuite. Sans cette verification active, `vite-plugin-checker` aurait pu etre present mais inerte.
- Le garde-fou `verifier-sortie.mjs` accepte le build reel (3 fichiers) et **refuse un `.png` glisse dans `dist/assets/`**, avec un message francais qui explique que le serveur repondrait 200 + une image vide de 2035 octets.
- `styles/tokens.css` pose la declaration d'ordre `@layer socle, legacy, base, composants, utilitaires;` avant toute utilisation de couche, et trois tokens prefixes `--mc-`. C'est la source unique que le plan 02-05 branchera sur les pages anciennes.

## Task Commits

1. **Tache 1 : creer le projet ui-app et installer la pile exacte** - `cedf1a0` (chore)
2. **Tache 2 : configurer Vite et ecrire la page vitrine minimale** - `53ed8ed` (feat)
3. **Tache 3 : le garde-fou d'extensions** - `49304bf` (feat)

## Files Created/Modified

- `ui-app/package.json` - `private`, `type: module`, 3 scripts en une commande chacun (`build`, `typecheck`, `verifier-sortie`)
- `ui-app/package-lock.json` - versions figees de la pile
- `ui-app/tsconfig.json` - strict, `jsx: react-jsx`, `moduleResolution: bundler`, `allowJs` (pour le futur `aspects.js` partage), `types: ["vite/client"]`
- `ui-app/.gitignore` - `node_modules/`, `dist/`
- `ui-app/vite.config.ts` - `base: '/app/'`, `rolldownOptions.input.vitrine`, `assetsInlineLimit: () => true`, `sourcemap: false`, plugins React + checker
- `ui-app/vitrine.html` - entree multi-pages a la racine, `<div id="vitrine">`, script module vers `/src/vitrine.tsx`
- `ui-app/src/vitrine.tsx` - montage React 19 dans `#vitrine`, affiche la version de React, importe `tokens.css`
- `ui-app/styles/tokens.css` - declaration d'ordre des couches + `--mc-fond`, `--mc-texte`, `--mc-espace-3`
- `ui-app/outils/verifier-sortie.mjs` - parcours recursif de `dist/`, liste blanche `.html`/`.js`/`.css`, `exit 1` sur intrus

## Decisions Made

- **`vite-plugin-checker@0.14.5` conserve.** Le plan prevoyait un repli (script `typecheck` appele avant le build dans `deployer.sh`) au cas ou le peer refuserait Vite 8. L'installation est passee sans conflit et le plugin fait effectivement echouer le build sur erreur de type : le repli n'est pas necessaire. Le script `typecheck` existe quand meme, comme controle independant.
- **Le garde-fou refuse aussi un dossier de sortie absent ou vide.** Un `dist/` vide passerait la liste blanche pour de mauvaises raisons : zero intrus parce que zero fichier. Deux messages d'erreur distincts couvrent ces cas.
- **Le garde-fou accepte un dossier en argument** (`node outils/verifier-sortie.mjs [dossier]`, defaut `dist`). Ca permettra au plan 02-03 de controler aussi la copie deployee si besoin, sans dupliquer le script.
- **`vitrine.html` reste volontairement pauvre.** Titre, une phrase qui dit ce qu'est cette page, la version de React. Le contenu du design system arrive au plan 02-09 : la roadmap met en garde contre le « design system first » paralysant.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Garde-fou aveugle sur un `dist/` absent ou vide**

- **Found during:** Tache 3
- **Issue:** Le modele de la recherche parcourt `dist/` sans verifier son existence. Sur dossier absent, `readdirSync` leve une exception Node en anglais avec une trace ; sur dossier vide, le script affiche « Sortie conforme : 0 fichiers » et sort en 0 — un build casse serait declare conforme.
- **Fix:** Deux controles explicites avant le filtrage, chacun avec un message francais et `exit 1`.
- **Files modified:** `ui-app/outils/verifier-sortie.mjs`
- **Verification:** `node outils/verifier-sortie.mjs dossier-absent` sort en 1 avec « Dossier de sortie introuvable ».
- **Committed in:** `49304bf` (commit de la tache 3)

---

**Total deviations:** 1 auto-corrigee (1 fonctionnalite critique manquante)
**Impact on plan:** Aucune derive de perimetre. Le garde-fou est le seul rempart contre une panne silencieuse : il ne doit pas avoir lui-meme un angle mort.

## Issues Encountered

Aucun. Les trois pieges anticipes par la recherche ne se sont pas manifestes :

- `vite-plugin-checker` s'installe sans conflit de peer avec Vite 8 ;
- `rolldownOptions` est accepte sans avertissement (le build est muet sur ce point) ;
- `npm` depuis WSL sur le chemin `/mnt/c/...` fonctionne sans adaptation, y compris pour `npm run verifier-sortie` qui passe par `cmd.exe`.

Point a garder en tete pour le plan 02-03 : les chemins affiches par le garde-fou utilisent le separateur Windows (`dist\assets\faux.png`), puisque Node est le binaire Windows. C'est lisible, mais a ne pas confondre avec un chemin WSL dans un futur message d'erreur.

## User Setup Required

Aucun - aucune configuration de service externe.

## Next Phase Readiness

**Pret pour le plan 02-03** (`deployer.sh` : build + garde-fou + `rsync` vers `public/app/` + copie de `tokens.css` vers `public/css/`). Tout ce dont il a besoin existe : `npm run build`, `node outils/verifier-sortie.mjs`, `dist/` et `styles/tokens.css`.

Points de vigilance transmis :

- **`ui-app/dist/` est ignore par git** : la sortie de build n'est jamais versionnee, elle est reconstruite. Le deploiement doit donc toujours enchainer build puis recopie, jamais recopier un `dist/` suppose present.
- **Question ouverte 1 de la recherche desormais sans objet** : `vitrine.html` ne reference aucune URL absolue vers `tokens.css`, le CSS passe par le bundle. Le pari sur la reecriture des URL absolues par Vite n'a pas eu a etre pris.
- **Le contenu de la vitrine est un squelette** : la page ne montre encore ni palette, ni typo, ni pastilles d'aspect, ni bascule de theme. C'est le perimetre du plan 02-09, pas un manque de celui-ci.
- **`vitrine.html` devra etre ajoute a `ui-check/ecrans.ts`** avec le marqueur `#vitrine` quand la page sera servie (plan 02-03 ou 02-09), pour beneficier du garde-fou anti `clean_cache.html` et des captures.

---
*Phase: 02-fondations-design-system*
*Completed: 2026-07-28*
