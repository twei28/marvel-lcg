# Phase 2 : Fondations — stack et design system tokenisé - Research

**Researched:** 2026-07-28
**Domain:** build statique Vite/React servi par un serveur aiohttp à routage par extension + refonte de la cascade CSS d'un existant (tokens, `@layer`, purge des `!important`)
**Confidence:** HIGH sur les contraintes serveur et l'inventaire CSS (mesurés sur le serveur en cours d'exécution et sur les fichiers), HIGH sur les versions npm (registre interrogé le jour même), MEDIUM sur deux points de configuration Vite non tranchés par la doc (réécriture des URL absolues dans le HTML, transformation de `light-dark()` par Lightning CSS)

## Summary

Cette phase fait converger deux chantiers indépendants : **poser la chaîne de build** (React 19 + TS 6 + Vite 8 → `public/app/`) et **remettre la cascade CSS d'aplomb** (purge des `!important`, `@layer`, tokens partagés). Les deux se rejoignent sur un seul fichier : `tokens.css`, consommé par les pages anciennes servies brutes par Python et par la nouvelle page React.

Trois découvertes changent la façon de planifier. **Un** : le filet de sécurité actuel ne couvre PAS la purge. `scene.html` n'affiche que le panneau 1 du wizard au chargement ; sur les 105 déclarations `!important` de `wizard.css`, environ **45 visent des éléments situés dans les panneaux 2, 3 et 4, invisibles à la capture**. Purger sans étendre le harnais, c'est purger à l'aveugle. **Deux** : les tokens ne gagnent pas la cascade tout seuls. Une propriété personnalisée n'entre pas en concurrence avec `background-color: rgb(43,43,43)` écrit en dur : tant que les feuilles anciennes ne sont pas **réécrites pour consommer `var(--mc-…)`**, changer un token ne change rien. Le vrai travail du critère 2, c'est la substitution d'environ 200 valeurs codées en dur dans `menu/style.css`, `menu/wizard.css` et `prepare/prepare.css`. **Trois** : `build.rollupOptions` est **renommé `build.rolldownOptions`** en Vite 8, et le seul Node disponible est le binaire Windows — le build ne doit jamais écrire directement dans l'arborescence WSL du jeu.

Le routage serveur a été vérifié **en direct sur le serveur en cours** : `.html`, `.css`, `.js` sont servis depuis `public/app/` et ses sous-dossiers, sous `/app/…` comme sous `/public/app/…` ; une police `.woff` hachée par Vite tombe en 404 ; un `.png` haché renvoie **200 + image/jpeg de 2035 octets** (échec silencieux). La configuration du build doit donc garantir qu'il ne sort **que** du `.html`, du `.js` et du `.css`, et un contrôle automatique doit le prouver à chaque build.

**Primary recommendation :** projet Vite dans `ui-app/` (dépôt Desktop, chemin Windows natif), `base: '/app/'`, sortie locale dans `dist/` puis recopie par un script bash WSL vers `public/app/` ; séquence CSS strictement ordonnée **étendre les captures aux 4 panneaux du wizard → purger les 105 `!important` → poser `@layer socle, legacy, base, composants, utilitaires` → substituer les valeurs en dur par `var(--mc-…)`**, chaque étape validée par `npm run captures` sur photos.

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---|---|---|---|
| Vite | **8.1.5** | Build statique multi-pages | Stable depuis le 12/03/2026, unifié sur Rolldown. Le hachage de contenu supprime les `?v=N` manuels. Multi-entrées HTML = exactement le modèle que le serveur Python sait déjà servir. Node requis : `^20.19.0 \|\| >=22.12.0` (mesuré : v25.3.0 en place, ça passe). |
| React | **19.2.8** | Couche vue | Version courante du registre. Aucun besoin spécifique de 19.2 en phase 2 (pas d'`<Activity>`, pas de `useEffectEvent`) : c'est la version cible du projet, on la pose. |
| react-dom | **19.2.8** | Rendu DOM | Doit suivre react à l'identique. |
| TypeScript | **6.0.3** (surtout PAS 7.0.2) | Typage | 7.0.2 est `latest` mais expédié **sans API compilateur publique** : `typescript-eslint` en mode type-aware, ts-jest et ts-morph sont cassés. Vérifié le 2026-07-28 : le dist-tag `next` est `7.1.0-dev.20260728.1`, donc **7.1 n'est pas sorti** et l'API n'existe toujours pas. 6.0.3 est le dernier 6.x. |
| @vitejs/plugin-react | **6.0.4** | JSX + Fast Refresh | Peer `vite: ^8.0.0` **strict** (vérifié). Les peers `@rolldown/plugin-babel` et `babel-plugin-react-compiler` sont **optionnels** : ne pas les installer. |
| @types/react, @types/react-dom | **19.x** | Types React | Obligatoires avec React 19. |

### Supporting

| Library | Version | Purpose | When to Use |
|---|---|---|---|
| vite-plugin-checker | **0.14.5** | `tsc` en parallèle du build/dev | Sinon Vite transpile sans jamais type-checker. À poser dès le premier plan, sinon le typage est décoratif. |
| @axe-core/playwright | **4.12.1** | Vérification des contrastes sur page réelle (ACC-02) | S'ajoute au harnais `ui-check` existant. La règle `color-contrast` d'axe mesure le rendu réel, pas la théorie. |
| culori | **4.0.2** | Calcul de contraste WCAG à partir des valeurs de tokens | Pour le contrôle **déterministe** des paires de tokens, sans navigateur. Supporte oklch. Alternative plus légère : `wcag-contrast@3.0.0` (mais pas d'oklch). |
| stylelint | **17.14.1** | Interdire `!important` dans le CSS neuf | La règle `declaration-no-important` transforme la discipline en garde-fou automatique. Optionnel mais peu cher. |

**Ne PAS installer en phase 2 :** zustand, motion, @dnd-kit, @tanstack/react-query, lucide-react, zod, vitest. Aucun n'a de consommateur en phase 2 (page vitrine statique). Le projet a déjà documenté le piège « design-system-first paralysant » : pas de dépendance sans usage réel.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|---|---|---|
| CSS natif + custom properties | Tailwind CSS 4.3.x | Écarté pour ce projet (voir `.planning/research/STACK.md`) : les états combinatoires de carte se lisent mieux en `[data-etat~="…"]`, et le preflight Tailwind écraserait `menu/style.css`. Surtout : Tailwind ne peut pas alimenter les pages anciennes servies brutes, ce qui tue le critère 2. |
| `@import … layer(legacy)` | Envelopper chaque feuille ancienne dans `@layer legacy { … }` | L'`@import` évite d'éditer les feuilles mais ajoute une requête sérielle et rend l'ordre plus difficile à lire. **Recommandé : envelopper les fichiers**, ils nous appartiennent. |
| `light-dark()` | Deux blocs de tokens (`:root` / `:root[data-theme="dark"]`) | `light-dark()` est Baseline 2024 et élégant, mais il serait transformé par Lightning CSS côté build Vite et pas côté CSS ancien servi brut : deux comportements pour un même fichier. **Recommandé : deux blocs**, portable partout, zéro build. |
| Vite dev server + proxy | `vite build --watch` + recopie | Le critère 1 exige que la page soit servie **par le serveur Python**. `--watch` évite toute configuration de proxy et prouve le chemin réel à chaque sauvegarde. Le HMR n'a de valeur qu'à partir de la phase 3. |

**Installation :**

```bash
# depuis /mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app  (chemin Windows natif, obligatoire)
npm install react@19.2.8 react-dom@19.2.8
npm install -D vite@8.1.5 @vitejs/plugin-react@6.0.4 typescript@6.0.3
npm install -D @types/react@19 @types/react-dom@19 vite-plugin-checker@0.14.5

# dans ui-check (harnais existant) — pour ACC-02
npm install -D @axe-core/playwright@4.12.1 culori@4.0.2
```

## Architecture Patterns

### Recommended Project Structure

```
/mnt/c/Users/arnau/Desktop/Marvel LCG/     # dépôt git, chemin Windows natif
├── ui-check/                  # harnais Playwright (existant, phase 1)
└── ui-app/                    # NOUVEAU — sources de la nouvelle UI, jamais dans le livrable
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── vitrine.html           # entrée multi-pages n°1 (page de démonstration)
    ├── src/
    │   ├── vitrine.tsx        # point d'entrée React
    │   └── composants/        # plafonné : rien sans 2 usages réels
    ├── styles/
    │   └── tokens.css         # SOURCE UNIQUE des tokens (copiée vers le jeu au déploiement)
    ├── outils/
    │   ├── verifier-sortie.mjs   # garde-fou : seules .html/.js/.css sortent du build
    │   └── empreintes.mjs        # remplace les ?v=N des pages anciennes par une empreinte
    └── deployer.sh            # bash WSL : build + recopie vers l'arborescence du jeu
                               #   (jamais lancé par npm : npm passe par cmd.exe)

~/marvel-work/fusion/marvel-lcg-src/       # codebase VIVANT (WSL), servi par launcher_fast.py
└── public/
    ├── app/                   # SORTIE DE BUILD — contenu entièrement recréé à chaque déploiement
    │   ├── vitrine.html
    │   └── assets/index-<hash>.js|.css
    └── css/
        └── tokens.css         # COPIE de ui-app/styles/tokens.css, servie brute aux pages anciennes
```

**Pourquoi ce découpage :** le seul Node disponible est `node.exe` Windows (mesuré : `~/.local/bin/node` → `/mnt/c/Program Files/nodejs/node.exe`, aucun Node Linux). Il faut donc que `node_modules` et le `outDir` de Vite vivent sur un chemin Windows natif. Le franchissement WSL se fait par **une commande `rsync` en bash**, pas par Node.

### Pattern 1 : configuration Vite conforme à la liste blanche du serveur

**What:** un build multi-pages qui ne peut émettre que des extensions routées.
**When to use:** dès le premier plan de la phase.

```ts
// ui-app/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import checker from 'vite-plugin-checker'
import { resolve } from 'node:path'

export default defineConfig({
  // URL réelle servie par le serveur Python. VÉRIFIÉ en direct :
  //   GET /app/vitrine.html            -> ./public/app/vitrine.html
  //   GET /app/assets/index-<hash>.js  -> ./public/app/assets/index-<hash>.js
  base: '/app/',

  plugins: [react(), checker({ typescript: true })],

  build: {
    outDir: 'dist',        // LOCAL. La recopie vers le jeu est faite par deployer.sh.
    emptyOutDir: true,

    // Le serveur n'a AUCUNE route pour .png/.webp/.woff2/.json, et sa route .svg
    // ne lit que assets/textures/ à plat. On force donc l'inlining de tout
    // asset importé : rien d'autre que .html/.js/.css ne doit sortir.
    assetsInlineLimit: () => true,

    // .js.map renvoie 404 en mode RELEASE (les deux launchers posent RELEASE=1).
    sourcemap: false,

    // Vite 8 : rollupOptions est RENOMMÉ rolldownOptions (l'ancien nom est déprécié).
    rolldownOptions: {
      input: {
        vitrine: resolve(import.meta.dirname, 'vitrine.html'),
        // les écrans réels arrivent en phase 3 et suivantes
      },
    },
  },
})
```

**Points vérifiés :**
- `base: '/app/'` **et** `base: '/public/app/'` fonctionnent tous les deux (mesuré). `/app/` est plus court et cohérent avec `/prepare.html`.
- Vite ignore le nom donné à l'entrée et **respecte le chemin résolu du fichier HTML** pour placer la sortie. Poser les `.html` d'entrée à la racine de `ui-app/` garantit une sortie plate.
- `build.emptyOutDir` vaut `true` par défaut quand `outDir` est **dans** le root. C'est le cas ici, donc rien à forcer — et surtout aucun risque d'effacer un dossier du jeu.

### Pattern 2 : déploiement par bash, jamais par Node

**What:** franchir la frontière Windows/WSL avec l'outil qui sait le faire.
**When to use:** à chaque build.

```bash
#!/usr/bin/env bash
# ui-app/deployer.sh — à lancer depuis WSL.
set -euo pipefail

RACINE_APP="/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
JEU="$HOME/marvel-work/fusion/marvel-lcg-src"

cd "$RACINE_APP"
npm run build                        # npm passe par cmd.exe : UNE seule commande par script npm
node outils/verifier-sortie.mjs      # échoue si une extension hors liste blanche est sortie

# public/ est un SYMLINK sous launcher_fast.py : la copie est visible immédiatement,
# aucune relance de serveur, aucune partie perdue.
rsync -a --delete dist/ "$JEU/public/app/"

# tokens.css : une seule source, deux destinations.
cp styles/tokens.css "$JEU/public/css/tokens.css"

node outils/empreintes.mjs "$JEU/public"   # remplace les ?v=N par une empreinte de contenu
echo "Déployé. Recharge la page dans le navigateur."
```

**Pourquoi pas `npm run deploy` :** mesuré en phase 1, `npm` exécute ses scripts via `cmd.exe`. Ni `&&` ni `;` POSIX ne fonctionnent, et un script npm doit rester **une commande unique**. L'enchaînement vit donc dans un script bash WSL.

### Pattern 3 : garde-fou d'extensions à la sortie du build

**What:** transformer une contrainte serveur invisible en test rouge.
**When to use:** à chaque build, avant la recopie.

```js
// ui-app/outils/verifier-sortie.mjs
import { readdirSync, statSync } from 'node:fs'
import { join, extname } from 'node:path'

// Liste blanche RÉELLE du serveur, relevée dans web_server.py:258-277 et
// vérifiée en direct sur le serveur en cours. Tout le reste échoue :
//   .woff2 / .json / .png -> 200 + image/jpeg de 2035 octets (échec SILENCIEUX)
//   .svg / .woff hachés   -> 404
const AUTORISEES = new Set(['.html', '.js', '.css'])

function parcourir(dossier) {
  return readdirSync(dossier).flatMap((nom) => {
    const chemin = join(dossier, nom)
    return statSync(chemin).isDirectory() ? parcourir(chemin) : [chemin]
  })
}

const intrus = parcourir('dist').filter((f) => !AUTORISEES.has(extname(f).toLowerCase()))
if (intrus.length) {
  console.error(
    "Le build a produit des fichiers que le serveur du jeu ne sait pas servir :\n" +
    intrus.map((f) => '  - ' + f).join('\n') +
    "\nCes fichiers ne renverraient PAS d'erreur : le serveur répondrait une image vide.\n" +
    "Corrige la configuration Vite (assetsInlineLimit) ou sors ces fichiers du build."
  )
  process.exit(1)
}
console.log('Sortie conforme : ' + parcourir('dist').length + ' fichiers, extensions autorisées uniquement.')
```

### Pattern 4 : la séquence CSS obligatoire, étape par étape

L'ordre imposé par la roadmap est **captures → purge `!important` → `@layer` → tokens**. Il manque une étape zéro, révélée par la mesure.

**Étape 0 (NOUVELLE, indispensable) — étendre le filet aux panneaux cachés du wizard.**
`scene.html` contient 4 panneaux (`.w-step-panel[data-panel="0..3"]`), un seul porte la classe `on` au chargement. La référence actuelle `preparation/*.png` ne montre donc que le panneau 1.

Répartition mesurée des 105 déclarations `!important` de `wizard.css` :

| Cible | Déclarations | Couverte par la capture actuelle ? |
|---|---|---|
| Panneau 0 (Scénario) : `#set-images`, `#set-content`, `#w-splash` | 33 | oui |
| Génériques : `body`, `.w-step-panel`, `.w-step-h`, `fieldset`, `details` | 27 | partiellement |
| Panneau 1 (Rencontre) : `#modular-sets`, `#encounter-sets` | ~21 | **non** |
| Panneau 2 (Héros) : `#starter-gallery`, `img[id^=img-heroes]`, `input[type=file]` | ~9 | **non** |
| Panneau 3 (Lancement) : `#play-buttons`, `#game-start`, `#clearCacheButton`, `#mode`, `#rules`, `#challenge`, `#settings_other` | 16 | **non** |

**Environ 45 déclarations sur 105 sont hors champ.** Avant toute purge, ajouter au harnais un test qui capture `scene.html` panneau par panneau (clic sur `.w-step[data-step="N"]`, ou `page.evaluate` sur `wizardGo`), soit 4 références supplémentaires par gabarit. Sans ça, « aucune régression visuelle » est une affirmation invérifiable.

**Étape 1 — purge des `!important` de `wizard.css`.**
Ce que la mesure dit de l'origine du problème : `scene.html` charge `menu/style.css`, puis `font-awesome.css`, puis `menu/wizard.css`, **puis 9 blocs `<style>` en ligne** (370 lignes, 66 règles). `wizard.css` gagne naturellement contre `style.css` par ordre de source ; ses `!important` servent presque uniquement à battre les blocs en ligne qui viennent **après** lui. Purger consiste donc à :

1. retirer **toutes** les `!important` de `wizard.css` (105 déclarations, 67 lignes) ;
2. relancer `npm run captures` (les 4 panneaux × 3 gabarits) ;
3. pour chaque régression, corriger par **ordre de source ou spécificité**, jamais par un `!important` réintroduit. Le levier le plus efficace : déplacer les blocs `<style>` en ligne de `scene.html` dans `@layer legacy` à l'étape suivante, ce qui les fait perdre face à tout ce qui est layered.

Le seuil du harnais est `maxDiffPixelRatio: 0.002` (0,2 %) : un décalage de 1 px sur un badge se voit, l'anticrénelage non.

**Étape 2 — poser `@layer`.**

```css
/* public/css/tokens.css — PREMIER <link> de chaque page, ancienne comme nouvelle. */

/* La déclaration d'ordre doit être vue AVANT toute utilisation de couche.
   Elle a le droit de précéder un @import (seuls @charset et @layer le peuvent). */
@layer socle, legacy, base, composants, utilitaires;

@layer socle {
  :root {
    color-scheme: light;
    /* … les tokens … */
  }
}
```

Puis envelopper chaque feuille ancienne :

```css
/* public/css/menu/wizard.css */
@font-face { /* … reste HORS couche, par prudence … */ }

@layer legacy {
  /* tout le contenu existant, sans un seul !important */
}
```

Et les 9 blocs `<style>` de `scene.html`, et les blocs de `prepare.html` / `cards.html` le jour où on y touche.

**Règles de cascade à ne pas se tromper** (source : MDN `@layer`, vérifié) :
- déclarations normales : **le non-layered bat tout le layered** ; entre couches, la **dernière** déclarée gagne ;
- déclarations `!important` : **l'ordre est inversé** — la **première** couche gagne, et une couche `!important` bat un `!important` non-layered.

Conséquence directe, c'est le piège documenté : mettre `wizard.css` dans `legacy` (la couche la plus basse) **sans purger** rendrait ses 105 `!important` plus forts que les `!important` des couches supérieures. La purge est un **prérequis**, pas une amélioration ultérieure.

**Choix d'ordre recommandé : `socle, legacy, base, composants, utilitaires`.**
`socle` en premier plutôt qu'après `legacy` parce que les tokens n'ont pas vocation à gagner un conflit : ils définissent des variables que `legacy` consomme. Et pour éliminer tout risque de collision, **préfixer tous les tokens neufs `--mc-`** : les feuilles anciennes définissent déjà `--card--width`, `--font-size`, `--color`, `--z-index-*` (relevé : 34 `--color`, 23 `--y`, 15 `--text-shadow-color`, 9 `--font-size`…). Aucun nom neuf ne doit croiser un nom ancien.

**Étape 3 — tokens : c'est une substitution, pas un ajout.**
Le piège le plus coûteux du critère 2 : **ajouter `tokens.css` ne change rien tant que les feuilles anciennes gardent leurs valeurs codées en dur**. Une propriété personnalisée n'entre pas en concurrence avec `background-color: rgb(43,43,43)`.

Volume mesuré de valeurs de couleur en dur :

| Fichier | Couleurs en dur | Portée |
|---|---|---|
| `css/menu/wizard.css` | 83 | scene.html (ancienne préparation) |
| `css/prepare/prepare.css` | 77 | prepare.html (nouvelle préparation) |
| `css/menu/style.css` | 34 | scene.html, cards.html, deck.html… |
| `css/menu/preview.css` | 6 | |
| `css/marvel/*` (60 fichiers) | 250 | plateau — **hors périmètre phase 2** |

Périmètre recommandé pour la phase 2 : les 200 valeurs de `menu/` + `prepare/`. Le plateau attend la phase 5.

### Pattern 5 : thème sombre par bascule de tokens

**What:** deux blocs de tokens, un attribut sur `<html>`, zéro composant touché.
**When to use:** critère 3.

```css
/* public/css/tokens.css */
@layer socle {
  :root {
    color-scheme: light;
    --mc-fond: #f4f5f7;
    --mc-texte: #16181d;
    --mc-panneau: #ffffff;
  }

  /* Préférence système, sauf choix explicite contraire. */
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      color-scheme: dark;
      --mc-fond: #0b0c10;
      --mc-texte: #e7eaf0;
      --mc-panneau: #171a22;
    }
  }

  /* Choix explicite de l'utilisateur, gagne toujours. */
  :root[data-theme="dark"] {
    color-scheme: dark;
    --mc-fond: #0b0c10;
    --mc-texte: #e7eaf0;
    --mc-panneau: #171a22;
  }
}
```

La bascule se pose sur `document.documentElement.dataset.theme`, mémorisée dans **`localStorage`**, en réutilisant le vocabulaire déjà en place (clé `ui` pour la bascule ancienne/nouvelle → clé `theme` ici). Jamais un cookie : le serveur en pose déjà deux (`session_token`, `app_version`).

Deux blocs plutôt que `light-dark()` : le même `tokens.css` est servi **brut** par Python aux pages anciennes et passe **par Lightning CSS** s'il est importé par Vite. Deux chemins de transformation pour un fichier, c'est une source de divergence gratuite.

### Pattern 6 : identité des aspects sans la couleur (ACC-01)

État des lieux mesuré — il y a aujourd'hui **trois palettes d'aspects divergentes** :

| Source | Aggression | Justice | Leadership | Protection |
|---|---|---|---|---|
| `js/prepare/app.js` (const `ASPECTS`) | `#d1403a` | `#e3b23c` | `#3d7bd6` | `#3fae67` |
| `cards.html` (attributs `style=` en ligne) | `rgb(237,51,51)` | `rgb(255,219,35)` | `rgb(66,164,236)` | `rgb(84,255,149)` |
| `wizard.css` (`--w-red`, `--w-gold`, `--w-green`) | `#e62429` | `#f2a900` | — | `#37b24d` |

Et **une seule violation franche d'ACC-01** : `aspectBar()` dans `js/prepare/app.js` rend des segments `background: ASPECTS[a]` avec l'aspect uniquement dans un attribut `title` — invisible au doigt, invisible au clavier, invisible en niveaux de gris. `cards.html` a déjà couleur + libellé, il lui manque l'icône (et ses contrastes sont mauvais : texte sur `rgb(84,255,149)` et `rgb(255,219,35)`).

**Il n'existe aucun glyphe d'aspect dans les ressources du jeu.** `ChampionsIcons.ttf` (déclarée `font-family:'marvel-icons'` dans `css/marvel/marvel.css:74`) ne couvre que les ressources et statuts : `energy`, `mental`, `physical`, `wild`, `boost`, `hazard`, `acceleration`, `crisis`, `amplify`, `per_hero`, `unique`, `cost`. Les icônes d'aspect sont donc **à créer**.

**Recommandation : un module ES unique, `public/js/aspects.js`**, source de vérité partagée :

```js
// public/js/aspects.js — servi brut aux pages anciennes ET importé par la nouvelle UI.
// .js est dans la liste blanche du serveur ; .json ne l'est PAS (200 + image JPEG).
export const ASPECTS = {
  aggression:  { libelle: 'Agression',   token: '--mc-aspect-agression',   svg: '<svg …>' },
  justice:     { libelle: 'Justice',     token: '--mc-aspect-justice',     svg: '<svg …>' },
  leadership:  { libelle: 'Commandement',token: '--mc-aspect-commandement',svg: '<svg …>' },
  protection:  { libelle: 'Protection',  token: '--mc-aspect-protection',  svg: '<svg …>' },
  basic:       { libelle: 'Base',        token: '--mc-aspect-base',        svg: '<svg …>' },
  pool:        { libelle: 'Pool',        token: '--mc-aspect-pool',        svg: '<svg …>' },
}
```

SVG **en ligne dans le module**, pas en fichiers `.svg` : la route `handle_svg` ne lit que `assets/textures/` à plat, un `.svg` haché sortant du build tombe en 404 (mesuré). Un fichier posé à la main dans `assets/textures/` marche (mesuré : `/t-a1b2.svg` → 200), mais le module `.js` évite d'avoir deux mécanismes.

Ce module suit exactement la convention établie en phase 1 pour les fixtures (« les fixtures sont des modules `.js` et jamais `.json` »).

### Pattern 7 : contrastes vérifiés (ACC-02)

Le critère parle de « seuil défini par les tokens ». Deux niveaux de vérification, complémentaires :

1. **Contrôle déterministe des paires de tokens** (rapide, sans navigateur) : un script lit `tokens.css`, extrait les paires déclarées (`--mc-texte` sur `--mc-fond`, `--mc-texte-regles` sur `--mc-panneau`, compteurs…) et calcule le ratio WCAG 2.2 avec `culori`. Seuils : **4,5:1** pour le texte de règles, **3:1** pour le gros texte et les composants d'interface (compteurs, bordures d'état). Le fichier de tokens déclare lui-même ses paires, en commentaire structuré ou dans un `paires.js` voisin.
2. **Contrôle sur page réelle** : `@axe-core/playwright` sur la page vitrine, règle `color-contrast`, en plus des captures. Il attrape ce que le calcul théorique rate (superpositions, dégradés, transparences — et `wizard.css` en est plein : `rgba(11,12,16,.85)`, `backdrop-filter: blur(14px)`).

Ne pas coder la formule de contraste à la main : la relative luminance WCAG a des seuils de linéarisation exacts que tout le monde rate.

### Anti-Patterns to Avoid

- **Poser `@layer` avant d'avoir purgé les `!important`** : l'ordre des couches s'inverse pour les `!important`, les 105 de `wizard.css` deviendraient les plus forts du document. Le symptôme « c'est pire qu'avant » est attendu et démoralisant — d'où l'ordre imposé.
- **Ajouter `tokens.css` sans réécrire les valeurs en dur** : le critère 2 resterait faux tout en donnant l'illusion d'être fait.
- **Faire écrire Node dans l'arborescence WSL du jeu** (`outDir` en `//wsl.localhost/…`) : lent, fragile, et `emptyOutDir` sur un chemin UNC est une mauvaise idée. Passer par `rsync` en bash.
- **Émettre un `.svg`, un `.woff2`, un `.png` ou un `.json` depuis le build** : `.svg` et `.woff` → 404, `.woff2`/`.png`/`.json` → **200 avec une image JPEG**. Aucune erreur console dans le second cas.
- **Réintroduire un `!important` pour régler une régression de purge** : c'est exactement le mécanisme qui a produit l'état actuel.
- **Créer des composants React « au cas où »** : la roadmap place les écrans pilotes en phase 3. La page vitrine de la phase 2 est une preuve de chaîne, pas un design system.
- **Nommer un token neuf comme un ancien** (`--font-size`, `--color`, `--card--width`) : collision silencieuse avec `menu/style.css` et `css/marvel/*`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Cache-busting des assets | Incrémenter `?v=N` à la main | Hachage de contenu Vite (nouveau) + script d'empreinte (ancien) | Mesuré : 5 occurrences réelles de `?v=N`, déjà désynchronisées entre `prepare.html` (`?v=18`) et les imports internes de `app.js` (`?v=9`, `?v=5`). C'est le bug que le critère 5 vise. |
| Calcul de contraste WCAG | Formule de luminance maison | `culori@4.0.2` (calcul) + `@axe-core/playwright@4.12.1` (page réelle) | Les seuils de linéarisation sRGB et le traitement des couleurs semi-transparentes sont des pièges classiques. |
| Détection du thème système | `matchMedia` + réécriture de styles en JS | `prefers-color-scheme` + `color-scheme` + `[data-theme]` | Zéro JS, zéro flash au chargement, et `color-scheme` corrige aussi les widgets natifs (scrollbars, `<select>`, champs). |
| Vérification de non-régression visuelle | Comparaison d'images maison | `ui-check` existant (`npm run captures`, `npm run captures:comparer`, `npm run captures:valider`) | Le harnais est là, en français, avec validation sur photos. La phase 2 l'**étend** (panneaux du wizard, page vitrine), elle ne le double pas. |
| Type-check pendant le build | Enchaîner `tsc && vite build` à la main | `vite-plugin-checker@0.14.5` | `npm` passe par `cmd.exe` : un script npm doit rester une commande unique. Le plugin évite l'enchaînement. |
| Copie Windows ↔ WSL | `fs.cp` en Node sur chemin UNC | `rsync -a --delete` en bash WSL | Node est le binaire Windows ; `rsync` connaît les deux mondes et gère la suppression des fichiers obsolètes. |

**Key insight :** tout ce qui touche au franchissement Windows/WSL et à la liste blanche d'extensions échoue **silencieusement**. Chaque garde-fou doit produire un message d'erreur en français, pas un comportement dégradé.

## Common Pitfalls

### Pitfall 1 : le filet de sécurité ne couvre pas 45 % des `!important` à purger

**Ce qui se passe :** `scene.html` n'affiche que le panneau 1 du wizard au chargement (`.w-step-panel{display:none}`, seul `data-panel="0"` porte `.on`). La référence `preparation/*.png` ne voit ni `#modular-sets`, ni `#starter-gallery`, ni `#play-buttons`, ni `#mode/#rules/#challenge`.
**Mesuré :** 105 déclarations `!important` dans `wizard.css`, dont ~33 sur le panneau 0, ~27 génériques, et **~45 sur les panneaux 1 à 3, invisibles**.
**Comment l'éviter :** avant toute purge, ajouter un test Playwright qui ouvre chaque panneau (`.w-step[data-step="N"]`) et capture. 4 références de plus par gabarit, soit 12. C'est le premier plan de la phase.
**Signes d'alerte :** `npm run captures` vert après une purge massive, sans une seule différence — c'est trop beau.

### Pitfall 2 : extension hors liste blanche = 200 OK avec une image vide

**Ce qui se passe :** `web_server.py` enregistre des routes par extension, puis `server_files.py:37` pose un fourre-tout `/{path:.+}` → `Cache.LoadImage(basename)` → image « no image » générée.
**Mesuré en direct sur le serveur en cours :**

| Requête | Résultat |
|---|---|
| `/app/assets/i-a1b2.js` | 200 `application/javascript` ✅ |
| `/app/assets/i-a1b2.css` | 200 `text/css` ✅ |
| `/app/vitrine.html` | 200 `text/html` ✅ |
| `/public/app/assets/f-a1b2.woff` | **404** (route `.woff` = `public/fonts/` à plat) |
| `/public/app/assets/t-a1b2.svg` | **404** (route `.svg` = `assets/textures/` à plat) |
| `/public/app/assets/logo-a1b2.png` | **200 `image/jpeg`, 2035 octets** ← échec silencieux |
| `/public/app/x.json` | **200 `image/jpeg`, 2035 octets** ← échec silencieux |
| `/app/test.woff2` | **200 `image/jpeg`, 2035 octets** ← échec silencieux |

**Nuance utile :** une police ou un SVG haché **fonctionne** si un fichier du même nom de base existe dans `public/fonts/` ou `assets/textures/` (vérifié : `/public/app/assets/f-a1b2.woff` → 200 après dépôt de `public/fonts/f-a1b2.woff`). C'est une porte de sortie, pas une architecture : elle polluerait ces dossiers à chaque build.
**Comment l'éviter :** `assetsInlineLimit: () => true` + le garde-fou `verifier-sortie.mjs` (Pattern 3). Polices : rester sur les `.ttf` existantes de `public/fonts/`, référencées en URL absolue — Vite ne touche pas aux `url()` absolues.
**Effet de bord :** `Cache.LoadImage` met le placeholder en cache **mémoire** sous le nom de base. Une fois l'erreur commise, le serveur continue de renvoyer le placeholder jusqu'à sa relance, même après correction.

### Pitfall 3 : `build.rollupOptions` n'existe plus sous ce nom en Vite 8

**Ce qui se passe :** Vite 8 unifie tout sur Rolldown. Le guide de migration officiel liste `build.rollupOptions: renamed to build.rolldownOptions`, parmi les options dépréciées « qui seront retirées à l'avenir ». Tout exemple multi-pages antérieur à mars 2026 (et `.planning/research/STACK.md` lui-même) utilise l'ancien nom.
**Comment l'éviter :** écrire `build.rolldownOptions.input`. Vérifier au premier build qu'aucun avertissement de dépréciation ne sort.
**Autre changement de version à connaître :** la cible par défaut passe à Chrome 111 / Edge 111 / Firefox 114 / Safari 16.4 (« Baseline Widely Available au 2026-01-01 »).

### Pitfall 4 : Node est Windows, le jeu est en WSL

**Ce qui se passe :** `~/.local/bin/node` est un lien vers `/mnt/c/Program Files/nodejs/node.exe` ; il n'existe **aucun Node natif Linux** (vérifié : `which -a node` ne remonte que ce lien). Depuis un dossier WSL, `process.cwd()` est un chemin UNC `\\wsl.localhost\…`.
**Comment l'éviter :** `ui-app/` sous `/mnt/c/Users/arnau/Desktop/Marvel LCG/` comme `ui-check/`, `outDir` local, franchissement par `rsync` en bash. Ne jamais pointer `outDir` sur l'arborescence du jeu.
**Rappel npm :** les scripts npm passent par `cmd.exe` → une seule commande par script, pas de `&&`, pas de variable d'environnement en préfixe sans `WSLENV`.

### Pitfall 5 : les tokens ne gagnent pas la cascade tout seuls

**Ce qui se passe :** on ajoute `tokens.css`, on modifie `--mc-fond`, et rien ne bouge sur les écrans anciens — parce que `menu/style.css` dit `background-color: rgb(43, 43, 43)` en dur. Une custom property n'est pas une déclaration concurrente.
**Mesuré :** 200 valeurs de couleur en dur dans `menu/` + `prepare/` (dont 83 dans `wizard.css`), 250 de plus dans `css/marvel/`.
**Comment l'éviter :** le plan « tokens » n'est pas « créer tokens.css », c'est « **substituer** les valeurs en dur par `var(--mc-…)` dans les feuilles du périmètre ». Vérification directe du critère 2 : changer une seule valeur dans `tokens.css`, relancer `npm run captures`, constater que `preparation`, `preparation-nouvelle` **et** `vitrine` bougent ensemble.

### Pitfall 6 : `@layer` ne protège pas des blocs `<style>` en ligne

**Ce qui se passe :** MDN est formel — « les styles qui ne sont pas définis dans une couche écrasent toujours les styles déclarés dans des couches ». `scene.html` porte **9 blocs `<style>` (370 lignes, 66 règles)** après le `<link>` de `wizard.css`. Tant qu'ils restent hors couche, ils battent `socle`, `base`, `composants` et `utilitaires`.
**Comment l'éviter :** envelopper ces blocs dans `@layer legacy { … }` dans le même plan que la pose des couches. Même chose pour le bloc en ligne de `cards.html` (qui contient d'ailleurs le seul autre `!important` du dossier : `background-color: black !important`).

### Pitfall 7 : l'ordre de chargement décide de l'ordre des couches

**Ce qui se passe :** l'ordre des couches est fixé par la **première** déclaration `@layer` rencontrée dans le document. Si une page charge `menu/style.css` (qui contient `@layer legacy { … }`) avant `tokens.css` (qui contient `@layer socle, legacy, …;`), l'ordre devient `legacy, socle, …` — l'inverse de l'intention.
**Comment l'éviter :** `<link rel="stylesheet" href="/public/css/tokens.css">` en **tout premier** dans le `<head>` de chaque page concernée, ancienne et nouvelle. À vérifier par grep sur les pages du périmètre.
**Bon à savoir :** une instruction `@layer` a le droit de précéder un `@import` — seuls `@charset` et `@layer` en ont le droit (MDN `@import`, vérifié).

### Pitfall 8 : le contrôle de version peut renvoyer `clean_cache.html` en 200

**Ce qui se passe :** `IsVersionMatch` sert `clean_cache.html` (statut **200**) quand le cookie `app_version` est absent ou obsolète. `launcher_fast.py` désactive ce contrôle (mesuré : requête sans cookie → 200 sur le vrai CSS), **`launcher.py` non**.
**Conséquence pour la phase 2 :** la nouvelle page vitrine doit être ajoutée à `ecrans.ts` avec un **marqueur** propre (un `#id` du composant React), comme les 6 écrans existants. Le garde-fou par le titre « Version Mismatch » reste actif.
**Effet secondaire :** ce mécanisme est **redondant mais inoffensif** face au hachage Vite. Ne pas chercher à le supprimer : ce serait toucher au backend.

### Pitfall 9 : `?v=N` — le serveur ignore la query string

**Ce qui se passe :** les routes par extension ne lisent que `request.path` ; `?v=18` n'a aucun effet côté serveur, c'est purement une clé de cache navigateur. En mode RELEASE (posé par les deux launchers), chaque fichier part avec `Cache-Control: public, max-age=60` (`cache_max_age: 60` dans `launch.json`).
**Inventaire mesuré :** 5 occurrences réelles — `prepare.html` (`prepare.css?v=18`, `app.js?v=18`), `js/prepare/app.js` (`api.js?v=9`, `launcher.js?v=5`), `scene.html` (`wizard.css?v=9`). Les 7 autres occurrences sont des commentaires dans `font-awesome.css`.
**Comment satisfaire le critère 5 :**
- pages neuves : le hachage de contenu Vite suffit, plus aucun `?v=` ;
- pages anciennes : un script `empreintes.mjs` qui remplace chaque `?v=…` par les 8 premiers caractères du SHA-256 du fichier référencé, dans les `.html` **et** dans les spécificateurs d'import des `.js` (2 des 5 occurrences y sont). Lancé à chaque déploiement.
**Ne pas faire :** modifier `cache_max_age` dans `launch.json`. Ça toucherait aussi les images de cartes, et c'est un changement de configuration du livrable pour un problème de 5 lignes.

### Pitfall 10 : URLs absolues dans le HTML d'entrée Vite

**Ce qui se passe :** Vite réécrit les URL d'assets en préfixant `base`. Un `<link rel="stylesheet" href="/public/css/tokens.css">` écrit dans `vitrine.html` risque de devenir `/app/public/css/tokens.css` au build — cassé. La documentation consultée ne tranche pas explicitement ce cas.
**Confiance :** MEDIUM. À vérifier au premier build, c'est trivial (`grep tokens dist/vitrine.html`).
**Comment l'éviter par construction :** ne pas dépendre de la réponse. `tokens.css` a **une** source (`ui-app/styles/tokens.css`) et **deux** destinations : importé normalement par le bundle Vite, et copié tel quel vers `public/css/tokens.css` par `deployer.sh` pour les pages anciennes. Un seul fichier édité, deux consommateurs, aucun pari sur le comportement de Vite.

### Pitfall 11 : `Fusion/marvel-lcg-src/` est périmé

**Ce qui se passe :** le dossier `Fusion/marvel-lcg-src/` du dépôt Desktop ne contient **ni `fixtures.html`, ni `js/fixtures/`, ni `js/ui-switch.js`** — les trois livrables de la phase 1. Le codebase vivant est `~/marvel-work/fusion/marvel-lcg-src/`, et `Fusion/marvel-lcg-src-fusion.zip` est la sauvegarde.
**Comment l'éviter :** toute lecture ou modification de code de jeu se fait dans `~/marvel-work/fusion/marvel-lcg-src/`. Le rituel de livraison (re-zip + relance + autoplay 0 traceback) reste celui de la phase 1.

## Code Examples

### `ui-app/vitrine.html` — entrée multi-pages minimale

```html
<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vitrine du design system — Marvel Champions</title>
    <!-- tokens.css est importé par le bundle (voir src/vitrine.tsx). Les pages
         anciennes chargent la COPIE servie à /public/css/tokens.css. -->
</head>
<body>
    <div id="vitrine">Chargement…</div>
    <script type="module" src="/src/vitrine.tsx"></script>
</body>
</html>
```

Pas d'aiguillage `ui-switch.js` sur cette page : elle n'a pas d'ancienne version, il n'y a rien vers quoi revenir. La recette de câblage de la phase 1 s'applique à partir de la phase 3, quand un écran réel aura deux versions.

### Extension du harnais : capturer les 4 panneaux du wizard

```ts
// ui-check/tests/wizard-panneaux.spec.ts
// Les !important de wizard.css agissent majoritairement sur des panneaux
// masques au chargement. Sans ces captures, la purge de la phase 2 se ferait
// a l'aveugle sur environ 45 declarations sur 105.
import { test, expect } from '@playwright/test';

const PANNEAUX = [
  { index: 0, nom: 'scenario' },
  { index: 1, nom: 'rencontre' },
  { index: 2, nom: 'heros' },
  { index: 3, nom: 'lancement' },
];

for (const p of PANNEAUX) {
  test(`Preparation ancienne - etape ${p.index + 1} (${p.nom})`, async ({ page }) => {
    await page.addInitScript(() => { Math.random = () => 0.42; });
    await page.goto('/scene.html', { waitUntil: 'networkidle' });
    await expect(page).toHaveTitle(/New Game/);          // garde-fou anti clean_cache
    await page.locator(`.w-step[data-step="${p.index}"]`).click();
    await expect(page.locator(`.w-step-panel[data-panel="${p.index}"]`)).toHaveClass(/\bon\b/);
    await expect(page).toHaveScreenshot(`${p.nom}.png`, {
      fullPage: true,
      mask: [page.locator('#seed_div')],
    });
  });
}
```

### Vérification des contrastes déclarés par les tokens

```js
// ui-app/outils/contrastes.mjs
import { readFileSync } from 'node:fs'
import { wcagContrast } from 'culori'

// Les paires sont declarees a cote des tokens : le seuil fait partie du design
// system, pas du test. C'est ce que dit le critere 4 « le seuil defini par les tokens ».
const PAIRES = [
  { texte: '--mc-texte-regles', fond: '--mc-panneau',        seuil: 4.5, quoi: 'texte de regles' },
  { texte: '--mc-compteur',     fond: '--mc-carte-fond',     seuil: 3.0, quoi: 'compteur sur carte' },
  { texte: '--mc-texte',        fond: '--mc-fond',           seuil: 4.5, quoi: 'texte courant' },
]

const css = readFileSync('styles/tokens.css', 'utf8')
const valeur = (nom) => {
  const m = css.match(new RegExp(`${nom}\\s*:\\s*([^;]+);`))
  if (!m) throw new Error(`Token introuvable dans tokens.css : ${nom}`)
  return m[1].trim()
}

let echecs = 0
for (const p of PAIRES) {
  const ratio = wcagContrast(valeur(p.texte), valeur(p.fond))
  const ok = ratio >= p.seuil
  if (!ok) echecs++
  console.log(`${ok ? 'OK  ' : 'ECHEC'}  ${p.quoi} : ${ratio.toFixed(2)}:1 (seuil ${p.seuil}:1)`)
}
if (echecs) {
  console.error(`\n${echecs} paire(s) de couleurs sous le seuil. Corrige les tokens, pas le seuil.`)
  process.exit(1)
}
```

### Aspect affiché avec couleur + icône + libellé (ACC-01)

```jsx
// ui-app/src/composants/Aspect.tsx — la seule forme autorisee d'affichage d'aspect.
import { ASPECTS } from '../aspects'

export function Aspect({ cle, compte }: { cle: keyof typeof ASPECTS; compte?: number }) {
  const a = ASPECTS[cle]
  return (
    <span className="mc-aspect" style={{ '--teinte': `var(${a.token})` } as React.CSSProperties}>
      {/* 1. l'icone : identifiable en niveaux de gris */}
      <span className="mc-aspect__icone" aria-hidden="true" dangerouslySetInnerHTML={{ __html: a.svg }} />
      {/* 2. le libelle : jamais un title, jamais seulement une couleur */}
      <span className="mc-aspect__libelle">{a.libelle}</span>
      {compte != null && <b className="mc-aspect__compte">{compte}</b>}
    </span>
  )
}
```

Équivalent côté page ancienne, dans `js/prepare/app.js` (le `aspectBar` actuel ne porte que la couleur) :

```js
import { ASPECTS } from "/public/js/aspects.js";

function aspectBar(st) {
    const ordre = ["aggression", "justice", "leadership", "protection", "basic", "pool"];
    const segs = ordre.filter((a) => st.asp[a]).map((a) => el("span", {
        class: "seg",
        style: { background: `var(${ASPECTS[a].token})`, flex: st.asp[a] },
        // couleur + icone + libelle, meme dans la barre compacte
        html: `${ASPECTS[a].svg}<span class="seg-lbl">${ASPECTS[a].libelle} ${st.asp[a]}</span>`,
    }));
    return el("div", { class: "aspect-bar" }, ...segs);
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| `build.rollupOptions` | `build.rolldownOptions` | Vite 8, 12/03/2026 | Tout exemple multi-pages antérieur est à corriger, y compris celui de `.planning/research/STACK.md`. |
| Cible de build Chrome 107 / Safari 16.0 | Chrome 111 / Edge 111 / Firefox 114 / Safari 16.4 | Vite 8 | Aligné « Baseline Widely Available au 2026-01-01 ». Sans objet ici (navigateur local récent). |
| `!important` pour surcharger une feuille tierce | `@layer` | Baseline 2022 | L'ordre de couche l'emporte sur la spécificité : une classe dans `composants` bat `#set-images` dans `legacy` sans un seul `!important`. |
| Deux jeux de couleurs dupliqués pour le thème sombre en JS | `color-scheme` + `prefers-color-scheme` + `[data-theme]` | Baseline | Zéro JS pour le rendu, widgets natifs corrigés au passage. |
| `100vh` | `100dvh` | Baseline 2022 | Aucune occurrence de `dvh` dans `public/css/` aujourd'hui ; `wizard.css` et `prepare.css` utilisent `100vh`. À intégrer aux tokens de mise en page. |
| Media queries pour l'adaptation de composant | Container queries (`@container`, unités `cqi`) | Baseline 2023 | Pas nécessaire en phase 2 (page vitrine), mais les tokens d'espacement doivent être exprimés en `rem` pour rester compatibles. |

**Déprécié / à ne pas reproduire :**
- TypeScript 7.0.2 : `latest` sur npm mais sans API compilateur publique (vérifié le 2026-07-28 : le tag `next` est encore `7.1.0-dev`). `typescript-eslint` en mode type-aware ne fonctionne pas.
- `?v=N` manuel : remplacé par le hachage de contenu (neuf) et l'empreinte automatique (ancien).
- Font Awesome 4 (`css/font-awesome.css`, 40 Ko + `.eot`/`.woff`) chargé par `scene.html` : dépend de la route `handle_font` à chemin écrasé. Hors périmètre phase 2, mais candidat à la suppression quand `scene.html` sera remplacé.

## Open Questions

1. **Vite réécrit-il `href="/public/css/tokens.css"` en `/app/public/css/tokens.css` ?**
   - Ce qu'on sait : `base` réécrit « tous les chemins d'assets » ; la doc consultée ne traite pas explicitement les URL absolues pointant hors `publicDir`.
   - Ce qui est flou : le comportement exact pour un fichier absent de `publicDir`.
   - Recommandation : ne pas parier. Une source (`ui-app/styles/tokens.css`), deux destinations par copie. Vérification triviale au premier build (`grep tokens dist/vitrine.html`).

2. **Lightning CSS transforme-t-il `@layer` ou les fonctions de couleur modernes vers la cible Safari 16.4 ?**
   - Ce qu'on sait : Vite 8 embarque Lightning CSS comme dépendance standard et l'utilise pour la minification en production ; la cible par défaut inclut Safari 16.4.
   - Ce qui est flou : quelles fonctions sont downlevelées (`light-dark()` l'est sûrement, `oklch()` peut-être).
   - Recommandation : c'est la raison de servir `tokens.css` **brut** aux pages anciennes et d'éviter `light-dark()`. Si un token neuf utilise `oklch()` ou `color-mix()`, inspecter le CSS émis une fois. Au besoin, forcer `build.target: ['chrome120']` (navigateur local uniquement).

3. **Combien des 105 `!important` sont réellement nécessaires après purge ?**
   - Ce qu'on sait : les blocs `<style>` en ligne de `scene.html` chargent **après** `wizard.css`, ce qui explique la majorité des cas ; une fois ces blocs placés dans `@layer legacy`, ils perdent contre tout le layered.
   - Ce qui est flou : le nombre exact de régressions après purge sèche, non déterminable statiquement (il faudrait un vrai moteur de cascade).
   - Recommandation : purge sèche complète, puis correction guidée par les captures des 4 panneaux. Prévoir un plan dédié à la purge, avec checkpoint utilisateur sur photos.

4. **Périmètre exact de la tokenisation en phase 2.**
   - Ce qu'on sait : 200 valeurs en dur dans `menu/` + `prepare/`, 250 de plus dans `css/marvel/` (plateau, phase 5).
   - Ce qui est flou : faut-il inclure `cards.html` et `deck.html` (galerie et decks, différés en v1.x mais toujours en service, et `cards.html` porte la 3e palette d'aspects divergente) ?
   - Recommandation : périmètre minimal `menu/style.css` + `menu/wizard.css` + `prepare/prepare.css` pour le critère 2 ; inclure les 7 `style=` en ligne d'aspects de `cards.html` **uniquement** au titre d'ACC-01/ACC-02 (leurs contrastes sont mauvais), pas comme tokenisation complète.

5. **Nom et contenu exact de la page vitrine.**
   - Ce qu'on sait : le critère 1 demande « une page », la phase 3 s'occupe des écrans réels. La roadmap et `PITFALLS.md` avertissent contre le « design-system-first paralysant ».
   - Recommandation : `vitrine.html`, en français, montrant palette + typo + espacements + les 6 pastilles d'aspect + les paires de contraste + la bascule de thème. Rien d'autre. À ajouter à `ecrans.ts` avec un marqueur (`#vitrine`).

6. **Faut-il un `ui-switch.js` sur la page vitrine ?**
   - Ce qu'on sait : la recette de câblage de la phase 1 suppose deux versions d'un même écran.
   - Recommandation : non. La vitrine n'a pas d'équivalent ancien. La recette redevient obligatoire en phase 3.

## Sources

### Primary (HIGH confidence)

**Mesures directes sur le serveur en cours d'exécution (127.0.0.1:2345, launcher_fast.py)**
- Routage `public/app/` : `/app/vitrine.html`, `/public/app/index.html`, `/app/assets/*.js`, `/app/assets/*.css` → 200 avec le bon type MIME
- Échecs silencieux : `/app/test.woff2`, `/public/app/x.json`, `/public/app/assets/logo-a1b2.png` → **200 `image/jpeg`, 2035 octets**
- Échecs francs : `/public/app/assets/f-a1b2.woff`, `/public/app/assets/t-a1b2.svg` → 404
- Porte de sortie : après dépôt de `public/fonts/f-a1b2.woff` et `assets/textures/t-a1b2.svg`, les mêmes URL renvoient 200 (résolution par nom de fichier à plat)
- `/get_version` → `Set-Cookie: app_version=0.5.9.200r`, `Cache-Control: public, max-age=60`, `Content-Type: image/jpeg`
- Fichiers de test créés puis supprimés ; l'arborescence du jeu est revenue à son état initial

**Code du jeu, lu directement (`~/marvel-work/fusion/marvel-lcg-src/`)**
- `src/engine/network/web_server.py:130-164` (`ReadFile`, résolution `['./'] + find_paths`), `:218-277` (routes par extension), `:81-89` (`IsVersionMatch`), `:39` (`Cache-Control`)
- `src/engine/device/web/server/server_files.py:22-37` (fourre-tout `/{path:.+}` enregistré **en dernier**, après `AddDefaultGet()`)
- `src/engine/file/cache.py:29-111` (`Cache.LoadImage`, essai `.webp/.jpg/.png`, `CreateNoImage`, cache mémoire par nom de base)
- `src/engine/lib/mime_type.py`, `src/engine/file/manager.py:24` (`JoinPath` = `os.path.join`)
- `src/build.py:3` + `launcher.py:17` + `launcher_fast.py:29` : `RELEASE=1` dans les deux launchers
- `launch.json` : `cache_max_age: 60`

**Inventaire CSS mesuré**
- `css/menu/wizard.css` : 396 lignes, 67 lignes contenant `!important`, **105 déclarations** `!important` réparties sur 38 sélecteurs
- Répartition par panneau du wizard : ~33 panneau 0, 27 génériques, ~21 panneau 1, ~9 panneau 2, 16 panneau 3
- `scene.html` : 4 `.w-step-panel` (`data-panel` 0 à 3), un seul `on` au chargement ; **9 blocs `<style>`, 370 lignes, 66 règles, 1 `!important`**
- Ordre du `<head>` de `scene.html` : `menu/style.css` → `font-awesome.css` → `menu/wizard.css?v=9` → blocs `<style>` en ligne
- Couleurs en dur : wizard 83, prepare 77, style 34, preview 6, `css/marvel/*` 250
- `?v=N` réels : 5 (`prepare.html` ×2, `js/prepare/app.js` ×2, `scene.html` ×1)
- Palettes d'aspects : `js/prepare/app.js:28`, `cards.html:280-300` (attributs `style=` en ligne), `css/menu/wizard.css:18-19`
- Police d'icônes : `css/marvel/marvel.css:74-75` (`marvel-icons` ← `ChampionsIcons.ttf`) ; glyphes couverts relevés dans `css/marvel/icon.css` — **aucun glyphe d'aspect**
- Environnement : `~/.local/bin/node` → `node.exe` Windows (v25.3.0), npm 11.6.2, aucun Node Linux ; `rsync` 3.2.7 disponible en WSL

**Registre npm interrogé le 2026-07-28**
- `vite@8.1.5` (engines `^20.19.0 || >=22.12.0`), `react@19.2.8`, `react-dom@19.2.8`, `typescript` latest `7.0.2` / dernier 6.x `6.0.3` / next `7.1.0-dev.20260728.1`, `@vitejs/plugin-react@6.0.4` (peer `vite: ^8.0.0`, peers Babel optionnels), `@axe-core/playwright@4.12.1`, `culori@4.0.2`, `wcag-contrast@3.0.0`, `vite-plugin-checker@0.14.5`, `stylelint@17.14.1`, `typescript-eslint@8.65.0`, `eslint@10.8.0`, `colorjs.io@0.7.1`

**Documentation officielle**
- https://developer.mozilla.org/en-US/docs/Web/CSS/@layer — « Styles that are not defined in a layer always override styles declared in named and anonymous layers » ; « The order of precedence among important rules is the inverse of normal rules »
- https://developer.mozilla.org/en-US/docs/Web/CSS/@import — `@import` doit précéder toute autre règle sauf `@charset` et `@layer` ; syntaxe `layer(nom)`
- https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark — Baseline 2024, exige `color-scheme: light dark`
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/link — **aucun attribut `layer`** documenté
- https://vite.dev/guide/migration.html — « `build.rollupOptions`: renamed to `build.rolldownOptions` » ; nouvelles cibles Chrome 111 / Edge 111 / Firefox 114 / Safari 16.4
- https://vite.dev/guide/build.html — multi-pages via `rolldownOptions.input` ; « Vite ignores the name given to the entry … and instead respects the resolved id of the file »
- https://vite.dev/config/build-options.html — `assetsInlineLimit: number | ((filePath, content) => boolean | undefined)`, défaut 4096 ; `sourcemap` défaut `false` ; `emptyOutDir` défaut `true` si `outDir` est dans `root`
- https://vite.dev/guide/cli.html — `vite build --watch` : « Rebuilds when modules have changed on disk »
- https://vite.dev/blog/announcing-vite8 — stable le 12/03/2026, Rolldown, Node 20.19+/22.12+

**Documents du projet**
- `.planning/research/PITFALLS.md` §7 (cohabitation CSS, inversion `!important`/`@layer`) et §11 (design-system-first)
- `.planning/research/STACK.md` (tableau des contraintes serveur — **corrigé ici sur `rollupOptions`**)
- `.planning/phases/01-filet-de-securite/01-RESEARCH.md` Pitfalls 1 à 4 (Node Windows, liste blanche, `public/` symlinké par `launcher_fast.py`, verrou de version)
- `.planning/STATE.md` (décisions structurantes, contraintes d'environnement)
- `ui-check/playwright.config.ts`, `ui-check/ecrans.ts`, `ui-check/global-setup.ts`, `ui-check/package.json`

### Secondary (MEDIUM confidence)
- Comportement de Vite face aux URL absolues du HTML d'entrée : déduit du rôle de `base`, non confirmé explicitement par la documentation consultée (voir Open Question 1)
- Transformation de `light-dark()` / `oklch()` par Lightning CSS vers la cible par défaut : plausible, non vérifié (voir Open Question 2)
- Estimation « ~45 `!important` sur des panneaux non capturés » : attribution automatique des sélecteurs aux panneaux par identifiant ; les sélecteurs multi-panneaux ont été répartis au prorata

### Tertiary (LOW confidence)
- Attribut `layer` sur `<link>` : proposition CSSWG (issue #5853), absente de MDN. Considéré **non disponible** — d'où la recommandation d'envelopper les fichiers plutôt que de compter dessus

## Metadata

**Confidence breakdown:**
- Contraintes serveur et configuration du build : **HIGH** — vérifiées en direct sur le serveur en cours, code lu, tests créés puis nettoyés
- Versions et compatibilités npm : **HIGH** — registre interrogé le jour même, peers et engines lus
- Inventaire CSS et séquence de purge : **HIGH** sur les chiffres (mesurés fichier par fichier), **MEDIUM** sur le nombre de régressions attendues après purge (non déterminable statiquement)
- Sémantique de `@layer` et de l'inversion `!important` : **HIGH** — MDN, citée mot pour mot
- Thème sombre et contrastes : **HIGH** sur le mécanisme, **MEDIUM** sur le choix des seuils par token (dépend du design, à trancher en planification)
- Iconographie des aspects : **HIGH** sur le constat (aucun glyphe existant, 3 palettes divergentes, 1 violation ACC-01 franche), **MEDIUM** sur la forme de la solution partagée (module `.js` recommandé, non éprouvé sur ce projet)

**Research date:** 2026-07-28
**Valid until:** 2026-08-27 (30 jours). À revalider plus tôt si Vite passe en 8.2, si TypeScript 7.1 sort (l'API compilateur débloquerait la migration TS 7), ou si Playwright monte de version (re-validation des références obligatoire).
