# Plateau mobile — plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rendre le plateau Marvel Champions jouable au doigt sur un téléphone, par un rendu alternatif condensé qui tient toujours à l'écran, sans modifier le mode PC.

**Architecture :** `zones.ts` produit déjà un `Plateau` (emplacements, unités, identifiants affichés) que `Board.tsx` dessine dans une scène de 1920x940 mise à l'échelle. On ajoute un second consommateur de ce même `Plateau`, `PlateauMobile.tsx`, qui le rend en bandes condensées non défilantes, avec une couche de focus par bande. `board.tsx` choisit l'un ou l'autre selon `useModeMobile`. `ScanCard`, `interaction.ts`, `MenuActionsCarte`, `SelecteurCibles` et `world.ts` sont partagés sans modification de comportement.

**Tech Stack :** React 19.2.8, TypeScript 6.0.3, Vite 8.1.5, Vitest + jsdom + @testing-library/react (ajoutés par ce plan), Playwright 1.62.0 (existant, dans `ui-check/`).

**Spec :** `docs/superpowers/specs/2026-08-02-plateau-mobile-design.md`

## Global Constraints

- Le mode PC n'est jamais modifié. `Board.tsx` et `board.css` ne changent pas de comportement de rendu ; les références de captures PC restent vertes.
- Le runtime historique `public/js/marvel/` n'est ni lu ni modifié. Le nouveau code est une fonction pure de `/get_world`.
- Tout passage vers le jeu se fait par `bash ui-app/deployer.sh`, jamais par une recopie de `dist/` à la main.
- Le routage du serveur est une liste blanche stricte par extension : le build ne produit que `.html`, `.js`, `.css`. `assetsInlineLimit: () => true` reste en place.
- Ne jamais écrire dans `Fusion/marvel-lcg-src` (codebase de distribution périmé, servi avec une partie possiblement en cours). Le codebase de travail est `~/marvel-work/fusion/marvel-lcg-src`.
- Node est le binaire Windows : il ne lit pas les chemins WSL, et npm exécute ses scripts via `cmd.exe`. **Tout script npm doit rester une commande unique** (pas de `&&`, pas de `;`).
- TypeScript reste en 6.0.3. `vite-plugin-checker` fait échouer le build sur erreur de type : le typage doit être juste, aucun `any`.
- Tout le texte visible passe par `t()` de `board/langue.ts`, comme le reste du plateau.
- Pas d'em dash dans les commentaires ni dans les libellés.
- Cible de référence : 480x1050 px CSS, `pointer: coarse`. Toute cible tactile fait au moins 44x44 px.

## Structure des fichiers

Tout le neuf vit dans `ui-app/src/board/mobile/`. Un fichier, une responsabilité.

| Fichier | Responsabilité |
|---|---|
| `condensation.ts` | Pur. Combien de tuiles tiennent dans un budget, à quelle taille, combien restent |
| `condensation.test.ts` | Ses tests |
| `couches.ts` | Pur. La pile des couches ouvertes (focus, menu, sélecteur) |
| `couches.test.ts` | Ses tests |
| `useModeMobile.ts` | La bascule mobile/PC : media query, réglage ⚙, `localStorage` |
| `useModeMobile.test.ts` | Ses tests |
| `bandes.ts` | Pur. La table qui range les 11 `CleEmplacement` en 6 bandes |
| `bandes.test.ts` | Ses tests |
| `TuileCondensee.tsx` | Une entité réduite à vignette, nom court, compteurs |
| `TuileCondensee.test.tsx` | Ses tests |
| `BandeMobile.tsx` | Une bande : titre, tuiles condensées, pastille « +N » |
| `ZoneFocus.tsx` | Le niveau 2 : une bande ouverte en feuille, cartes à 149 px |
| `PlateauMobile.tsx` | Le niveau 1 : HUD, bandes, barre d'action, tiroir de main |
| `mobile.css` | Les styles des deux niveaux |
| `joueurs.ts` | Pur. Répartition des groupes de `terrain-soutien` par joueur |
| `joueurs.test.ts` | Ses tests |

Fichiers existants modifiés : `ui-app/src/board.tsx` (choix du rendu, réglage ⚙), `ui-app/src/board/zones.ts` (un champ additif `proprietaires`), `ui-app/package.json`, `ui-check/playwright.config.ts`, `ui-check/tests/` (un fichier de test nouveau).

---

### Task 1 : Outillage de test unitaire et modèle de condensation

Le modèle de condensation est la règle qui rend le niveau 1 tenable : il décide combien de tuiles s'affichent, à quelle taille, et combien se replient dans une pastille « +N ». C'est une fonction pure dont la justesse est invisible sur une capture d'écran, d'où l'ajout de Vitest.

**Files:**
- Modify: `ui-app/package.json`
- Create: `ui-app/vitest.config.ts`
- Create: `ui-app/src/board/mobile/condensation.ts`
- Test: `ui-app/src/board/mobile/condensation.test.ts`

**Interfaces:**
- Consomme : `UniteAffichee` de `../zones` (déjà exporté).
- Produit : `condenser(unites, budget) => BandeCondensee`, les types `Taille`, `BudgetBande`, `BandeCondensee`, et les constantes `TUILE_CONFORT`, `TUILE_PLANCHER`, `ECART`.

- [ ] **Step 1 : Installer Vitest et son environnement DOM**

Justification de la dépendance, à recopier dans le message de commit : les règles de condensation et la pile de couches sont de la logique pure dont la justesse ne se voit pas sur une capture, et Playwright ne sait pas les tester à ce niveau.

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm install --save-dev vitest@^3 jsdom@^26 @testing-library/react@^16 @testing-library/jest-dom@^6
```

- [ ] **Step 2 : Déclarer le script de test**

Dans `ui-app/package.json`, ajouter dans `scripts` (une commande unique, npm passe par `cmd.exe`) :

```json
"test": "vitest run"
```

- [ ] **Step 3 : Créer `ui-app/vitest.config.ts`**

Configuration séparée de `vite.config.ts` : `vite-plugin-checker` et l'entrée multi-pages n'ont rien à faire dans une exécution de tests.

```ts
// Configuration des tests unitaires. Separee de vite.config.ts : le plugin de
// verification de types et l'entree multi-pages n'ont rien a faire ici.
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['src/**/*.test.{ts,tsx}'],
    setupFiles: ['./src/test-setup.ts'],
  },
})
```

- [ ] **Step 4 : Créer `ui-app/src/test-setup.ts`**

```ts
// Charge les matchers DOM (toBeInTheDocument, toHaveClass...) pour tous les tests.
import '@testing-library/jest-dom/vitest'
```

- [ ] **Step 5 : Écrire les tests de condensation (ils doivent échouer)**

Créer `ui-app/src/board/mobile/condensation.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { condenser, type BudgetBande } from './condensation'
import type { UniteAffichee } from '../zones'

/** Une unite minimale : condenser() ne regarde que le nombre, jamais le contenu. */
function unites(nombre: number): UniteAffichee[] {
  return Array.from({ length: nombre }, (_, index) => ({
    cle: `u${index}`,
    carte: { id: String(index), name: `Carte ${index}`, kind: 'ally', imageUrl: '' },
    attachees: [],
  }))
}

const LARGE: BudgetBande = { largeur: 464, hauteur: 200 }
const ETROIT: BudgetBande = { largeur: 464, hauteur: 72 }
const MINUSCULE: BudgetBande = { largeur: 150, hauteur: 72 }

describe('condenser', () => {
  it('ne dessine rien pour une bande vide', () => {
    const bande = condenser([], LARGE)
    expect(bande.tuiles).toHaveLength(0)
    expect(bande.restantes).toBe(0)
  })

  it('garde la taille de confort quand tout tient', () => {
    const bande = condenser(unites(2), LARGE)
    expect(bande.taille).toBe('confort')
    expect(bande.tuiles).toHaveLength(2)
    expect(bande.restantes).toBe(0)
  })

  it('descend au plancher plutot que de replier', () => {
    // 9 unites ne tiennent pas en confort dans ce budget, mais tiennent au plancher.
    const bande = condenser(unites(9), LARGE)
    expect(bande.taille).toBe('plancher')
    expect(bande.tuiles).toHaveLength(9)
    expect(bande.restantes).toBe(0)
  })

  it('replie le surplus dans une pastille et reserve sa place', () => {
    const bande = condenser(unites(20), ETROIT)
    expect(bande.taille).toBe('plancher')
    expect(bande.restantes).toBeGreaterThan(0)
    // Une place est reservee a la pastille « +N » : elle ne recouvre pas une tuile.
    expect(bande.tuiles.length + bande.restantes).toBe(20)
  })

  it('ne montre aucune tuile quand une seule place existe', () => {
    const bande = condenser(unites(5), MINUSCULE)
    expect(bande.tuiles).toHaveLength(0)
    expect(bande.restantes).toBe(5)
  })

  it('conserve toujours l\'invariant tuiles + restantes = total', () => {
    for (const nombre of [1, 3, 7, 12, 40]) {
      for (const budget of [LARGE, ETROIT, MINUSCULE]) {
        const bande = condenser(unites(nombre), budget)
        expect(bande.tuiles.length + bande.restantes).toBe(nombre)
        expect(bande.restantes).toBeGreaterThanOrEqual(0)
      }
    }
  })
})
```

- [ ] **Step 6 : Lancer les tests pour vérifier qu'ils échouent**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm test`
Attendu : ÉCHEC, `Failed to resolve import "./condensation"`.

- [ ] **Step 7 : Écrire `ui-app/src/board/mobile/condensation.ts`**

```ts
// Combien de tuiles tiennent dans une bande, a quelle taille, combien restent.
//
// C'est la regle qui remplace le zoom optique : le niveau 1 ne defile JAMAIS,
// il condense davantage. Par ordre d'application :
//   1. les tuiles rétrécissent jusqu'a leur taille plancher ;
//   2. au-dela, le surplus se replie dans une pastille « +N » touchable ;
//   3. (hors de ce fichier) un seul joueur est deplie a la fois.
//
// Fonction pure : elle ne regarde que le NOMBRE d'unites, jamais leur contenu.

import type { UniteAffichee } from '../zones'

/** Taille d'une tuile condensee, en pixels CSS. */
export const TUILE_CONFORT = { largeur: 140, hauteur: 96 }

/**
 * Plancher de lisibilite. 64 px de haut est la valeur de la spec : en dessous,
 * le nom et les compteurs ne sont plus lisibles, et la cible tactile passe sous
 * les 44 px une fois la marge interne retiree.
 */
export const TUILE_PLANCHER = { largeur: 96, hauteur: 64 }

/** Ecart entre deux tuiles, dans les deux axes. */
export const ECART = 8

export type Taille = 'confort' | 'plancher'

export type BudgetBande = {
  /** Place disponible pour les tuiles, marges de la bande deja retirees. */
  largeur: number
  hauteur: number
}

export type BandeCondensee = {
  /** Les unites reellement dessinees, dans l'ordre recu. */
  tuiles: UniteAffichee[]
  /** Les unites repliees dans la pastille « +N ». Jamais negatif. */
  restantes: number
  taille: Taille
}

/** Combien de tuiles de cette taille tiennent dans ce budget. Au moins 0. */
function capacite(budget: BudgetBande, tuile: { largeur: number; hauteur: number }): number {
  const colonnes = Math.floor((budget.largeur + ECART) / (tuile.largeur + ECART))
  const rangees = Math.floor((budget.hauteur + ECART) / (tuile.hauteur + ECART))
  return Math.max(0, colonnes * rangees)
}

export function condenser(unites: UniteAffichee[], budget: BudgetBande): BandeCondensee {
  if (unites.length === 0) {
    return { tuiles: [], restantes: 0, taille: 'confort' }
  }

  if (unites.length <= capacite(budget, TUILE_CONFORT)) {
    return { tuiles: unites, restantes: 0, taille: 'confort' }
  }

  const placesAuPlancher = capacite(budget, TUILE_PLANCHER)
  if (unites.length <= placesAuPlancher) {
    return { tuiles: unites, restantes: 0, taille: 'plancher' }
  }

  // Une place est reservee a la pastille « +N » : elle ne recouvre pas une tuile.
  const montrees = Math.max(0, placesAuPlancher - 1)
  return {
    tuiles: unites.slice(0, montrees),
    restantes: unites.length - montrees,
    taille: 'plancher',
  }
}
```

- [ ] **Step 8 : Lancer les tests pour vérifier qu'ils passent**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm test`
Attendu : 6 tests verts dans `condensation.test.ts`.

- [ ] **Step 9 : Vérifier que le typage reste propre**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm run typecheck`
Attendu : aucune sortie, code de retour 0.

- [ ] **Step 10 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/package.json ui-app/package-lock.json ui-app/vitest.config.ts ui-app/src/test-setup.ts ui-app/src/board/mobile/
git commit -m "feat(mobile): modele de condensation des bandes, teste

Ajout de Vitest : les regles de condensation sont de la logique pure dont la
justesse ne se voit pas sur une capture d'ecran."
```

---

### Task 2 : La bascule mobile / PC

**Files:**
- Create: `ui-app/src/board/mobile/useModeMobile.ts`
- Test: `ui-app/src/board/mobile/useModeMobile.test.ts`

**Interfaces:**
- Produit : `type ReglageMode = 'auto' | 'mobile' | 'pc'`, `type ModeRendu = 'mobile' | 'pc'`, `CLE_MODE`, `REQUETE_MOBILE`, `modeEffectif(reglage, correspond) => ModeRendu`, `lireReglage() => ReglageMode`, `ecrireReglage(reglage) => void`, `useModeMobile() => { mode, reglage, changer }`.

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/useModeMobile.test.ts` :

```ts
import { beforeEach, describe, expect, it } from 'vitest'
import { CLE_MODE, ecrireReglage, lireReglage, modeEffectif } from './useModeMobile'

describe('modeEffectif', () => {
  it('suit la media query en mode auto', () => {
    expect(modeEffectif('auto', true)).toBe('mobile')
    expect(modeEffectif('auto', false)).toBe('pc')
  })

  it('ignore la media query quand un mode est force', () => {
    expect(modeEffectif('mobile', false)).toBe('mobile')
    expect(modeEffectif('pc', true)).toBe('pc')
  })
})

describe('reglage memorise', () => {
  beforeEach(() => window.localStorage.clear())

  it('vaut auto quand rien n\'est memorise', () => {
    expect(lireReglage()).toBe('auto')
  })

  it('relit ce qui a ete ecrit', () => {
    ecrireReglage('mobile')
    expect(window.localStorage.getItem(CLE_MODE)).toBe('mobile')
    expect(lireReglage()).toBe('mobile')
  })

  it('retombe sur auto devant une valeur inconnue', () => {
    window.localStorage.setItem(CLE_MODE, 'tablette')
    expect(lireReglage()).toBe('auto')
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- useModeMobile` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/useModeMobile.ts`**

```ts
// Le plateau se dessine-t-il en mode mobile ou en mode PC ?
//
// La decision est prise en JavaScript, pas en CSS : ce n'est pas une question
// d'apparence mais de composant a monter. Le reglage a trois etats permet de
// tester le mode mobile depuis un PC, et de repasser en mode PC sur une tablette.
//
// La memorisation suit le modele de la bascule ?ui=old : localStorage, jamais
// l'adresse (le lancement d'une partie efface toute query string) et jamais un
// cookie (le serveur en pose deja deux).

import { useEffect, useState } from 'react'

export type ReglageMode = 'auto' | 'mobile' | 'pc'
export type ModeRendu = 'mobile' | 'pc'

export const CLE_MODE = 'mode-plateau'

/** Un ecran etroit OU un pointeur grossier suffit : la virgule est un OU en CSS. */
export const REQUETE_MOBILE = '(max-width: 900px), (pointer: coarse)'

export function modeEffectif(reglage: ReglageMode, correspond: boolean): ModeRendu {
  if (reglage === 'mobile') return 'mobile'
  if (reglage === 'pc') return 'pc'
  return correspond ? 'mobile' : 'pc'
}

export function lireReglage(): ReglageMode {
  try {
    const valeur = window.localStorage.getItem(CLE_MODE)
    return valeur === 'mobile' || valeur === 'pc' ? valeur : 'auto'
  } catch {
    return 'auto'
  }
}

export function ecrireReglage(reglage: ReglageMode): void {
  try {
    window.localStorage.setItem(CLE_MODE, reglage)
  } catch {
    // Navigation privee, quota plein : le reglage ne survit pas, le jeu si.
  }
}

export function useModeMobile(): {
  mode: ModeRendu
  reglage: ReglageMode
  changer: (reglage: ReglageMode) => void
} {
  const [reglage, setReglage] = useState<ReglageMode>(lireReglage)
  const [correspond, setCorrespond] = useState(
    () => window.matchMedia(REQUETE_MOBILE).matches
  )

  useEffect(() => {
    const liste = window.matchMedia(REQUETE_MOBILE)
    const surChangement = (evenement: MediaQueryListEvent) => setCorrespond(evenement.matches)
    liste.addEventListener('change', surChangement)
    return () => liste.removeEventListener('change', surChangement)
  }, [])

  const changer = (suivant: ReglageMode) => {
    ecrireReglage(suivant)
    setReglage(suivant)
  }

  return { mode: modeEffectif(reglage, correspond), reglage, changer }
}
```

- [ ] **Step 4 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- useModeMobile` depuis `ui-app/`
Attendu : 5 tests verts.

- [ ] **Step 5 : Commit**

```bash
git add ui-app/src/board/mobile/useModeMobile.ts ui-app/src/board/mobile/useModeMobile.test.ts
git commit -m "feat(mobile): bascule mobile/PC a trois etats, memorisee"
```

---

### Task 3 : La table des bandes

Les 11 `CleEmplacement` de `zones.ts` se rangent en 6 bandes lisibles. C'est une table, pas une logique : elle vit dans son propre fichier pour qu'ajouter un emplacement soit une ligne.

**Files:**
- Create: `ui-app/src/board/mobile/bandes.ts`
- Test: `ui-app/src/board/mobile/bandes.test.ts`

**Interfaces:**
- Consomme : `CleEmplacement`, `EmplacementAffiche`, `Plateau` de `../zones`.
- Produit : `type CleBande`, `BANDES`, `repartir(plateau) => BandeAffichee[]`, `type BandeAffichee = { cle: CleBande; titre: string; emplacements: EmplacementAffiche[] }`.

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/bandes.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { BANDES, repartir } from './bandes'
import type { CleEmplacement, EmplacementAffiche, Plateau } from '../zones'

function emplacement(cle: CleEmplacement): EmplacementAffiche {
  return { cle, titre: cle, groupes: [[]], nombreSurLaLigne: 0 }
}

function plateau(cles: CleEmplacement[]): Plateau {
  return {
    emplacements: cles.map(emplacement),
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

describe('BANDES', () => {
  it('range les 11 emplacements sans oubli ni doublon', () => {
    const toutes: CleEmplacement[] = [
      'piles-rencontre', 'rencontre', 'complot-principal', 'complots-secondaires',
      'terrain-combat', 'terrain-soutien', 'deck-special', 'piles-joueur',
      'nemesis', 'annexes', 'main',
    ]
    const rangees = BANDES.flatMap((bande) => bande.emplacements)
    expect([...rangees].sort()).toEqual([...toutes].sort())
  })
})

describe('repartir', () => {
  it('ne rend pas une bande dont aucun emplacement n\'est present', () => {
    const bandes = repartir(plateau(['rencontre']))
    expect(bandes.map((bande) => bande.cle)).toEqual(['vilain'])
  })

  it('regroupe les emplacements d\'une meme bande', () => {
    const bandes = repartir(plateau(['complot-principal', 'complots-secondaires']))
    expect(bandes).toHaveLength(1)
    expect(bandes[0].cle).toBe('complots')
    expect(bandes[0].emplacements).toHaveLength(2)
  })

  it('rend les bandes dans l\'ordre de lecture, pas dans celui du plateau', () => {
    const bandes = repartir(plateau(['main', 'rencontre', 'complot-principal']))
    expect(bandes.map((bande) => bande.cle)).toEqual(['vilain', 'complots', 'main'])
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- bandes` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/bandes.ts`**

```ts
// Les 11 emplacements de zones.ts, ranges en 6 bandes lisibles sur un telephone.
//
// C'est une TABLE, pas une logique. Ajouter un emplacement dans zones.ts, c'est
// ajouter une entree ici : le test verifie qu'aucun ne reste orphelin.
//
// L'ordre des bandes est l'ordre de LECTURE du plateau (la menace d'abord, ta
// main en dernier), pas l'ordre dans lequel zones.ts les produit.

import { t } from '../langue'
import type { CleEmplacement, EmplacementAffiche, Plateau } from '../zones'

export type CleBande = 'vilain' | 'complots' | 'terrain' | 'rencontre' | 'heros' | 'main'

export const BANDES: Array<{
  cle: CleBande
  titre: () => string
  emplacements: CleEmplacement[]
}> = [
  { cle: 'vilain', titre: () => t('Méchant'), emplacements: ['rencontre'] },
  {
    cle: 'complots',
    titre: () => t('Manigances'),
    emplacements: ['complot-principal', 'complots-secondaires'],
  },
  { cle: 'terrain', titre: () => t('Terrain'), emplacements: ['terrain-combat'] },
  { cle: 'rencontre', titre: () => t('Rencontre'), emplacements: ['piles-rencontre'] },
  {
    cle: 'heros',
    titre: () => t('Héros'),
    emplacements: ['terrain-soutien', 'deck-special', 'piles-joueur', 'nemesis', 'annexes'],
  },
  { cle: 'main', titre: () => t('Ta main'), emplacements: ['main'] },
]

export type BandeAffichee = {
  cle: CleBande
  titre: string
  emplacements: EmplacementAffiche[]
}

/** Les bandes reellement peuplees, dans l'ordre de lecture. */
export function repartir(plateau: Plateau): BandeAffichee[] {
  const parCle = new Map<CleEmplacement, EmplacementAffiche>()
  for (const emplacement of plateau.emplacements) parCle.set(emplacement.cle, emplacement)

  return BANDES.map((bande) => ({
    cle: bande.cle,
    titre: bande.titre(),
    emplacements: bande.emplacements
      .map((cle) => parCle.get(cle))
      .filter((emplacement): emplacement is EmplacementAffiche => emplacement !== undefined),
  })).filter((bande) => bande.emplacements.length > 0)
}
```

- [ ] **Step 4 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- bandes` depuis `ui-app/`
Attendu : 4 tests verts.

Si le test « range les 11 emplacements » échoue, c'est que `zones.ts` a changé : ajouter l'emplacement manquant à la bande qui lui convient, jamais assouplir le test.

- [ ] **Step 5 : Commit**

```bash
git add ui-app/src/board/mobile/bandes.ts ui-app/src/board/mobile/bandes.test.ts
git commit -m "feat(mobile): table des 6 bandes, couverture des 11 emplacements verifiee"
```

---

### Task 4 : La tuile condensée

**Files:**
- Create: `ui-app/src/board/mobile/TuileCondensee.tsx`
- Create: `ui-app/src/board/mobile/mobile.css`
- Test: `ui-app/src/board/mobile/TuileCondensee.test.tsx`

**Interfaces:**
- Consomme : `ScanCardProps` de `../../components/ScanCard`, `Taille` de `./condensation`.
- Produit : `TuileCondensee` et `type TuileCondenseeProps = { carte: ScanCardProps; taille: Taille; onOuvrir: () => void }`.

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/TuileCondensee.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { TuileCondensee } from './TuileCondensee'
import type { ScanCardProps } from '../../components/ScanCard'

const RHINO: ScanCardProps = {
  id: '42',
  name: 'Rhino',
  kind: 'villain',
  imageUrl: '/scan.jpg',
  allyHp: '12/22',
  counters: [{ label: 'Tough', value: 1 }],
}

describe('TuileCondensee', () => {
  it('montre le nom et les compteurs sans ouvrir la carte', () => {
    render(<TuileCondensee carte={RHINO} taille="confort" onOuvrir={() => {}} />)
    expect(screen.getByText('Rhino')).toBeInTheDocument()
    expect(screen.getByText('12/22')).toBeInTheDocument()
    expect(screen.getByText('Tough 1')).toBeInTheDocument()
  })

  it('est un bouton, donc atteignable au doigt et au clavier', () => {
    const ouvrir = vi.fn()
    render(<TuileCondensee carte={RHINO} taille="confort" onOuvrir={ouvrir} />)
    screen.getByRole('button', { name: /Rhino/ }).click()
    expect(ouvrir).toHaveBeenCalledOnce()
  })

  it('porte la classe de sa taille', () => {
    const { container } = render(
      <TuileCondensee carte={RHINO} taille="plancher" onOuvrir={() => {}} />
    )
    expect(container.querySelector('.tuile')).toHaveClass('tuile-plancher')
  })

  it('ne divulgue rien d\'une carte face cachee', () => {
    render(
      <TuileCondensee
        carte={{ ...RHINO, facedown: true }}
        taille="confort"
        onOuvrir={() => {}}
      />
    )
    expect(screen.queryByText('Rhino')).not.toBeInTheDocument()
    expect(screen.queryByText('12/22')).not.toBeInTheDocument()
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- TuileCondensee` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/TuileCondensee.tsx`**

```tsx
// Une entite du plateau, reduite a ce qu'il faut pour DECIDER : sa vignette, son
// nom, et les seuls chiffres qui comptent. Le texte de regles et le scan complet
// arrivent au tap, dans le menu d'actions.
//
// Une tuile est un <button> : c'est ce qui la rend atteignable au doigt ET au
// clavier sans code supplementaire, et ce qui lui donne un role accessible.

import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { Taille } from './condensation'
import './mobile.css'

export type TuileCondenseeProps = {
  carte: ScanCardProps
  taille: Taille
  onOuvrir: () => void
}

export function TuileCondensee({ carte, taille, onOuvrir }: TuileCondenseeProps) {
  // Une carte face cachee ne divulgue NI son nom NI ses compteurs : ce serait
  // donner au joueur une information que le moteur lui refuse.
  const cachee = carte.facedown === true && carte.peeking !== true
  const nom = cachee ? t('Carte face cachée') : carte.name

  return (
    <button
      type="button"
      className={`tuile ${taille === 'plancher' ? 'tuile-plancher' : 'tuile-confort'}`}
      onClick={onOuvrir}
      data-tactile="tuile"
    >
      <span className="tuile-vignette" aria-hidden="true">
        {cachee ? null : <img src={carte.imageUrl} alt="" loading="lazy" />}
      </span>
      <span className="tuile-texte">
        <span className="tuile-nom">{nom}</span>
        {cachee ? null : (
          <span className="tuile-compteurs">
            {carte.allyHp ? <span className="tuile-pv">{carte.allyHp}</span> : null}
            {carte.schemeThreat ? (
              <span className="tuile-menace">{carte.schemeThreat}</span>
            ) : null}
            {carte.pileCount ? <span className="tuile-pile">{carte.pileCount}</span> : null}
            {(carte.counters ?? []).map((compteur) => (
              <span className="tuile-compteur" key={compteur.label}>
                {compteur.label} {compteur.value}
              </span>
            ))}
          </span>
        )}
      </span>
    </button>
  )
}
```

- [ ] **Step 4 : Écrire les styles dans `ui-app/src/board/mobile/mobile.css`**

```css
/* Le plateau au doigt. Deux niveaux : la vue d'etat (qui ne defile jamais) et
   la zone en focus (ou l'on agit, cartes a 149 px).

   Les tailles ici sont des pixels CSS reels, pas des pixels de scene : ce rendu
   n'est PAS mis a l'echelle, contrairement a board.css. */

@layer composants {
  /* --- Tuile condensee ---------------------------------------------------- */

  .tuile {
    display: flex;
    align-items: center;
    gap: 8px;
    /* 44 px est le plancher tactile ; 64 est le plancher de LISIBILITE, seul
       celui-ci nous limite. */
    min-height: 64px;
    padding: 6px 8px;
    font: inherit;
    text-align: left;
    color: #e8e9ee;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    cursor: pointer;
  }

  .tuile-confort {
    width: 140px;
    height: 96px;
  }

  .tuile-plancher {
    width: 96px;
    height: 64px;
  }

  .tuile-vignette {
    flex: 0 0 auto;
    width: 34px;
    height: 47px;
    overflow: hidden;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.5);
  }

  .tuile-vignette img {
    width: 100%;
    height: 100%;
    /* Le haut du scan porte l'art et le nom : c'est ce qu'on garde en cadrant. */
    object-fit: cover;
    object-position: top center;
  }

  .tuile-texte {
    display: grid;
    gap: 2px;
    min-width: 0;
  }

  .tuile-nom {
    overflow: hidden;
    font-size: 0.8rem;
    font-weight: 800;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .tuile-plancher .tuile-nom {
    font-size: 0.72rem;
  }

  .tuile-compteurs {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    font-size: 0.7rem;
    font-weight: 900;
  }

  .tuile-pv {
    color: #ff8a8a;
  }

  .tuile-menace {
    color: #ffd45a;
  }

  .tuile-pile,
  .tuile-compteur {
    color: #9fb0c4;
  }
}
```

- [ ] **Step 5 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- TuileCondensee` depuis `ui-app/`
Attendu : 4 tests verts.

- [ ] **Step 6 : Commit**

```bash
git add ui-app/src/board/mobile/TuileCondensee.tsx ui-app/src/board/mobile/TuileCondensee.test.tsx ui-app/src/board/mobile/mobile.css
git commit -m "feat(mobile): tuile condensee, face cachee non divulguee"
```

---

### Task 5 : La pile des couches et le retour d'Android

**Files:**
- Create: `ui-app/src/board/mobile/couches.ts`
- Test: `ui-app/src/board/mobile/couches.test.ts`

**Interfaces:**
- Produit : `type Couche = { sorte: 'focus'; bande: CleBande } | { sorte: 'carte'; id: string }`, `empiler(pile, couche) => Couche[]`, `depiler(pile) => Couche[]`, `sommet(pile) => Couche | undefined`, `useCouches() => { pile, ouvrir, fermer, toutFermer }`.

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/couches.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { depiler, empiler, sommet, type Couche } from './couches'

const FOCUS: Couche = { sorte: 'focus', bande: 'heros' }
const CARTE: Couche = { sorte: 'carte', id: '42' }

describe('pile des couches', () => {
  it('est vide au depart', () => {
    expect(sommet([])).toBeUndefined()
    expect(depiler([])).toEqual([])
  })

  it('empile et depile une couche a la fois', () => {
    const pile = empiler(empiler([], FOCUS), CARTE)
    expect(pile).toHaveLength(2)
    expect(sommet(pile)).toEqual(CARTE)
    expect(sommet(depiler(pile))).toEqual(FOCUS)
  })

  it('n\'empile pas deux fois la meme couche', () => {
    const pile = empiler(empiler([], FOCUS), FOCUS)
    expect(pile).toHaveLength(1)
  })

  it('ne modifie jamais la pile recue', () => {
    const depart: Couche[] = [FOCUS]
    empiler(depart, CARTE)
    depiler(depart)
    expect(depart).toEqual([FOCUS])
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- couches` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/couches.ts`**

```ts
// Les couches ouvertes par-dessus la vue d'etat, de la plus ancienne a la plus
// recente. Le retour d'Android ferme la couche du SOMMET, une a la fois : c'est
// pour cela qu'on tient une pile et pas un booleen par couche.
//
// La partie pure est ici et testee ; le hook ci-dessous la relie a l'historique
// du navigateur.

import { useCallback, useEffect, useState } from 'react'
import type { CleBande } from './bandes'

export type Couche =
  | { sorte: 'focus'; bande: CleBande }
  | { sorte: 'carte'; id: string }

function memeCouche(a: Couche, b: Couche): boolean {
  if (a.sorte !== b.sorte) return false
  if (a.sorte === 'focus' && b.sorte === 'focus') return a.bande === b.bande
  if (a.sorte === 'carte' && b.sorte === 'carte') return a.id === b.id
  return false
}

export function sommet(pile: Couche[]): Couche | undefined {
  return pile[pile.length - 1]
}

/** Empiler la couche deja au sommet ne fait rien : un double tap ne crée pas deux feuilles. */
export function empiler(pile: Couche[], couche: Couche): Couche[] {
  const haut = sommet(pile)
  if (haut && memeCouche(haut, couche)) return pile
  return [...pile, couche]
}

export function depiler(pile: Couche[]): Couche[] {
  return pile.slice(0, -1)
}

/**
 * Relie la pile a l'historique du navigateur : une entree par couche ouverte,
 * pour que le bouton retour d'Android ferme la feuille du dessus au lieu de
 * quitter la partie.
 */
export function useCouches(): {
  pile: Couche[]
  ouvrir: (couche: Couche) => void
  fermer: () => void
  toutFermer: () => void
} {
  const [pile, setPile] = useState<Couche[]>([])

  const ouvrir = useCallback((couche: Couche) => {
    setPile((precedente) => {
      const suivante = empiler(precedente, couche)
      if (suivante !== precedente) window.history.pushState({ couche: suivante.length }, '')
      return suivante
    })
  }, [])

  // Fermer se fait TOUJOURS par history.back() : le gestionnaire de popstate
  // ci-dessous est alors le seul endroit qui retire une couche, et la pile ne
  // peut pas se desynchroniser de l'historique.
  const fermer = useCallback(() => {
    window.history.back()
  }, [])

  const toutFermer = useCallback(() => {
    setPile((precedente) => {
      if (precedente.length > 0) window.history.go(-precedente.length)
      return precedente
    })
  }, [])

  useEffect(() => {
    const surRetour = () => setPile((precedente) => depiler(precedente))
    window.addEventListener('popstate', surRetour)
    return () => window.removeEventListener('popstate', surRetour)
  }, [])

  return { pile, ouvrir, fermer, toutFermer }
}
```

- [ ] **Step 4 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- couches` depuis `ui-app/`
Attendu : 4 tests verts.

- [ ] **Step 5 : Commit**

```bash
git add ui-app/src/board/mobile/couches.ts ui-app/src/board/mobile/couches.test.ts
git commit -m "feat(mobile): pile des couches reliee au retour d'Android"
```

---

### Task 6 : Répartition des joueurs dans `terrain-soutien`

`zones.ts` aplatit les aires de tous les joueurs dans un seul emplacement `terrain-soutien`, en groupes successifs. Le mode mobile a besoin de savoir quel groupe appartient à quel joueur pour n'en déplier qu'un. On ajoute un champ **additif** à `EmplacementAffiche` : le mode PC l'ignore, son rendu ne change pas.

**Files:**
- Modify: `ui-app/src/board/zones.ts`
- Create: `ui-app/src/board/mobile/joueurs.ts`
- Test: `ui-app/src/board/mobile/joueurs.test.ts`

**Interfaces:**
- Consomme : `EmplacementAffiche` (enrichi de `proprietaires?: number[]`).
- Produit : `groupesParJoueur(emplacement) => Map<number, UniteAffichee[][]>`, `ordreDAffichage(joueurs, actif) => number[]`.

- [ ] **Step 1 : Lire le code réel avant de le modifier**

Ouvrir `ui-app/src/board/zones.ts` autour de la ligne 512 (`emplacement('terrain-soutien', ...)`) et relever l'ordre exact des groupes produits : les groupes du joueur courant d'abord, puis ceux des autres joueurs, dans l'ordre de `world.players`. Le champ à ajouter doit refléter cet ordre, un identifiant de joueur par groupe.

- [ ] **Step 2 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/joueurs.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { groupesParJoueur, ordreDAffichage } from './joueurs'
import type { EmplacementAffiche } from '../zones'

const EMPLACEMENT: EmplacementAffiche = {
  cle: 'terrain-soutien',
  titre: 'Héros et soutiens',
  groupes: [[], [], [], [], [], []],
  nombreSurLaLigne: 0,
  proprietaires: [0, 0, 0, 1, 1, 1],
}

describe('groupesParJoueur', () => {
  it('range chaque groupe sous son joueur', () => {
    const par = groupesParJoueur(EMPLACEMENT)
    expect([...par.keys()]).toEqual([0, 1])
    expect(par.get(0)).toHaveLength(3)
    expect(par.get(1)).toHaveLength(3)
  })

  it('met tout sous le joueur 0 quand le champ est absent', () => {
    const par = groupesParJoueur({ ...EMPLACEMENT, proprietaires: undefined })
    expect([...par.keys()]).toEqual([0])
    expect(par.get(0)).toHaveLength(6)
  })
})

describe('ordreDAffichage', () => {
  it('met le joueur actif en premier', () => {
    expect(ordreDAffichage([0, 1, 2], 2)).toEqual([2, 0, 1])
  })

  it('ne bouge rien si l\'actif est inconnu', () => {
    expect(ordreDAffichage([0, 1, 2], 7)).toEqual([0, 1, 2])
  })
})
```

- [ ] **Step 3 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- joueurs` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable et propriété `proprietaires` inconnue.

- [ ] **Step 4 : Ajouter le champ additif dans `zones.ts`**

Dans le type `EmplacementAffiche` (vers la ligne 62), ajouter :

```ts
  /**
   * Identifiant du joueur proprietaire de chaque groupe, meme longueur que
   * `groupes`. Renseigne pour `terrain-soutien` seulement, ou les aires de tous
   * les joueurs sont aplaties. Le rendu PC l'ignore : c'est le mode mobile qui
   * s'en sert pour ne deplier qu'un joueur a la fois.
   */
  proprietaires?: number[]
```

Puis, à la construction de `terrain-soutien`, renseigner ce tableau avec un identifiant par groupe, dans le même ordre que les groupes.

- [ ] **Step 5 : Écrire `ui-app/src/board/mobile/joueurs.ts`**

```ts
// Qui possede quoi dans l'emplacement `terrain-soutien`.
//
// zones.ts y aplatit les aires de TOUS les joueurs en groupes successifs, parce
// que le plateau PC les pose cote a cote. Sur un telephone, un seul joueur est
// deplie a la fois : il faut donc pouvoir recoudre les groupes par joueur.

import type { EmplacementAffiche, UniteAffichee } from '../zones'

/**
 * Les groupes ranges par joueur, dans l'ordre ou zones.ts les a produits.
 * Sans le champ `proprietaires` (partie solo, ou emplacement d'un autre type),
 * tout revient au joueur 0 : le comportement reste celui d'avant.
 */
export function groupesParJoueur(
  emplacement: EmplacementAffiche
): Map<number, UniteAffichee[][]> {
  const par = new Map<number, UniteAffichee[][]>()
  emplacement.groupes.forEach((groupe, index) => {
    const joueur = emplacement.proprietaires?.[index] ?? 0
    const deja = par.get(joueur)
    if (deja) deja.push(groupe)
    else par.set(joueur, [groupe])
  })
  return par
}

/** Le joueur actif d'abord, les autres dans leur ordre d'origine. */
export function ordreDAffichage(joueurs: number[], actif: number): number[] {
  if (!joueurs.includes(actif)) return joueurs
  return [actif, ...joueurs.filter((joueur) => joueur !== actif)]
}
```

- [ ] **Step 6 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- joueurs` depuis `ui-app/`
Attendu : 4 tests verts.

- [ ] **Step 7 : Vérifier que le mode PC n'a pas bougé**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm test && npm run typecheck`
Attendu : tous les tests verts, typage propre. Le champ est purement additif : aucun rendu PC ne le lit.

- [ ] **Step 8 : Commit**

```bash
git add ui-app/src/board/zones.ts ui-app/src/board/mobile/joueurs.ts ui-app/src/board/mobile/joueurs.test.ts
git commit -m "feat(mobile): proprietaire de chaque groupe de terrain-soutien (champ additif)"
```

---

### Task 7 : La bande et la zone en focus

**Files:**
- Create: `ui-app/src/board/mobile/BandeMobile.tsx`
- Create: `ui-app/src/board/mobile/ZoneFocus.tsx`
- Modify: `ui-app/src/board/mobile/mobile.css`
- Test: `ui-app/src/board/mobile/BandeMobile.test.tsx`

**Interfaces:**
- Consomme : `BandeAffichee` de `./bandes`, `condenser` de `./condensation`, `TuileCondensee`, `ScanCard` de `../../components/ScanCard`.
- Produit : `BandeMobile` (props `{ bande, budget, onOuvrirBande, onOuvrirCarte }`), `ZoneFocus` (props `{ bande, onFermer, onOuvrirCarte }`).

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/BandeMobile.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BandeMobile } from './BandeMobile'
import type { BandeAffichee } from './bandes'
import type { ScanCardProps } from '../../components/ScanCard'

function carte(id: number): ScanCardProps {
  return { id: String(id), name: `Allié ${id}`, kind: 'ally', imageUrl: '' }
}

function bande(nombre: number): BandeAffichee {
  return {
    cle: 'terrain',
    titre: 'Terrain',
    emplacements: [
      {
        cle: 'terrain-combat',
        titre: 'Terrain',
        nombreSurLaLigne: nombre,
        groupes: [
          Array.from({ length: nombre }, (_, index) => ({
            cle: `u${index}`,
            carte: carte(index),
            attachees: [],
          })),
        ],
      },
    ],
  }
}

describe('BandeMobile', () => {
  it('montre son titre et ses tuiles', () => {
    render(
      <BandeMobile
        bande={bande(2)}
        budget={{ largeur: 464, hauteur: 200 }}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )
    expect(screen.getByText('Terrain')).toBeInTheDocument()
    expect(screen.getByText('Allié 0')).toBeInTheDocument()
  })

  it('replie le surplus dans une pastille qui ouvre la bande', () => {
    const ouvrir = vi.fn()
    render(
      <BandeMobile
        bande={bande(30)}
        budget={{ largeur: 464, hauteur: 72 }}
        onOuvrirBande={ouvrir}
        onOuvrirCarte={() => {}}
      />
    )
    const pastille = screen.getByRole('button', { name: /\+\d+/ })
    pastille.click()
    expect(ouvrir).toHaveBeenCalledOnce()
  })

  it('ouvre la carte touchee, pas la bande', () => {
    const ouvrirBande = vi.fn()
    const ouvrirCarte = vi.fn()
    render(
      <BandeMobile
        bande={bande(2)}
        budget={{ largeur: 464, hauteur: 200 }}
        onOuvrirBande={ouvrirBande}
        onOuvrirCarte={ouvrirCarte}
      />
    )
    screen.getByRole('button', { name: /Allié 1/ }).click()
    expect(ouvrirCarte).toHaveBeenCalledOnce()
    expect(ouvrirBande).not.toHaveBeenCalled()
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- BandeMobile` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/BandeMobile.tsx`**

```tsx
// Une bande de la vue d'etat : un titre, des tuiles condensees, et une pastille
// « +N » quand le budget ne suffit pas. La pastille ouvre la bande en focus :
// c'est la seule facon d'atteindre ce qui est replie, elle n'est jamais decorative.

import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { BandeAffichee } from './bandes'
import { condenser, type BudgetBande } from './condensation'
import { TuileCondensee } from './TuileCondensee'
import './mobile.css'

export type BandeMobileProps = {
  bande: BandeAffichee
  budget: BudgetBande
  onOuvrirBande: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

export function BandeMobile({
  bande,
  budget,
  onOuvrirBande,
  onOuvrirCarte,
}: BandeMobileProps) {
  const unites = bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
  const { tuiles, restantes, taille } = condenser(unites, budget)

  return (
    <section className="bande" aria-label={bande.titre}>
      <h2 className="bande-titre">{bande.titre}</h2>
      <div className="bande-tuiles">
        {tuiles.map((unite) => (
          <TuileCondensee
            key={unite.cle}
            carte={unite.carte}
            taille={taille}
            onOuvrir={() => onOuvrirCarte(unite.carte)}
          />
        ))}
        {restantes > 0 ? (
          <button
            type="button"
            className="bande-surplus"
            onClick={onOuvrirBande}
            data-tactile="surplus"
            aria-label={`${t('Voir les')} ${restantes} ${t('autres')}`}
          >
            +{restantes}
          </button>
        ) : null}
      </div>
    </section>
  )
}
```

- [ ] **Step 4 : Écrire `ui-app/src/board/mobile/ZoneFocus.tsx`**

```tsx
// Le niveau 2 : une bande ouverte en feuille par-dessus la vue d'etat, cartes a
// 149 px de large. C'est la qu'on lit et qu'on agit.
//
// 149 px vient du calcul de la spec : a 480 px de large, (480 - 20 de marges
// - 12 d'ecarts) / 3 = 149. Trois cartes par rangee, chacune tres au-dessus des
// 44 px de cible tactile.

import { t } from '../langue'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import type { BandeAffichee } from './bandes'
import './mobile.css'

export type ZoneFocusProps = {
  bande: BandeAffichee
  onFermer: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

export function ZoneFocus({ bande, onFermer, onOuvrirCarte }: ZoneFocusProps) {
  return (
    <div className="focus-voile" onPointerDown={onFermer}>
      <section
        className="focus"
        role="dialog"
        aria-label={bande.titre}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <header className="focus-entete">
          <span className="focus-poignee" aria-hidden="true" />
          <h2>{bande.titre}</h2>
          <button type="button" className="focus-fermer" onClick={onFermer} data-tactile="fermer">
            {t('Fermer')}
          </button>
        </header>
        <div className="focus-cartes">
          {bande.emplacements.flatMap((emplacement) =>
            emplacement.groupes.flat().map((unite) => (
              <ScanCard
                key={unite.cle}
                {...unite.carte}
                onSelect={() => onOuvrirCarte(unite.carte)}
              />
            ))
          )}
        </div>
      </section>
    </div>
  )
}
```

- [ ] **Step 5 : Ajouter leurs styles à `mobile.css`**

À la suite du fichier créé en Task 4 :

```css
@layer composants {
  /* --- Bande de la vue d'etat --------------------------------------------- */

  .bande {
    display: grid;
    gap: 4px;
    min-height: 0;
    padding: 6px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .bande-titre {
    margin: 0;
    font-size: 0.66rem;
    font-weight: 800;
    text-transform: uppercase;
    color: #ffd45a;
  }

  .bande-tuiles {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-height: 0;
    /* Le niveau 1 ne defile JAMAIS : ce qui deborde est replie par condenser(),
       pas cache par un overflow. Le masquage est un filet, pas le mecanisme. */
    overflow: hidden;
  }

  .bande-surplus {
    min-width: 64px;
    min-height: 64px;
    font: inherit;
    font-size: 0.9rem;
    font-weight: 900;
    color: #ffd45a;
    background: rgba(255, 212, 90, 0.1);
    border: 1px dashed rgba(255, 212, 90, 0.45);
    border-radius: 10px;
    cursor: pointer;
  }

  /* --- Zone en focus (niveau 2) ------------------------------------------- */

  .focus-voile {
    position: fixed;
    inset: 0;
    z-index: 40;
    background: rgba(0, 0, 0, 0.62);
  }

  .focus {
    position: absolute;
    inset: auto 0 0 0;
    display: grid;
    grid-template-rows: auto 1fr;
    max-height: 88dvh;
    /* La barre gestuelle d'Android mange le bas de l'ecran : sans cela, le
       dernier rang de cartes est sous le doigt du systeme. */
    padding-bottom: env(safe-area-inset-bottom, 0px);
    background: #12141b;
    border-radius: 16px 16px 0 0;
  }

  .focus-entete {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }

  .focus-poignee {
    width: 36px;
    height: 4px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.3);
  }

  .focus-entete h2 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 800;
  }

  .focus-fermer {
    margin-left: auto;
    min-width: 44px;
    min-height: 44px;
    font: inherit;
    font-weight: 700;
    color: #e8e9ee;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 8px;
    cursor: pointer;
  }

  .focus-cartes {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 10px;
    overflow-y: auto;
  }
}

@layer utilitaires {
  /* Le niveau 2 fixe la largeur de carte : 3 par rangee a 480 px de large.
     Contrairement a board.css, ce rendu n'est PAS mis a l'echelle, donc la
     valeur est un vrai pixel CSS. */
  .focus-cartes .scan-card {
    --card-w: 149px;
    --inspect-scale: 1;
  }

  .focus-cartes .scan-card.is-landscape {
    --card-w: 212px;
  }
}
```

- [ ] **Step 6 : Lancer les tests pour vérifier qu'ils passent**

Run : `npm test -- BandeMobile` depuis `ui-app/`
Attendu : 3 tests verts.

- [ ] **Step 7 : Commit**

```bash
git add ui-app/src/board/mobile/BandeMobile.tsx ui-app/src/board/mobile/ZoneFocus.tsx ui-app/src/board/mobile/BandeMobile.test.tsx ui-app/src/board/mobile/mobile.css
git commit -m "feat(mobile): bande condensee et zone en focus a 149 px"
```

---

### Task 8 : `PlateauMobile`, le niveau 1 complet

**Files:**
- Create: `ui-app/src/board/mobile/PlateauMobile.tsx`
- Modify: `ui-app/src/board/mobile/mobile.css`
- Test: `ui-app/src/board/mobile/PlateauMobile.test.tsx`

**Interfaces:**
- Consomme : `BoardProps` de `../Board` (mêmes props, pour être interchangeable), `repartir` de `./bandes`, `useCouches` de `./couches`, `BandeMobile`, `ZoneFocus`, `groupesParJoueur` et `ordreDAffichage` de `./joueurs`.
- Produit : `PlateauMobile` acceptant exactement `BoardProps`. C'est ce qui permet à `board.tsx` de choisir l'un ou l'autre sans adapter ses props.

- [ ] **Step 1 : Écrire les tests (ils doivent échouer)**

Créer `ui-app/src/board/mobile/PlateauMobile.test.tsx`. Les props minimales suffisent : le test vérifie la structure, pas le contenu de jeu.

```tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { PlateauMobile } from './PlateauMobile'
import type { Plateau } from '../zones'
import type { World } from '../world'

const MONDE = {
  phase: 'Player 1 Turn',
  round: 3,
  prompt: '',
  players: [],
} as unknown as World

const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'rencontre',
      titre: 'Méchant',
      nombreSurLaLigne: 1,
      groupes: [
        [
          {
            cle: 'v',
            carte: { id: '1', name: 'Rhino', kind: 'villain', imageUrl: '', allyHp: '12/22' },
            attachees: [],
          },
        ],
      ],
    },
  ],
  nombreDeCartes: 1,
  idsAffiches: new Set<number>([1]),
  representantsDePile: new Map<number, number>(),
  nombreIgnore: 0,
}

describe('PlateauMobile', () => {
  it('montre le HUD et les bandes peuplees', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.getByText('Méchant')).toBeInTheDocument()
    expect(screen.getByText('Rhino')).toBeInTheDocument()
  })

  it('ne dessine aucune bande vide', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.queryByText('Manigances')).not.toBeInTheDocument()
    expect(screen.queryByText('Ta main')).not.toBeInTheDocument()
  })

  it('ouvre la bande en focus au tap sur son titre', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    screen.getByRole('button', { name: /Méchant/ }).click()
    expect(screen.getByRole('dialog', { name: 'Méchant' })).toBeInTheDocument()
  })
})
```

- [ ] **Step 2 : Lancer les tests pour vérifier qu'ils échouent**

Run : `npm test -- PlateauMobile` depuis `ui-app/`
Attendu : ÉCHEC, module introuvable.

- [ ] **Step 3 : Écrire `ui-app/src/board/mobile/PlateauMobile.tsx`**

```tsx
// Le niveau 1 : la vue d'etat. Elle tient TOUJOURS a l'ecran, en entier, et ne
// defile jamais. Ce n'est pas le plateau en petit, c'est l'etat de la partie en
// objets condenses.
//
// Elle accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import { useMemo, useRef, useState } from 'react'
import { phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import { BandeMobile } from './BandeMobile'
import { repartir, type CleBande } from './bandes'
import { useCouches } from './couches'
import { ZoneFocus } from './ZoneFocus'
import './mobile.css'

/** Hauteurs de repos de la spec, en pixels CSS. La condensation fait le reste. */
const BUDGETS: Record<CleBande, number> = {
  vilain: 140,
  complots: 110,
  terrain: 120,
  rencontre: 64,
  heros: 200,
  main: 76,
}

/** Largeur utile d'une bande : la fenetre moins les marges laterales de mobile.css. */
const MARGES_LATERALES = 20

export function PlateauMobile({
  world,
  plateau,
  outils,
  actionsPartie,
  bas,
  onCardClick,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const [largeur, setLargeur] = useState(() => window.innerWidth)
  const { pile, ouvrir, fermer } = useCouches()

  const bandes = useMemo(() => repartir(plateau), [plateau])

  const couche = pile[pile.length - 1]
  const bandeEnFocus =
    couche?.sorte === 'focus' ? bandes.find((bande) => bande.cle === couche.bande) : undefined

  const ouvrirCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }

  return (
    <div className="plateau-mobile" ref={cadre}>
      <header className="pm-hud">
        <span className="pm-etat">
          <strong>{phaseAffichee(world.phase)}</strong>
          <span className="pm-tour">
            {t('Tour')} {world.round}
          </span>
        </span>
        <span className="pm-outils">
          {actionsPartie}
          {outils}
        </span>
      </header>

      <div className="pm-bandes">
        {bandes.map((bande) => (
          <BandeMobile
            key={bande.cle}
            bande={bande}
            budget={{
              largeur: Math.max(0, largeur - MARGES_LATERALES),
              hauteur: BUDGETS[bande.cle],
            }}
            onOuvrirBande={() => ouvrir({ sorte: 'focus', bande: bande.cle })}
            onOuvrirCarte={ouvrirCarte}
          />
        ))}
      </div>

      {bas ? <div className="pm-barre-action">{bas}</div> : null}

      {bandeEnFocus ? (
        <ZoneFocus bande={bandeEnFocus} onFermer={fermer} onOuvrirCarte={ouvrirCarte} />
      ) : null}
    </div>
  )
}
```

Note pour l'implémenteur : `setLargeur` est appelé par un `ResizeObserver` sur `cadre`, sur le modèle exact de `useEchelle` dans `Board.tsx:83-112`. Recopier ce motif plutôt que d'écouter `window.resize`, qui ne voit pas les changements de mise en page.

- [ ] **Step 4 : Rendre le titre de bande touchable**

Dans `BandeMobile.tsx`, le titre doit ouvrir la bande en focus (le test de l'étape 1 le vérifie). Remplacer le `<h2>` par :

```tsx
      <button
        type="button"
        className="bande-titre"
        onClick={onOuvrirBande}
        data-tactile="titre-bande"
      >
        {bande.titre}
      </button>
```

Et dans `mobile.css`, ajouter à la règle `.bande-titre` :

```css
    min-height: 44px;
    font: inherit;
    text-align: left;
    background: none;
    border: 0;
    cursor: pointer;
```

- [ ] **Step 5 : Ajouter les styles du niveau 1 à `mobile.css`**

```css
@layer composants {
  .plateau-mobile {
    display: grid;
    grid-template-rows: auto 1fr auto;
    /* 100dvh et non 100vh : sur Chrome mobile la barre d'URL apparait et
       disparait, et 100vh laisserait le bas du plateau sous elle. */
    height: 100dvh;
    padding-top: env(safe-area-inset-top, 0px);
    /* La vue d'etat ne defile JAMAIS. Si quelque chose deborde, c'est un bug de
       condensation, pas une raison d'ajouter une barre de defilement. */
    overflow: hidden;
  }

  .pm-hud {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 52px;
    padding: 6px 10px;
    background: rgba(10, 12, 16, 0.94);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }

  .pm-etat {
    display: grid;
    min-width: 0;
    line-height: 1.2;
  }

  .pm-etat strong {
    overflow: hidden;
    font-size: 0.9rem;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .pm-tour {
    font-size: 0.66rem;
    font-weight: 800;
    text-transform: uppercase;
    color: #ffd45a;
  }

  .pm-outils {
    display: flex;
    gap: 6px;
    margin-left: auto;
  }

  .pm-bandes {
    display: grid;
    align-content: start;
    min-height: 0;
    overflow: hidden;
  }

  .pm-barre-action {
    padding: 8px 10px calc(8px + env(safe-area-inset-bottom, 0px));
    background: rgba(10, 12, 16, 0.96);
    border-top: 1px solid rgba(255, 255, 255, 0.14);
  }
}
```

- [ ] **Step 6 : Lancer les tests pour vérifier qu'ils passent**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm test`
Attendu : tous les tests verts, dont les 3 de `PlateauMobile`.

- [ ] **Step 7 : Commit**

```bash
git add ui-app/src/board/mobile/
git commit -m "feat(mobile): vue d'etat non defilante, HUD et bandes"
```

---

### Task 9 : Câblage dans `board.tsx` et réglage ⚙

**Files:**
- Modify: `ui-app/src/board.tsx`

**Interfaces:**
- Consomme : `useModeMobile` de `./board/mobile/useModeMobile`, `PlateauMobile` de `./board/mobile/PlateauMobile`.
- Produit : rien de nouveau. `board.tsx` monte `Board` ou `PlateauMobile` selon le mode.

- [ ] **Step 1 : Repérer le point de montage**

Ouvrir `ui-app/src/board.tsx` et localiser l'endroit où `<Board ... />` est rendu (l'import est en ligne 28). Relever la liste exacte des props passées : elles seront passées à l'identique au composant mobile, qui accepte les mêmes `BoardProps`.

- [ ] **Step 2 : Remplacer le montage par un choix de composant**

```tsx
const { mode, reglage, changer } = useModeMobile()
const Rendu = mode === 'mobile' ? PlateauMobile : Board
// ...
<Rendu {...proprietesDuPlateau} />
```

Les `proprietesDuPlateau` sont exactement celles déjà passées à `<Board>` : ne rien ajouter, ne rien retirer.

- [ ] **Step 3 : Ajouter le réglage dans le panneau ⚙**

Le panneau d'options utilise déjà des lignes `.ligne-option` avec un état à droite (voir `board.css`, règle `.ligne-option-etat`). Ajouter une ligne qui fait tourner les trois états :

```tsx
<button
  type="button"
  className="ligne-option"
  onClick={() => changer(reglage === 'auto' ? 'mobile' : reglage === 'mobile' ? 'pc' : 'auto')}
>
  {t('Disposition')}
  <span className="ligne-option-etat">
    {reglage === 'auto' ? t('Automatique') : reglage === 'mobile' ? t('Mobile') : t('Ordinateur')}
  </span>
</button>
```

- [ ] **Step 4 : Vérifier le typage et les tests**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm run typecheck`
Attendu : aucune sortie, code de retour 0. Si `PlateauMobile` refuse une prop de `Board`, c'est que sa signature a divergé de `BoardProps` : corriger `PlateauMobile`, jamais le site d'appel.

Run : `npm test`
Attendu : tous les tests verts.

- [ ] **Step 5 : Vérifier à l'œil dans le navigateur**

Lancer le serveur de dev Vite depuis `ui-app/` (`npx vite`), ouvrir `board.html?etat=rhino__spider_man__debut-de-tour.js` dans Chrome, ouvrir les outils de développement, activer l'émulation d'appareil en 480x1050 avec pointeur grossier. Attendu : la vue d'état s'affiche en entier, sans barre de défilement verticale sur `.plateau-mobile`. Le réglage ⚙ « Disposition » fait basculer entre les deux rendus sans rechargement.

- [ ] **Step 6 : Commit**

```bash
git add ui-app/src/board.tsx
git commit -m "feat(mobile): board.tsx choisit le rendu selon le mode, reglage dans le panneau options"
```

---

### Task 10 : Équivalents tactiles des survols

Quatre `onMouseEnter` pilotent aujourd'hui l'aperçu et la mise en avant d'options. Au doigt, ils ne se déclenchent jamais.

**Files:**
- Modify: `ui-app/src/board/MenuActionsCarte.tsx:594`, `:674`
- Modify: `ui-app/src/board/SelecteurCibles.tsx:39`
- Modify: `ui-app/src/board/DemandeCentrale.tsx:189`

- [ ] **Step 1 : Relever ce que fait chaque survol**

Pour chacun des quatre sites, noter la fonction appelée (`activerOption(option)` pour trois d'entre eux, `survoler?.(cible.props)` pour `SelecteurCibles`) et ce qu'elle change à l'écran.

- [ ] **Step 2 : Ajouter le déclencheur tactile à côté du survol**

Sur chaque élément concerné, ajouter `onFocus` avec le même effet que `onMouseEnter`, et rendre l'élément focalisable s'il ne l'est pas déjà (`tabIndex={0}` sur un élément non interactif). Un tap sur un `<button>` lui donne le focus : le même code sert alors au doigt et au clavier, sans geste nouveau.

```tsx
onMouseEnter={() => activerOption(option)}
onFocus={() => activerOption(option)}
```

- [ ] **Step 3 : Vérifier que le mode PC n'a pas changé**

Run : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm run typecheck && npm test`
Attendu : vert. `onFocus` s'ajoute au survol, il ne le remplace pas : le comportement souris est inchangé.

- [ ] **Step 4 : Commit**

```bash
git add ui-app/src/board/MenuActionsCarte.tsx ui-app/src/board/SelecteurCibles.tsx ui-app/src/board/DemandeCentrale.tsx
git commit -m "feat(mobile): equivalent tactile et clavier des quatre survols du plateau"
```

---

### Task 11 : Le filet Playwright, gabarit S24 et géométrie

Les tests unitaires prouvent les règles ; seul un vrai navigateur prouve que rien ne déborde et que les cibles font 44 px.

**Files:**
- Modify: `ui-check/playwright.config.ts`
- Create: `ui-check/tests/plateau-mobile.spec.ts`
- Modify: `ui-check/package.json`

**Interfaces:**
- Consomme : les 34 fixtures de `public/js/fixtures/`, chargées par `/app/board.html?etat=<fichier>`.
- Produit : le script `npm run plateau-mobile` dans `ui-check/`.

- [ ] **Step 1 : Ajouter le gabarit S24 dans `ui-check/playwright.config.ts`**

Dans l'objet `GABARITS`, ajouter :

```ts
  // Samsung S24 Ultra en portrait, l'appareil de reference du plateau mobile.
  s24: { width: 480, height: 1050 },
```

Puis, dans la liste `projects`, déclarer le projet correspondant avec le pointeur grossier et le tactile, qui sont ce que le code teste réellement :

```ts
    {
      name: 's24',
      use: {
        viewport: GABARITS.s24,
        hasTouch: true,
        isMobile: true,
        deviceScaleFactor: 1,
      },
    },
```

`deviceScaleFactor` reste à 1 comme les autres gabarits : les PNG pèseraient neuf fois plus lourd sans rien prouver de plus.

- [ ] **Step 2 : Déclarer le script npm**

Dans `ui-check/package.json`, dans `scripts` (une commande unique) :

```json
"plateau-mobile": "playwright test tests/plateau-mobile.spec.ts --project=s24"
```

- [ ] **Step 3 : Écrire le test**

Créer `ui-check/tests/plateau-mobile.spec.ts` :

```ts
// Le plateau mobile tient-il vraiment a l'ecran, et se joue-t-il au doigt ?
//
// Deux affirmations, verifiees sur les 34 etats enregistres :
//   1. la vue d'etat ne deborde JAMAIS (c'est toute la promesse du modele) ;
//   2. toute cible tactile mesure au moins 44 px dans les deux axes.
//
//   npm run plateau-mobile
//
// La page est ouverte avec ?etat=<fixture> : aucune partie n'a besoin de tourner.
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;

type Entree = { fichier: string; titre: string };

test('La vue d\'etat tient a l\'ecran et se joue au doigt', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });
  expect(await page.title()).not.toBe(TITRE_PAGE_AVERTISSEMENT);

  const catalogue: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );
  expect(catalogue.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);

  for (const entree of catalogue) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });

      const vue = page.locator('.plateau-mobile');
      await expect(vue, 'Le rendu mobile ne s\'est pas monte').toBeVisible();

      // 1. Rien ne deborde : la hauteur de contenu ne depasse pas la hauteur visible.
      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `La vue d'etat deborde de ${debordement.contenu - debordement.visible} px : la condensation n'a pas suffi`
      ).toBeLessThanOrEqual(debordement.visible);

      // 2. Toute cible tactile respecte le plancher de 44 px.
      const cibles = page.locator('[data-tactile]');
      const nombre = await cibles.count();
      for (let index = 0; index < nombre; index += 1) {
        const boite = await cibles.nth(index).boundingBox();
        if (!boite) continue;
        expect(
          Math.min(boite.width, boite.height),
          `Cible tactile trop petite (${Math.round(boite.width)}x${Math.round(boite.height)})`
        ).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      }
    });
  }

  expect(erreurs, `Erreurs signalees par le navigateur :\n${erreurs.join('\n')}`).toHaveLength(0);
});
```

- [ ] **Step 4 : Déployer avant de tester**

Le test vise le jeu servi, pas le serveur Vite : il faut donc déployer d'abord.

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
```

Attendu : build vert, garde-fou d'extensions vert, recopie vers `public/app/`.

- [ ] **Step 5 : Lancer le test et corriger ce qu'il trouve**

Vérifier d'abord que le serveur de développement tourne sur 2346 (voir `.planning/STATE.md`, points de vigilance), puis :

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE
npm run plateau-mobile
```

Attendu au premier passage : des échecs sur certains états. C'est le but du test. Chaque débordement se corrige dans `condensation.ts` ou dans les budgets de `PlateauMobile.tsx`, **jamais** en ajoutant un `overflow: auto` à `.plateau-mobile` ni en abaissant `CIBLE_MINIMUM`.

- [ ] **Step 6 : Vérifier que les références PC restent vertes**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
npm run captures
```

Attendu : toutes les références existantes vertes. Une seule qui bouge signifie que le mode PC a été touché, ce que ce plan interdit.

- [ ] **Step 7 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ../ui-check/playwright.config.ts ../ui-check/package.json ../ui-check/tests/plateau-mobile.spec.ts
git commit -m "test(mobile): gabarit S24, non-debordement et cibles 44px sur les 34 etats"
```

---

### Task 12 : Livraison et vérification d'ensemble

**Files:**
- Aucun fichier source. C'est le rituel de livraison du projet.

- [ ] **Step 1 : Déployer la version finale**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
```

Attendu : build vert, garde-fou d'extensions vert, empreintes recalculées.

- [ ] **Step 2 : Vérifier la non-régression du moteur**

Lancer l'autoplay selon la recette de `.planning/STATE.md` (dossier de jeu `.game`, `RELEASE=1` posée avant tout import, `winsound` fourni par `PYTHONPATH`).
Attendu : zéro traceback.

- [ ] **Step 3 : Jouer une partie solo complète depuis le téléphone**

Lancer une partie solo depuis un PC, puis ouvrir le plateau sur le S24 Ultra. Jouer jusqu'à la fin.

À vérifier pendant la partie, c'est la definition of done de la spec :
1. On ne zoome jamais.
2. La vue d'état ne défile jamais.
3. Chaque carte à jouer s'atteint en un tap ou deux.
4. La barre d'action reste visible tant que le moteur attend une réponse.
5. Le retour d'Android ferme la feuille du dessus et ne quitte jamais la partie.

- [ ] **Step 4 : Vérifier que la sortie de secours fonctionne toujours**

Ouvrir une page migrée avec la bascule `?ui=old` et vérifier que l'ancienne version se charge.

- [ ] **Step 5 : Consigner les décisions**

Ajouter dans `.planning/STATE.md`, section « Décisions », les points appris pendant l'implémentation : valeurs de budget retenues par bande, états de fixtures qui ont demandé une correction de condensation, pièges rencontrés.

- [ ] **Step 6 : Commit**

```bash
git add .planning/STATE.md
git commit -m "chore(mobile): livraison du plateau mobile, decisions consignees"
```

---

## Auto-revue

**Couverture de la spec :**

| Section de la spec | Tâche |
|---|---|
| §4 Architecture (rendu alternatif, réutilisation) | Tâches 8 et 9 |
| §5 Niveau 1, vue d'état | Tâches 3, 4, 7, 8 |
| §5 Niveau 2, zone en focus | Tâche 7 |
| §5 Règle de condensation | Tâches 1 et 6 |
| §5 Ciblage par `SelecteurCibles` | Tâche 10 (réutilisation du composant existant) |
| §6 Gestes, cibles 44 px, zones sûres | Tâches 4, 7, 10, 11 |
| §6 Retour Android et pile de couches | Tâche 5 |
| §7 Plusieurs joueurs, un seul déplié | Tâche 6 |
| §8 Bascule à trois états | Tâches 2 et 9 |
| §9 Filet, gabarit S24, 34 fixtures | Tâche 11 |
| §10 Definition of done | Tâche 12 |

**Réserve connue :** la tâche 6 pose la répartition par joueur, mais le repliement effectif des joueurs non actifs en bandeaux de 44 px se fait dans `PlateauMobile` (tâche 8) et n'a pas de test unitaire dédié : il est couvert par le test de non-débordement de la tâche 11, sur les fixtures multi-héros. Si une fixture à plusieurs joueurs déborde, c'est le signal qu'il manque une tâche de repliement à part entière.

**Cohérence des types :** `BandeCondensee`, `Taille`, `BudgetBande` (tâche 1) sont consommés tels quels par `BandeMobile` (tâche 7) et `TuileCondensee` (tâche 4). `CleBande` (tâche 3) est consommé par `couches.ts` (tâche 5) et `PlateauMobile` (tâche 8). `PlateauMobile` accepte `BoardProps` (tâche 8), ce que la tâche 9 vérifie au typage.
