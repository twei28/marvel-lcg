# Plateau paysage (sous-projet 1 du parcours solo mobile) : plan d'implémentation

> ⚠ **Plan exécuté le 07/09/2026 (22 commits, b60ba9fe..a3c84357), puis modèle abandonné le soir même** après le premier terrain : la spec est passée en version 2 (portrait, quatre rangées). Ce plan reste comme trace ; le suivant est `2026-09-07-plateau-portrait.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sur un téléphone tenu en paysage, le plateau montre deux rangées de vraies cartes (ennemie, héros) avec piles épinglées, main en éventail et barre basse ; en portrait, un écran couvre le plateau et demande de tourner l'appareil.

**Architecture:** Le mode mobile reste un rendu alternatif des mêmes objets : `board.tsx` monte `PlateauMobile` au lieu de `Board` selon `useModeMobile()`, avec les mêmes `BoardProps`. `PlateauMobile` devient un aiguillage : `PlateauPaysage` (nouveau, deux rangées de `ScanCard`) par défaut, `PlateauMedaillons` (l'ancien composant, renommé) derrière `?medaillons` pour comparer sur le téléphone jusqu'à sa suppression au sous-projet 3. Les modules purs (répartition en rangées, taille de carte, états, hors-champ, plein écran) sont testés sous vitest ; le rendu réel est mesuré par Playwright sur les 34 états enregistrés en 1050 x 480.

**Tech Stack:** React 19, TypeScript 6, Vite 8, vitest 3 + Testing Library (jsdom), Playwright 1.62 (`ui-check`). Zéro dépendance ajoutée.

**Spec:** `docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md` (§4, §5, §7.1 côté plateau).

## Global Constraints

- Aucune ligne de `ui-app/src/board/Board.tsx`, de `board.css` ni du moteur Python n'est modifiée (spec §2).
- `ScanCard`, `card-model.ts`, `zones.ts`, `interaction.ts`, `world.ts`, `SelecteurCibles`, `MenuActionsCarte`, `HistoriquePartie`, `DeroulePhase` sont utilisés sans modification (spec §5.2).
- Largeur de carte : `clamp(84px, (100dvh - 166px) / 2 * 63 / 88, 150px)` (spec §4.2). Plancher 84 px, plafond 150 px.
- Toute cible tactile mesure au moins 44 px dans les deux axes (spec §7.1).
- Textes en français passés à `t()` ; chaque nouveau texte reçoit sa traduction dans `dico-en.ts`.
- Pas de tiret cadratin ni de tiret parenthétique dans les textes et commentaires.
- Commits atomiques, un par tâche, message en français au format `feat(plateau-mobile): ...` / `test(...)` / `refactor(...)`, terminés par les deux lignes d'attribution de la session.
- Commandes : `cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"` puis `npx vitest run <fichier>` ; types : `npx tsc --noEmit`.
- Les médaillons (`Medaillon.tsx`, `RangeeMedaillons.tsx`, `TiroirPiles.tsx`, `ZoneFocus.tsx`, `medaillon.css`, `bandes.ts`) ne sont PAS supprimés dans ce plan (spec §4.9 : après la partie terrain, sous-projet 3).

---

## Structure des fichiers

| Fichier | Rôle |
|---|---|
| `ui-app/src/board/mobile/PlateauMedaillons.tsx` | Renommage de l'actuel `PlateauMobile.tsx`, sans changement de contenu autre que le nom exporté |
| `ui-app/src/board/mobile/PlateauMedaillons.test.tsx` | Renommage de l'actuel `PlateauMobile.test.tsx` |
| `ui-app/src/board/mobile/PlateauMobile.tsx` | Aiguillage : `?medaillons` rend l'ancien, sinon `PlateauPaysage` |
| `ui-app/src/board/mobile/rangees.ts` (+ test) | Les 12 emplacements de `zones.ts` rangés en deux rangées (défilants, épinglés) plus la main |
| `ui-app/src/board/mobile/taille-carte.ts` (+ test) | La formule de largeur de carte, en fonction pure |
| `ui-app/src/board/mobile/etats.ts` (+ test) | La table des états (coriace, sonné, désorienté), sortie du médaillon |
| `ui-app/src/board/mobile/hors-champ.ts` (+ test) | Combien de cartes d'une rangée sont hors du champ visible |
| `ui-app/src/board/mobile/plein-ecran.ts` (+ test) | Règles pures du plein écran et hook au premier geste |
| `ui-app/src/board/mobile/CartePosee.tsx` (+ test) | Une carte posée : `ScanCard` réel, états en pastilles, améliorations glissées derrière, tap qui ouvre |
| `ui-app/src/board/mobile/PilesEpinglees.tsx` (+ test) | Deck et défausse en dos réduit avec compte, tap qui étale la pile |
| `ui-app/src/board/mobile/RangeeCartes.tsx` (+ test) | Une rangée : étiquette, zone défilante, voile « +N », piles épinglées, recalage sur la première cible |
| `ui-app/src/board/mobile/EcranPortrait.tsx` (+ test) | Le voile « Tourne ton téléphone » |
| `ui-app/src/board/mobile/PlateauPaysage.tsx` (+ test) | La composition : deux rangées, main, barre, carte ouverte, pile regardée, écran portrait |
| `ui-app/src/board/mobile/paysage.css` | Les styles du nouveau plateau. `medaillon.css` reste chargé pour la main, la barre et la carte ouverte |
| `ui-app/src/board/dico-en.ts` | Traductions des nouveaux textes |
| `ui-check/tests/plateau-paysage.spec.ts` | Le filet Playwright en 1050 x 480 et le contrôle de l'écran portrait |
| `ui-check/playwright.config.ts`, `ui-check/package.json` | Projet `s24-paysage`, script `plateau-paysage` |
| `ui-check/tests/plateau-mobile.spec.ts` | Une ligne : l'URL gagne `&medaillons` pour continuer à tester l'ancien rendu |

---

### Task 1 : Mettre l'ancien plateau de côté sous le nom PlateauMedaillons

**Files:**
- Rename: `ui-app/src/board/mobile/PlateauMobile.tsx` → `ui-app/src/board/mobile/PlateauMedaillons.tsx`
- Rename: `ui-app/src/board/mobile/PlateauMobile.test.tsx` → `ui-app/src/board/mobile/PlateauMedaillons.test.tsx`
- Create: `ui-app/src/board/mobile/PlateauMobile.tsx`
- Modify: `ui-check/tests/plateau-mobile.spec.ts:44`

**Interfaces:**
- Produces: `export function PlateauMedaillons(props: BoardProps)` (l'ancien composant, inchangé) et `export function PlateauMobile(props: BoardProps)` (aiguillage). `board.tsx` continue d'importer `PlateauMobile` depuis `./board/mobile/PlateauMobile` sans modification.

- [ ] **Step 1 : Renommer les deux fichiers avec git**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app/src/board/mobile"
git mv PlateauMobile.tsx PlateauMedaillons.tsx
git mv PlateauMobile.test.tsx PlateauMedaillons.test.tsx
```

- [ ] **Step 2 : Renommer le composant dans les deux fichiers**

Dans `PlateauMedaillons.tsx`, remplacer la ligne `export function PlateauMobile({` par `export function PlateauMedaillons({`. Ajouter en tête du commentaire d'en-tête (première ligne du fichier) :

```ts
// ⚠ ANCIEN MODELE (medaillons, portrait). Conserve derriere `?medaillons` pour
// comparer sur le telephone, jusqu'a sa suppression au sous-projet 3 de
// docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md (§4.9).
// Le rendu par defaut est PlateauPaysage.tsx.
```

Dans `PlateauMedaillons.test.tsx`, remplacer `import { PlateauMobile } from './PlateauMobile'` par `import { PlateauMedaillons } from './PlateauMedaillons'`, `describe('PlateauMobile'` par `describe('PlateauMedaillons'`, et chaque `<PlateauMobile` par `<PlateauMedaillons` :

```bash
sed -i "s/import { PlateauMobile } from '.\/PlateauMobile'/import { PlateauMedaillons } from '.\/PlateauMedaillons'/; s/describe('PlateauMobile'/describe('PlateauMedaillons'/; s/<PlateauMobile\b/<PlateauMedaillons/g" PlateauMedaillons.test.tsx
grep -c "PlateauMobile" PlateauMedaillons.test.tsx
```

Attendu : `0`.

- [ ] **Step 3 : Écrire le nouvel aiguillage `PlateauMobile.tsx`**

```tsx
// Le plateau sur un telephone : l'aiguillage entre les deux rendus.
//
// Par defaut, PlateauPaysage : deux rangees de vraies cartes, paysage
// obligatoire (spec du 07/09/2026). L'ancien modele a medaillons reste
// atteignable par `?medaillons` dans l'adresse, pour le comparer sur un vrai
// telephone jusqu'a sa suppression (sous-projet 3). Lu a chaque rendu, sans
// etat : on ne memorise rien qui puisse enfermer quelqu'un, meme regle que
// `?mobile` dans useModeMobile.ts.
//
// Il accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import type { BoardProps } from '../Board'
import { PlateauMedaillons } from './PlateauMedaillons'

export function veutLesMedaillons(recherche: string): boolean {
  return new URLSearchParams(recherche).has('medaillons')
}

export function PlateauMobile(props: BoardProps) {
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  // PlateauPaysage arrive a la tache 11 ; d'ici la, l'ancien rendu reste le seul.
  return <PlateauMedaillons {...props} />
}
```

- [ ] **Step 4 : Faire pointer le filet Playwright de l'ancien rendu sur `?medaillons`**

Dans `ui-check/tests/plateau-mobile.spec.ts`, remplacer :

```ts
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
```

par :

```ts
      // `medaillons` : l'ancien rendu, que ce filet continue de mesurer
      // jusqu'a sa suppression (sous-projet 3 de la spec du 07/09/2026).
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}&medaillons`, {
```

- [ ] **Step 5 : Vérifier types et tests**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx tsc --noEmit && npx vitest run src/board/mobile
```

Attendu : `tsc` silencieux, tous les tests du dossier `mobile` verts (même nombre qu'avant le renommage).

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/PlateauMedaillons.tsx ui-app/src/board/mobile/PlateauMedaillons.test.tsx ui-app/src/board/mobile/PlateauMobile.tsx ui-check/tests/plateau-mobile.spec.ts
git commit -m "refactor(plateau-mobile): l'ancien rendu a medaillons passe derriere ?medaillons

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 2 : rangees.ts, les 12 emplacements en deux rangées

**Files:**
- Create: `ui-app/src/board/mobile/rangees.ts`
- Test: `ui-app/src/board/mobile/rangees.test.ts`

**Interfaces:**
- Consumes: `CleEmplacement`, `EmplacementAffiche`, `Plateau`, `UniteAffichee` de `../zones` ; `t` de `../langue`.
- Produces:
  - `type CleRangee = 'ennemie' | 'heros'`
  - `RANGEES: Array<{ cle: CleRangee; titre: () => string; defilants: CleEmplacement[]; epingles: CleEmplacement[] }>`
  - `EMPLACEMENT_MAIN: CleEmplacement` (vaut `'main'`)
  - `type RangeeAffichee = { cle: CleRangee; titre: string; defilants: EmplacementAffiche[]; epingles: EmplacementAffiche[] }`
  - `repartirEnRangees(plateau: Plateau): RangeeAffichee[]` (toujours les deux rangées, même vides)
  - `unitesDe(emplacements: EmplacementAffiche[]): UniteAffichee[]`
  - `mainDe(plateau: Plateau): UniteAffichee[]`

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/rangees.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { EMPLACEMENT_MAIN, RANGEES, mainDe, repartirEnRangees, unitesDe } from './rangees'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'

function unite(id: string): UniteAffichee {
  return { cle: `u${id}`, carte: { id, name: `Carte ${id}`, kind: 'ally', imageUrl: '' }, attachees: [] }
}

function emplacement(cle: CleEmplacement, unites: UniteAffichee[] = []): EmplacementAffiche {
  return { cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }
}

function plateau(emplacements: EmplacementAffiche[]): Plateau {
  return {
    emplacements,
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

describe('RANGEES', () => {
  it('range les 12 emplacements sans oubli ni doublon, main comprise', () => {
    const toutes: CleEmplacement[] = [
      'piles-rencontre', 'rencontre', 'complot-principal', 'complots-secondaires',
      'terrain-combat', 'terrain-soutien', 'deck-special', 'piles-joueur',
      'nemesis', 'annexes', 'reserve', 'main',
    ]
    const rangees = RANGEES.flatMap((rangee) => [...rangee.defilants, ...rangee.epingles])
    expect([...rangees, EMPLACEMENT_MAIN].sort()).toEqual([...toutes].sort())
  })

  it('lit la rangee ennemie du mechant vers le terrain, piles de rencontre epinglees', () => {
    const ennemie = RANGEES.find((rangee) => rangee.cle === 'ennemie')
    expect(ennemie?.defilants).toEqual(['rencontre', 'complot-principal', 'complots-secondaires', 'terrain-combat'])
    expect(ennemie?.epingles).toEqual(['piles-rencontre'])
  })

  // Demande de l'utilisateur (7/8/2026), toujours valable : la Reserve de Brawn
  // vit avec le heros, a cote du deck special, jamais avec la main.
  it('range la Reserve et le deck special avec le heros', () => {
    const heros = RANGEES.find((rangee) => rangee.cle === 'heros')
    expect(heros?.defilants).toEqual(['terrain-soutien', 'deck-special', 'reserve', 'nemesis'])
    expect(heros?.epingles).toEqual(['piles-joueur', 'annexes'])
  })
})

describe('repartirEnRangees', () => {
  it('rend TOUJOURS les deux rangees, meme sans aucun emplacement', () => {
    const rangees = repartirEnRangees(plateau([]))
    expect(rangees.map((rangee) => rangee.cle)).toEqual(['ennemie', 'heros'])
    expect(rangees[0].defilants).toEqual([])
    expect(rangees[0].epingles).toEqual([])
  })

  it('range chaque emplacement present dans sa rangee, defilant ou epingle', () => {
    const rangees = repartirEnRangees(
      plateau([emplacement('piles-joueur'), emplacement('rencontre'), emplacement('terrain-soutien')])
    )
    expect(rangees[0].defilants.map((e) => e.cle)).toEqual(['rencontre'])
    expect(rangees[1].defilants.map((e) => e.cle)).toEqual(['terrain-soutien'])
    expect(rangees[1].epingles.map((e) => e.cle)).toEqual(['piles-joueur'])
  })

  it('garde l\'ordre de lecture, pas celui du plateau', () => {
    const rangees = repartirEnRangees(
      plateau([emplacement('terrain-combat'), emplacement('complot-principal'), emplacement('rencontre')])
    )
    expect(rangees[0].defilants.map((e) => e.cle)).toEqual(['rencontre', 'complot-principal', 'terrain-combat'])
  })
})

describe('unitesDe et mainDe', () => {
  it('aplatit tous les groupes de tous les emplacements', () => {
    const a = emplacement('rencontre', [unite('1')])
    const b: EmplacementAffiche = { cle: 'terrain-combat', titre: 'x', groupes: [[unite('2')], [unite('3')]], nombreSurLaLigne: 2 }
    expect(unitesDe([a, b]).map((u) => u.carte.id)).toEqual(['1', '2', '3'])
  })

  it('mainDe rend les cartes de la main, ou rien si elle est absente', () => {
    expect(mainDe(plateau([]))).toEqual([])
    const main = mainDe(plateau([emplacement('main', [unite('7')])]))
    expect(main.map((u) => u.carte.id)).toEqual(['7'])
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npx vitest run src/board/mobile/rangees.test.ts
```

Attendu : échec, `Failed to resolve import "./rangees"`.

- [ ] **Step 3 : Écrire `rangees.ts`**

```ts
// Les 12 emplacements de zones.ts, ranges en DEUX rangees de cartes.
//
// C'est une TABLE, pas une logique. Ajouter un emplacement dans zones.ts, c'est
// ajouter une entree ici : le test verifie qu'aucun ne reste orphelin.
//
// Chaque rangee a deux parties : les emplacements qui DEFILENT (les cartes
// posees, de gauche a droite dans l'ordre de lecture) et ceux qui sont
// EPINGLES a droite (les piles : deck et defausse), hors du defilement. La
// main n'est pas une rangee : elle flotte en eventail au-dessus de la barre.
//
// Remplace bandes.ts (modele a medaillons), qui disparait au sous-projet 3.

import { t } from '../langue'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'

export type CleRangee = 'ennemie' | 'heros'

export const RANGEES: Array<{
  cle: CleRangee
  titre: () => string
  defilants: CleEmplacement[]
  epingles: CleEmplacement[]
}> = [
  {
    cle: 'ennemie',
    titre: () => t('Méchant'),
    defilants: ['rencontre', 'complot-principal', 'complots-secondaires', 'terrain-combat'],
    epingles: ['piles-rencontre'],
  },
  {
    cle: 'heros',
    titre: () => t('Ton héros'),
    // La Reserve (pack Brawn) suit le heros, a la meme place que le deck
    // special d'un Doctor Strange : c'est sa zone personnelle.
    defilants: ['terrain-soutien', 'deck-special', 'reserve', 'nemesis'],
    epingles: ['piles-joueur', 'annexes'],
  },
]

export const EMPLACEMENT_MAIN: CleEmplacement = 'main'

export type RangeeAffichee = {
  cle: CleRangee
  titre: string
  defilants: EmplacementAffiche[]
  epingles: EmplacementAffiche[]
}

/** Les deux rangees, TOUJOURS presentes : une rangee vide garde sa place. */
export function repartirEnRangees(plateau: Plateau): RangeeAffichee[] {
  const parCle = new Map<CleEmplacement, EmplacementAffiche>()
  for (const emplacement of plateau.emplacements) parCle.set(emplacement.cle, emplacement)
  const presents = (cles: CleEmplacement[]) =>
    cles
      .map((cle) => parCle.get(cle))
      .filter((emplacement): emplacement is EmplacementAffiche => emplacement !== undefined)

  return RANGEES.map((rangee) => ({
    cle: rangee.cle,
    titre: rangee.titre(),
    defilants: presents(rangee.defilants),
    epingles: presents(rangee.epingles),
  }))
}

/** Toutes les unites de ces emplacements, tous groupes confondus, dans l'ordre. */
export function unitesDe(emplacements: EmplacementAffiche[]): UniteAffichee[] {
  return emplacements.flatMap((emplacement) => emplacement.groupes.flat())
}

export function mainDe(plateau: Plateau): UniteAffichee[] {
  const main = plateau.emplacements.find((emplacement) => emplacement.cle === EMPLACEMENT_MAIN)
  return main ? unitesDe([main]) : []
}
```

- [ ] **Step 4 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/rangees.test.ts
```

Attendu : 8 tests verts.

- [ ] **Step 5 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/rangees.ts ui-app/src/board/mobile/rangees.test.ts
git commit -m "feat(plateau-mobile): les 12 emplacements ranges en deux rangees de cartes

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 3 : taille-carte.ts, la largeur d'une carte depuis la hauteur de l'écran

**Files:**
- Create: `ui-app/src/board/mobile/taille-carte.ts`
- Test: `ui-app/src/board/mobile/taille-carte.test.ts`

**Interfaces:**
- Produces: `HAUTEUR_BARRE = 48`, `HAUTEUR_MAIN_VISIBLE = 90`, `HAUTEUR_ETIQUETTE = 14`, `LARGEUR_MIN = 84`, `LARGEUR_MAX = 150`, `RATIO_CARTE = 63 / 88`, `HAUTEUR_FIXE = 166`, `hauteurRangee(hauteurFenetre: number): number`, `largeurCarte(hauteurFenetre: number): number`. Le CSS de la tâche 11 reproduit la même formule avec `100dvh`.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/taille-carte.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { HAUTEUR_FIXE, LARGEUR_MAX, LARGEUR_MIN, hauteurRangee, largeurCarte } from './taille-carte'

describe('taille-carte', () => {
  it('reserve 166 px aux bandes fixes : barre 48, main 90, deux etiquettes de 14', () => {
    expect(HAUTEUR_FIXE).toBe(48 + 90 + 2 * 14)
  })

  it('partage le reste en deux rangees egales', () => {
    expect(hauteurRangee(480)).toBe(157)
  })

  // S24 Ultra en paysage, plein ecran : la carte fait environ 112 px.
  it('donne environ 112 px en plein ecran (480 px de haut)', () => {
    expect(Math.round(largeurCarte(480))).toBe(112)
  })

  // Le meme, avec la barre du navigateur : environ 95 px.
  it('donne environ 95 px avec la barre du navigateur (430 px de haut)', () => {
    expect(Math.round(largeurCarte(430))).toBe(94)
  })

  it('ne descend jamais sous le plancher de 84 px', () => {
    expect(largeurCarte(300)).toBe(LARGEUR_MIN)
    expect(largeurCarte(0)).toBe(LARGEUR_MIN)
  })

  it('ne depasse jamais 150 px, la largeur du plateau PC (tablette)', () => {
    expect(largeurCarte(820)).toBe(LARGEUR_MAX)
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/taille-carte.test.ts
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `taille-carte.ts`**

```ts
// La largeur d'une carte posee, deduite de la hauteur de l'ecran.
//
// En paysage, la hauteur est la ressource rare : deux rangees de cartes, la
// main en eventail et la barre du bas doivent tenir dans 480 px (430 avec la
// barre du navigateur). La largeur de carte est donc une consequence, jamais
// une constante : celle qui remplit une rangee, entre un plancher de
// lisibilite et le plafond du plateau PC.
//
// paysage.css reproduit EXACTEMENT cette formule avec 100dvh. Cette version
// existe pour etre testee, et pour que les deux ne divergent pas sans qu'un
// test le dise.

/** La barre du bas (outils, ou demande du moteur). */
export const HAUTEUR_BARRE = 48
/** Ce que la main en eventail laisse voir au repos. */
export const HAUTEUR_MAIN_VISIBLE = 90
/** L'etiquette d'une rangee (« MECHANT », « TON HEROS »). */
export const HAUTEUR_ETIQUETTE = 14
export const HAUTEUR_FIXE = HAUTEUR_BARRE + HAUTEUR_MAIN_VISIBLE + 2 * HAUTEUR_ETIQUETTE

/** En dessous, le nom et les bulles de stats ne se lisent plus. */
export const LARGEUR_MIN = 84
/** La largeur d'une carte du plateau PC (board.css:893) : inutile d'aller au-dela. */
export const LARGEUR_MAX = 150
/** Largeur sur hauteur d'une carte a jouer. */
export const RATIO_CARTE = 63 / 88

export function hauteurRangee(hauteurFenetre: number): number {
  return (hauteurFenetre - HAUTEUR_FIXE) / 2
}

export function largeurCarte(hauteurFenetre: number): number {
  const ideale = hauteurRangee(hauteurFenetre) * RATIO_CARTE
  return Math.min(LARGEUR_MAX, Math.max(LARGEUR_MIN, ideale))
}
```

- [ ] **Step 4 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/taille-carte.test.ts
```

Attendu : 6 tests verts.

- [ ] **Step 5 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/taille-carte.ts ui-app/src/board/mobile/taille-carte.test.ts
git commit -m "feat(plateau-mobile): la largeur d'une carte se deduit de la hauteur de l'ecran

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 4 : etats.ts, la table des états sortie du médaillon

**Files:**
- Create: `ui-app/src/board/mobile/etats.ts`
- Test: `ui-app/src/board/mobile/etats.test.ts`
- Modify: `ui-app/src/board/mobile/Medaillon.tsx:27-38` (la table `ETATS` et `etatDe` y sont remplacées par un import)

**Interfaces:**
- Consumes: `ScanCardProps` de `../../components/ScanCard`.
- Produces: `type Etat = { lettre: string; classe: string; nom: string }`, `ETATS: Record<string, Etat>`, `etatDe(carte: ScanCardProps): Etat | undefined`, `separerAttachees(attachees: ScanCardProps[]): { etats: Etat[]; ameliorations: ScanCardProps[] }`.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/etats.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { etatDe, separerAttachees } from './etats'
import type { ScanCardProps } from '../../components/ScanCard'

const carte = (name: string, kind: ScanCardProps['kind'] = 'status'): ScanCardProps => ({
  id: name, name, kind, imageUrl: '',
})

describe('etatDe', () => {
  it('reconnait les trois etats par leur nom, sans tenir compte de la casse', () => {
    expect(etatDe(carte('Tough'))?.lettre).toBe('T')
    expect(etatDe(carte('STUNNED'))?.classe).toBe('est-sonne')
    expect(etatDe(carte(' confused '))?.nom).toBe('Désorienté')
  })

  // Le moteur pose les statuts avec kind 'status' (Board.tsx:174). Un statut
  // dont le nom serait traduit ou inconnu reste un etat, avec son initiale.
  it('traite toute carte de kind status comme un etat, meme au nom inconnu', () => {
    expect(etatDe(carte('Coriace', 'status'))).toEqual({ lettre: 'C', classe: 'est-autre', nom: 'Coriace' })
  })

  it('ne prend pas une amelioration pour un etat', () => {
    expect(etatDe(carte('Web-Shooter', 'upgrade'))).toBeUndefined()
  })
})

describe('separerAttachees', () => {
  it('separe les etats des ameliorations en gardant leur ordre', () => {
    const { etats, ameliorations } = separerAttachees([
      carte('Web-Shooter', 'upgrade'), carte('Stunned'), carte('Tough'), carte('Armor', 'upgrade'),
    ])
    expect(etats.map((etat) => etat.lettre)).toEqual(['S', 'T'])
    expect(ameliorations.map((a) => a.name)).toEqual(['Web-Shooter', 'Armor'])
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/etats.test.ts
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `etats.ts`**

```ts
// Les etats poses sur un personnage : coriace, sonne, desoriente.
//
// Le moteur les attache comme des CARTES (kind 'status'). Sur une carte de
// 100 px, une carte glissee derriere ne se lit pas : ces etats deviennent des
// pastilles lettrees au coin de la carte. Cette table dit la lettre, la classe
// CSS et le libelle de chacun. Partagee par CartePosee (paysage) et par le
// medaillon tant qu'il existe.

import type { ScanCardProps } from '../../components/ScanCard'

export type Etat = { lettre: string; classe: string; nom: string }

export const ETATS: Record<string, Etat> = {
  tough: { lettre: 'T', classe: 'est-coriace', nom: 'Coriace' },
  stunned: { lettre: 'S', classe: 'est-sonne', nom: 'Sonné' },
  confused: { lettre: 'C', classe: 'est-desoriente', nom: 'Désorienté' },
}

export function etatDe(carte: ScanCardProps): Etat | undefined {
  const connu = ETATS[carte.name.trim().toLowerCase()]
  if (connu) return connu
  if (carte.kind !== 'status') return undefined
  // Un statut au nom inconnu (traduit, ou maison) reste un etat : on garde son
  // initiale plutot que de le perdre en silence.
  const nom = carte.name.trim()
  return { lettre: (nom[0] ?? '?').toUpperCase(), classe: 'est-autre', nom }
}

export function separerAttachees(attachees: ScanCardProps[]): {
  etats: Etat[]
  ameliorations: ScanCardProps[]
} {
  const etats: Etat[] = []
  const ameliorations: ScanCardProps[] = []
  for (const attachee of attachees) {
    const etat = etatDe(attachee)
    if (etat) etats.push(etat)
    else ameliorations.push(attachee)
  }
  return { etats, ameliorations }
}
```

- [ ] **Step 4 : Faire consommer la table par le médaillon**

Dans `Medaillon.tsx`, supprimer les lignes 27 à 38 (le bloc `const ETATS ... ` et la fonction `etatDe`) et les remplacer par :

```ts
import { etatDe } from './etats'
```

placé avec les autres imports. Le reste du fichier appelle déjà `etatDe(attachee)` : rien d'autre ne change.

- [ ] **Step 5 : Lancer les tests, ils doivent passer**

```bash
npx vitest run src/board/mobile/etats.test.ts src/board/mobile/PlateauMedaillons.test.tsx && npx tsc --noEmit
```

Attendu : tout vert, `tsc` silencieux.

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/etats.ts ui-app/src/board/mobile/etats.test.ts ui-app/src/board/mobile/Medaillon.tsx
git commit -m "refactor(plateau-mobile): la table des etats sort du medaillon pour etre partagee

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 5 : hors-champ.ts, compter les cartes hors du champ visible

**Files:**
- Create: `ui-app/src/board/mobile/hors-champ.ts`
- Test: `ui-app/src/board/mobile/hors-champ.test.ts`

**Interfaces:**
- Produces: `type Boite1D = { gauche: number; largeur: number }`, `nombreHorsChamp(boites: Boite1D[], defilement: number, largeurVisible: number): number`, `mesurerHorsChamp(conteneur: HTMLElement, selecteur?: string): number` (lit `offsetLeft` / `offsetWidth` des enfants, sélecteur par défaut `.carte-posee`).

Règle : une carte est hors champ quand plus de la moitié de sa largeur dépasse le bord droit visible, ou quand plus de la moitié est cachée à gauche par le défilement.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/hors-champ.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { mesurerHorsChamp, nombreHorsChamp } from './hors-champ'

const cartes = (n: number, largeur = 100, ecart = 8) =>
  Array.from({ length: n }, (_, i) => ({ gauche: i * (largeur + ecart), largeur }))

describe('nombreHorsChamp', () => {
  it('vaut 0 quand tout tient', () => {
    expect(nombreHorsChamp(cartes(3), 0, 400)).toBe(0)
  })

  it('compte les cartes dont plus de la moitie depasse a droite', () => {
    // 5 cartes de 100 px, ecart 8 : bords droits a 100, 208, 316, 424, 532.
    // Fenetre de 370 px : la 4e depasse de 54 px (plus de la moitie), la 5e entierement.
    expect(nombreHorsChamp(cartes(5), 0, 370)).toBe(2)
  })

  it('ne compte pas une carte qui ne depasse que d\'un peu', () => {
    // La 4e carte (316 a 416) depasse de 16 px sur 100 : elle se lit encore.
    expect(nombreHorsChamp(cartes(4), 0, 400)).toBe(0)
  })

  it('compte aussi ce qui est cache a gauche par le defilement', () => {
    // Defilement de 60 px : la 1re carte (0 a 100) a 60 px caches, plus de la moitie.
    expect(nombreHorsChamp(cartes(3), 60, 1000)).toBe(1)
  })

  it('vaut 0 sans carte', () => {
    expect(nombreHorsChamp([], 0, 400)).toBe(0)
  })
})

describe('mesurerHorsChamp', () => {
  it('lit les positions des enfants dans le DOM', () => {
    const conteneur = document.createElement('div')
    for (const boite of cartes(5)) {
      const enfant = document.createElement('div')
      enfant.className = 'carte-posee'
      Object.defineProperty(enfant, 'offsetLeft', { value: boite.gauche })
      Object.defineProperty(enfant, 'offsetWidth', { value: boite.largeur })
      conteneur.append(enfant)
    }
    Object.defineProperty(conteneur, 'clientWidth', { value: 370 })
    conteneur.scrollLeft = 0
    expect(mesurerHorsChamp(conteneur)).toBe(2)
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/hors-champ.test.ts
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `hors-champ.ts`**

```ts
// Combien de cartes d'une rangee sont hors du champ visible ?
//
// Une rangee qui deborde defile, et un voile au bord droit porte ce compte :
// c'est le seul signal qui dit qu'il y a une suite. Le calcul est ici, pur,
// pour etre teste ; la lecture du DOM est une enveloppe de trois lignes.
//
// Une carte compte comme hors champ quand PLUS DE LA MOITIE de sa largeur est
// cachee, a droite comme a gauche : une carte coupee d'un bord reste lisible
// et se voit, inutile de l'annoncer.

export type Boite1D = { gauche: number; largeur: number }

export function nombreHorsChamp(boites: Boite1D[], defilement: number, largeurVisible: number): number {
  const bordDroit = defilement + largeurVisible
  let compte = 0
  for (const { gauche, largeur } of boites) {
    const moitie = largeur / 2
    const cacheADroite = gauche + largeur - bordDroit
    const cacheAGauche = defilement - gauche
    if (cacheADroite > moitie || cacheAGauche > moitie) compte += 1
  }
  return compte
}

export function mesurerHorsChamp(conteneur: HTMLElement, selecteur = '.carte-posee'): number {
  const boites: Boite1D[] = []
  for (const enfant of conteneur.querySelectorAll<HTMLElement>(selecteur)) {
    boites.push({ gauche: enfant.offsetLeft, largeur: enfant.offsetWidth })
  }
  return nombreHorsChamp(boites, conteneur.scrollLeft, conteneur.clientWidth)
}
```

- [ ] **Step 4 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/hors-champ.test.ts
```

Attendu : 6 tests verts.

- [ ] **Step 5 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/hors-champ.ts ui-app/src/board/mobile/hors-champ.test.ts
git commit -m "feat(plateau-mobile): compter les cartes d'une rangee hors du champ visible

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 6 : plein-ecran.ts, le plein écran au premier geste et l'écran portrait

**Files:**
- Create: `ui-app/src/board/mobile/plein-ecran.ts`
- Test: `ui-app/src/board/mobile/plein-ecran.test.ts`

**Interfaces:**
- Produces:
  - `doitDemanderPleinEcran(dejaEnPleinEcran: boolean, supporte: boolean): boolean`
  - `doitMontrerEcranPortrait(orientation: 'portrait' | 'paysage'): boolean`
  - `demanderPleinEcranPaysage(doc?: Document): Promise<void>` (n'échoue jamais)
  - `usePleinEcranAuPremierGeste(actif: boolean): void` (hook : au premier `pointerdown` sur le document, appelle `demanderPleinEcranPaysage`, une seule fois par montage)

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/plein-ecran.test.ts` :

```ts
import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import {
  demanderPleinEcranPaysage,
  doitDemanderPleinEcran,
  doitMontrerEcranPortrait,
  usePleinEcranAuPremierGeste,
} from './plein-ecran'

describe('regles pures', () => {
  it('demande le plein ecran seulement si le navigateur le supporte et qu\'on n\'y est pas', () => {
    expect(doitDemanderPleinEcran(false, true)).toBe(true)
    expect(doitDemanderPleinEcran(true, true)).toBe(false)
    expect(doitDemanderPleinEcran(false, false)).toBe(false)
  })

  it('montre l\'ecran portrait en portrait, et seulement la', () => {
    expect(doitMontrerEcranPortrait('portrait')).toBe(true)
    expect(doitMontrerEcranPortrait('paysage')).toBe(false)
  })
})

describe('demanderPleinEcranPaysage', () => {
  it('demande le plein ecran PUIS verrouille le paysage', async () => {
    const lock = vi.fn().mockResolvedValue(undefined)
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    const doc = {
      fullscreenElement: null,
      documentElement: { requestFullscreen },
      defaultView: { screen: { orientation: { lock } } },
    } as unknown as Document
    await demanderPleinEcranPaysage(doc)
    expect(requestFullscreen).toHaveBeenCalledOnce()
    expect(lock).toHaveBeenCalledWith('landscape')
  })

  it('ne leve rien quand le plein ecran est refuse (le filet est l\'ecran portrait)', async () => {
    const doc = {
      fullscreenElement: null,
      documentElement: { requestFullscreen: vi.fn().mockRejectedValue(new Error('refus')) },
      defaultView: { screen: { orientation: { lock: vi.fn() } } },
    } as unknown as Document
    await expect(demanderPleinEcranPaysage(doc)).resolves.toBeUndefined()
  })

  it('ne leve rien sans API de plein ecran (iOS Safari)', async () => {
    const doc = { fullscreenElement: null, documentElement: {}, defaultView: { screen: {} } } as unknown as Document
    await expect(demanderPleinEcranPaysage(doc)).resolves.toBeUndefined()
  })
})

describe('usePleinEcranAuPremierGeste', () => {
  afterEach(() => vi.restoreAllMocks())

  it('demande le plein ecran au PREMIER pointerdown, et une seule fois', () => {
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    document.documentElement.requestFullscreen = requestFullscreen
    renderHook(() => usePleinEcranAuPremierGeste(true))
    document.dispatchEvent(new Event('pointerdown'))
    document.dispatchEvent(new Event('pointerdown'))
    expect(requestFullscreen).toHaveBeenCalledOnce()
  })

  it('ne fait rien quand il est inactif', () => {
    const requestFullscreen = vi.fn().mockResolvedValue(undefined)
    document.documentElement.requestFullscreen = requestFullscreen
    renderHook(() => usePleinEcranAuPremierGeste(false))
    document.dispatchEvent(new Event('pointerdown'))
    expect(requestFullscreen).not.toHaveBeenCalled()
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/plein-ecran.test.ts
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `plein-ecran.ts`**

```ts
// Le plein ecran et le verrouillage en paysage, au premier geste.
//
// Le plateau se joue en paysage (spec du 07/09/2026, §4.8). Un navigateur
// mobile ne donne le plein ecran et le verrouillage d'orientation qu'en
// reponse a un geste de l'utilisateur : on s'accroche donc au PREMIER
// pointerdown, une seule fois. Tout refus est avale : le filet, c'est
// EcranPortrait, qui couvre le plateau tant que l'appareil est en portrait.

import { useEffect } from 'react'

export function doitDemanderPleinEcran(dejaEnPleinEcran: boolean, supporte: boolean): boolean {
  return supporte && !dejaEnPleinEcran
}

export function doitMontrerEcranPortrait(orientation: 'portrait' | 'paysage'): boolean {
  return orientation === 'portrait'
}

type Verrou = { lock?: (orientation: 'landscape') => Promise<void> }

export async function demanderPleinEcranPaysage(doc: Document = document): Promise<void> {
  const racine = doc.documentElement as HTMLElement & { requestFullscreen?: () => Promise<void> }
  const supporte = typeof racine.requestFullscreen === 'function'
  if (!doitDemanderPleinEcran(doc.fullscreenElement !== null, supporte)) return
  try {
    await racine.requestFullscreen!()
    // Le verrouillage n'est accepte QU'EN plein ecran : d'ou l'ordre.
    const verrou = (doc.defaultView?.screen as { orientation?: Verrou } | undefined)?.orientation
    if (verrou && typeof verrou.lock === 'function') await verrou.lock('landscape')
  } catch {
    // Refus (iOS Safari, navigateur de bureau, permission) : l'ecran portrait
    // fait le travail. Rien a signaler au joueur.
  }
}

export function usePleinEcranAuPremierGeste(actif: boolean): void {
  useEffect(() => {
    if (!actif) return
    const surGeste = () => {
      void demanderPleinEcranPaysage()
    }
    document.addEventListener('pointerdown', surGeste, { once: true })
    return () => document.removeEventListener('pointerdown', surGeste)
  }, [actif])
}
```

- [ ] **Step 4 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/plein-ecran.test.ts && npx tsc --noEmit
```

Attendu : 7 tests verts, `tsc` silencieux.

- [ ] **Step 5 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/plein-ecran.ts ui-app/src/board/mobile/plein-ecran.test.ts
git commit -m "feat(plateau-mobile): plein ecran et verrouillage paysage au premier geste

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 7 : CartePosee.tsx, une vraie carte sur la table

**Files:**
- Create: `ui-app/src/board/mobile/CartePosee.tsx`
- Test: `ui-app/src/board/mobile/CartePosee.test.tsx`

**Interfaces:**
- Consumes: `ScanCard`, `ScanCardProps`, `CardEffectDelta` de `../../components/ScanCard` ; `UniteAffichee` de `../zones` ; `separerAttachees` de `./etats` ; `t` de `../langue`.
- Produces: `export type CartePoseeProps = { unite: UniteAffichee; effet?: CardEffectDelta; onOuvrir: (carte: ScanCardProps) => void }` et `export function CartePosee(props)`.

Comportement : la carte est rendue par `ScanCard` SANS `onSelect` (le tap ouvre d'abord, l'action se déclenche depuis `CarteOuverte`, comme le médaillon), mais avec son `state`, ses stats et son `effectDelta`. Les améliorations sont glissées derrière, décalées de 14 px vers la DROITE chacune (la hauteur d'une rangée est fixe, on ne déborde pas vers le bas), tap possible sur la bande visible. Les états deviennent des pastilles au coin supérieur droit. Le conteneur porte `data-tactile="carte"` et un rôle de bouton.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/CartePosee.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CartePosee } from './CartePosee'
import type { UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const carte = (id: string, name: string, kind: ScanCardProps['kind'] = 'ally'): ScanCardProps => ({
  id, name, kind, imageUrl: '',
})

function unite(attachees: ScanCardProps[] = []): UniteAffichee {
  return { cle: 'u1', carte: { ...carte('1', 'Rhino', 'villain'), allyHp: '12/22', state: 'targetable', onSelect: () => {} }, attachees }
}

describe('CartePosee', () => {
  it('rend une VRAIE carte, avec son nom et ses PV, et se tape comme un bouton', () => {
    const ouvrir = vi.fn()
    render(<CartePosee unite={unite()} onOuvrir={ouvrir} />)
    const cible = screen.getByRole('button', { name: /Rhino/ })
    expect(cible).toHaveAttribute('data-tactile', 'carte')
    expect(cible.querySelector('.scan-card[data-card-id="1"]')).toBeInTheDocument()
    expect(screen.getByText('12/22')).toBeInTheDocument()
  })

  it('garde l\'etat d\'interaction sur la carte, mais le tap OUVRE au lieu d\'agir', () => {
    const agir = vi.fn()
    const ouvrir = vi.fn()
    const u = unite()
    u.carte.onSelect = agir
    render(<CartePosee unite={u} onOuvrir={ouvrir} />)
    expect(document.querySelector('.scan-card')).toHaveClass('state-targetable')
    fireEvent.click(screen.getByRole('button', { name: /Rhino/ }))
    expect(agir).not.toHaveBeenCalled()
    expect(ouvrir).toHaveBeenCalledWith(expect.objectContaining({ id: '1', onSelect: agir }))
  })

  it('pose les etats en pastilles lettrees, pas en cartes', () => {
    render(<CartePosee unite={unite([carte('s1', 'Stunned', 'status'), carte('s2', 'Tough', 'status')])} onOuvrir={() => {}} />)
    const pastilles = document.querySelectorAll('.carte-posee-etat')
    expect([...pastilles].map((p) => p.textContent)).toEqual(['S', 'T'])
    expect(pastilles[0]).toHaveClass('est-sonne')
    expect(pastilles[0]).toHaveAttribute('title', 'Sonné')
    // Aucune carte de statut n'est dessinee en carte.
    expect(document.querySelectorAll('.scan-card')).toHaveLength(1)
  })

  it('glisse les ameliorations derriere, tap possible sur chacune', () => {
    const ouvrir = vi.fn()
    render(
      <CartePosee
        unite={unite([carte('a1', 'Web-Shooter', 'upgrade'), carte('a2', 'Armor', 'upgrade')])}
        onOuvrir={ouvrir}
      />
    )
    const conteneur = document.querySelector<HTMLElement>('.carte-posee')
    expect(conteneur?.style.getPropertyValue('--nb')).toBe('2')
    const attachees = document.querySelectorAll<HTMLElement>('.carte-posee-attachee')
    expect(attachees).toHaveLength(2)
    expect(attachees[1].style.getPropertyValue('--i')).toBe('2')
    fireEvent.click(attachees[1])
    expect(ouvrir).toHaveBeenCalledWith(expect.objectContaining({ id: 'a2' }))
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })

  it('s\'ouvre aussi au clavier, Entree ou Espace', () => {
    const ouvrir = vi.fn()
    render(<CartePosee unite={unite()} onOuvrir={ouvrir} />)
    fireEvent.keyDown(screen.getByRole('button', { name: /Rhino/ }), { key: 'Enter' })
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/CartePosee.test.tsx
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `CartePosee.tsx`**

```tsx
// Une carte POSEE sur la table, vue de telephone en paysage.
//
// C'est une vraie carte (ScanCard), pas un medaillon : a 95 px et plus, le nom,
// le cout et les bulles de stats se lisent. Le texte de regles, lui, ne se lit
// pas a cette taille : le tap ouvre la carte en grand (CarteOuverte), et c'est
// de la qu'on agit. La carte ne recoit donc PAS son onSelect ici, mais garde
// son etat (cible, jouable, choisie) pour que le CSS l'allume ou l'eteigne.
//
// Ce qui s'attache a la carte :
//   - les ETATS (coriace, sonne, desoriente) en pastilles lettrees au coin :
//     une carte glissee derriere ne se lirait pas a cette taille ;
//   - les AMELIORATIONS glissees derriere le porteur, decalees vers la DROITE
//     de 14 px chacune. Vers le bas, elles sortiraient d'une rangee dont la
//     hauteur est fixe. La bande visible de chacune repond au tap.

import type { CSSProperties, KeyboardEvent } from 'react'
import { ScanCard, type CardEffectDelta, type ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import { separerAttachees } from './etats'
import './paysage.css'

export type CartePoseeProps = {
  unite: UniteAffichee
  /** Variation de compteur en cours : le nombre qui s'envole, rendu par ScanCard. */
  effet?: CardEffectDelta
  onOuvrir: (carte: ScanCardProps) => void
}

/** La carte telle qu'on la DESSINE : sans action directe, le tap ouvre d'abord. */
function sansAction(carte: ScanCardProps, effet?: CardEffectDelta): ScanCardProps {
  const { onSelect: _onSelect, ...reste } = carte
  return effet ? { ...reste, effectDelta: effet } : reste
}

export function CartePosee({ unite, effet, onOuvrir }: CartePoseeProps) {
  const { etats, ameliorations } = separerAttachees(unite.attachees)
  const carte = unite.carte
  const pastille = carte.allyHp ?? carte.schemeThreat

  const auClavier = (evenement: KeyboardEvent<HTMLDivElement>) => {
    if (evenement.key === 'Enter' || evenement.key === ' ') {
      evenement.preventDefault()
      onOuvrir(carte)
    }
  }

  return (
    <div
      className="carte-posee"
      role="button"
      tabIndex={0}
      data-tactile="carte"
      aria-label={`${carte.name}${pastille ? `, ${pastille}` : ''}`}
      style={{ '--nb': ameliorations.length } as CSSProperties}
      onClick={() => onOuvrir(carte)}
      onKeyDown={auClavier}
    >
      {ameliorations.map((amelioration, index) => (
        <span
          className="carte-posee-attachee"
          key={amelioration.id}
          style={{ '--i': index + 1 } as CSSProperties}
          onClick={(evenement) => {
            evenement.stopPropagation()
            onOuvrir(amelioration)
          }}
        >
          <ScanCard {...sansAction(amelioration)} />
        </span>
      ))}

      <ScanCard {...sansAction(carte, effet)} />

      {etats.length > 0 ? (
        <span className="carte-posee-etats">
          {etats.map((etat) => (
            <span className={`carte-posee-etat ${etat.classe}`} key={etat.lettre} title={t(etat.nom)}>
              {etat.lettre}
            </span>
          ))}
        </span>
      ) : null}
    </div>
  )
}
```

- [ ] **Step 4 : Créer `paysage.css` avec les règles de la carte posée**

`ui-app/src/board/mobile/paysage.css` (la tâche 11 complète ce fichier ; ne pas y mettre autre chose pour l'instant) :

```css
/* Le plateau en PAYSAGE : deux rangees de vraies cartes.
   Spec : docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md §4.

   Les tailles ici sont des pixels CSS reels, pas des pixels de scene : ce rendu
   n'est PAS mis a l'echelle, contrairement a board.css. La main, la barre du bas
   et la carte ouverte gardent leurs regles dans medaillon.css jusqu'au
   sous-projet 3. */

@layer composants {
  /* --- Une carte posee ------------------------------------------------------ */

  .carte-posee {
    position: relative;
    flex: none;
    scroll-snap-align: start;
    /* Les ameliorations glissees derriere depassent a DROITE de 14 px chacune :
       la carte reserve cette place pour ne pas les poser sur sa voisine. */
    padding-right: calc(var(--nb, 0) * 14px);
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }

  .carte-posee > .scan-card {
    position: relative;
    z-index: 1;
  }

  .carte-posee-attachee {
    position: absolute;
    top: 0;
    left: calc(var(--i, 1) * 14px);
    z-index: 0;
    filter: brightness(0.75);
  }

  /* Pastilles d'etat, au coin superieur droit du PORTEUR (pas du dernier
     jeton glisse derriere). */
  .carte-posee-etats {
    position: absolute;
    top: -6px;
    right: calc(var(--nb, 0) * 14px - 6px);
    z-index: 2;
    display: flex;
    gap: 2px;
  }

  .carte-posee-etat {
    display: grid;
    place-items: center;
    width: 20px;
    height: 20px;
    border: 2px solid #0b0b0b;
    border-radius: 50%;
    font-size: 0.7rem;
    font-weight: 900;
    color: #111;
    background: #e5e7eb;
  }

  .carte-posee-etat.est-coriace { background: #9ca3af; }
  .carte-posee-etat.est-sonne { background: #f59e0b; }
  .carte-posee-etat.est-desoriente { background: #a78bfa; }
}
```

- [ ] **Step 5 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/CartePosee.test.tsx && npx tsc --noEmit
```

Attendu : 5 tests verts, `tsc` silencieux. Si `tsc` se plaint de `_onSelect` inutilisé, remplacer la destructuration par `const reste = { ...carte }; delete reste.onSelect`.

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/CartePosee.tsx ui-app/src/board/mobile/CartePosee.test.tsx ui-app/src/board/mobile/paysage.css
git commit -m "feat(plateau-mobile): une carte posee est une vraie carte, etats en pastilles

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 8 : PilesEpinglees.tsx, deck et défausse au bout de la rangée

**Files:**
- Create: `ui-app/src/board/mobile/PilesEpinglees.tsx`
- Test: `ui-app/src/board/mobile/PilesEpinglees.test.tsx`
- Modify: `ui-app/src/board/mobile/paysage.css` (ajout des règles des piles)

**Interfaces:**
- Consumes: `ScanCard`, `ScanCardProps` ; `UniteAffichee` ; `t`.
- Produces: `export type PilesEpingleesProps = { piles: UniteAffichee[]; onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void }`, `export function PilesEpinglees(props)`.

Comportement : chaque pile est un `ScanCard` réduit (56 px, règle CSS) portant son compte (`carte.pileCount`, sinon la longueur de `pileContenu`, sinon 0) et son nom court (`unite.pileTitre ?? carte.name`). Une pile consultable (`pileContenu` non vide) s'ouvre au tap ; une pile secrète (deck) ne réagit pas et est marquée `aria-disabled`. `data-tactile="pile"`.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/PilesEpinglees.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PilesEpinglees } from './PilesEpinglees'
import type { UniteAffichee } from '../zones'

const deck: UniteAffichee = {
  cle: 'deck',
  carte: { id: '10', name: 'Encounter deck', kind: 'villain', imageUrl: '', facedown: true, pileCount: 23 },
  attachees: [],
  pileTitre: 'Deck de rencontre',
}

const defausse: UniteAffichee = {
  cle: 'defausse',
  carte: { id: '11', name: 'Advance', kind: 'treachery', imageUrl: '', discard: true },
  attachees: [],
  pileTitre: 'Défausse',
  pileContenu: [
    { id: '11', name: 'Advance', kind: 'treachery', imageUrl: '' },
    { id: '12', name: 'Assault', kind: 'treachery', imageUrl: '' },
  ],
}

describe('PilesEpinglees', () => {
  it('montre chaque pile avec son compte et son nom', () => {
    render(<PilesEpinglees piles={[deck, defausse]} onOuvrirPile={() => {}} />)
    expect(screen.getByText('23')).toBeInTheDocument()
    expect(screen.getByText('Deck de rencontre')).toBeInTheDocument()
    // Sans pileCount, le compte est la taille du contenu.
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(document.querySelectorAll('[data-tactile="pile"]')).toHaveLength(2)
  })

  it('etale une pile consultable au tap, avec son titre', () => {
    const ouvrir = vi.fn()
    render(<PilesEpinglees piles={[deck, defausse]} onOuvrirPile={ouvrir} />)
    fireEvent.click(screen.getByRole('button', { name: /Défausse/ }))
    expect(ouvrir).toHaveBeenCalledWith('Défausse', defausse.pileContenu)
  })

  it('ne fait rien sur une pile secrete, et le dit', () => {
    const ouvrir = vi.fn()
    render(<PilesEpinglees piles={[deck]} onOuvrirPile={ouvrir} />)
    const pile = screen.getByRole('button', { name: /Deck de rencontre/ })
    expect(pile).toHaveAttribute('aria-disabled', 'true')
    fireEvent.click(pile)
    expect(ouvrir).not.toHaveBeenCalled()
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/PilesEpinglees.test.tsx
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `PilesEpinglees.tsx`**

```tsx
// Les piles au bout d'une rangee : deck et defausse, en dos de carte reduit.
//
// Elles sont EPINGLEES a droite, hors du defilement de la rangee : on sait
// toujours ou elles sont, et ce qu'il reste dedans. Une pile consultable (la
// defausse, la victoire) s'etale au tap ; un deck reste secret et ne repond
// pas, sans pour autant disparaitre : son compte est une information de jeu.

import type { KeyboardEvent } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import './paysage.css'

export type PilesEpingleesProps = {
  piles: UniteAffichee[]
  onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void
}

function compteDe(unite: UniteAffichee): number {
  return unite.carte.pileCount ?? unite.pileContenu?.length ?? 0
}

export function PilesEpinglees({ piles, onOuvrirPile }: PilesEpingleesProps) {
  return (
    <div className="piles-epinglees">
      {piles.map((unite) => {
        const titre = unite.pileTitre ?? unite.carte.name
        const contenu = unite.pileContenu
        const consultable = contenu !== undefined && contenu.length > 0
        const ouvrir = () => {
          if (consultable) onOuvrirPile(titre, contenu)
        }
        const auClavier = (evenement: KeyboardEvent<HTMLDivElement>) => {
          if (evenement.key === 'Enter' || evenement.key === ' ') {
            evenement.preventDefault()
            ouvrir()
          }
        }
        const { onSelect: _onSelect, ...carte } = unite.carte
        return (
          <div
            className={`pile-epinglee${consultable ? '' : ' est-secrete'}`}
            role="button"
            tabIndex={0}
            aria-disabled={consultable ? undefined : true}
            aria-label={`${titre}, ${compteDe(unite)}`}
            data-tactile="pile"
            key={unite.cle}
            onClick={ouvrir}
            onKeyDown={auClavier}
          >
            <ScanCard {...carte} />
            <span className="pile-epinglee-compte">{compteDe(unite)}</span>
            <span className="pile-epinglee-nom">{titre}</span>
          </div>
        )
      })}
    </div>
  )
}
```

- [ ] **Step 4 : Ajouter les règles CSS des piles dans `paysage.css`**

À la fin du bloc `@layer composants { ... }` existant, avant l'accolade fermante :

```css
  /* --- Piles epinglees au bout d'une rangee --------------------------------- */

  .piles-epinglees {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    padding: 0 8px 0 6px;
    border-left: 1px solid rgba(255, 255, 255, 0.14);
  }

  .pile-epinglee {
    position: relative;
    display: grid;
    justify-items: center;
    gap: 2px;
    /* 56 px de carte, mais 44 px de cible au minimum dans les deux axes. */
    min-width: 44px;
    min-height: 44px;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }

  .pile-epinglee.est-secrete {
    cursor: default;
  }

  .pile-epinglee-compte {
    position: absolute;
    top: 4px;
    right: 4px;
    min-width: 22px;
    padding: 1px 5px;
    border: 2px solid #0b0b0b;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 900;
    text-align: center;
    color: #111;
    background: #f8fafc;
  }

  .pile-epinglee-nom {
    max-width: 64px;
    overflow: hidden;
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: rgba(255, 255, 255, 0.7);
  }
```

Et un nouveau bloc à la fin du fichier (les tailles de carte DOIVENT vivre dans `utilitaires`, voir la note en fin de `medaillon.css`) :

```css
/* --- Taille des cartes : DOIT etre dans `utilitaires` ---------------------
   ScanCard.css y impose ses propres --card-w selon la largeur d'ecran. Une
   couche posterieure l'emporte sur toute specificite. */
@layer utilitaires {
  .pile-epinglee .scan-card {
    --card-w: 56px;
    --inspect-scale: 1;
  }

  .pile-epinglee .scan-card .top-strip {
    display: none;
  }
}
```

- [ ] **Step 5 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/PilesEpinglees.test.tsx && npx tsc --noEmit
```

Attendu : 3 tests verts, `tsc` silencieux.

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/PilesEpinglees.tsx ui-app/src/board/mobile/PilesEpinglees.test.tsx ui-app/src/board/mobile/paysage.css
git commit -m "feat(plateau-mobile): deck et defausse epingles au bout de chaque rangee

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 9 : RangeeCartes.tsx, une rangée qui défile

**Files:**
- Create: `ui-app/src/board/mobile/RangeeCartes.tsx`
- Test: `ui-app/src/board/mobile/RangeeCartes.test.tsx`
- Modify: `ui-app/src/board/mobile/paysage.css` (règles de la rangée)

**Interfaces:**
- Consumes: `CartePosee` (tâche 7), `PilesEpinglees` (tâche 8), `mesurerHorsChamp` (tâche 5), `CleRangee` (tâche 2), `t`.
- Produces:
  - `export type GroupeRangee = { cle: string; unites: UniteAffichee[]; actif?: boolean }`
  - `export type RangeeCartesProps = { cle: CleRangee; titre: string; groupes: GroupeRangee[]; piles: UniteAffichee[]; cibles?: number; effets?: Map<number, CardEffectDelta>; onOuvrirCarte: (carte: ScanCardProps) => void; onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void }`
  - `export function RangeeCartes(props)`

Comportement : étiquette avec le compte de cibles ; zone défilante contenant les groupes séparés par un trait (`role="separator"`) ; `Vide` si aucun groupe n'a de carte ; voile « +N » cliquable qui fait avancer d'une largeur visible ; piles épinglées à droite ; quand `cibles` passe de 0 à plus, la première carte `.state-targetable` est ramenée dans le champ (`scrollIntoView`, gardé contre jsdom).

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/RangeeCartes.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { RangeeCartes, type GroupeRangee } from './RangeeCartes'
import type { UniteAffichee } from '../zones'

const unite = (id: string, name: string, state?: 'targetable' | 'disabled'): UniteAffichee => ({
  cle: `u${id}`,
  carte: { id, name, kind: 'ally', imageUrl: '', state },
  attachees: [],
})

function rendre(groupes: GroupeRangee[], extra: Partial<Parameters<typeof RangeeCartes>[0]> = {}) {
  return render(
    <RangeeCartes
      cle="heros"
      titre="Ton héros"
      groupes={groupes}
      piles={[]}
      onOuvrirCarte={() => {}}
      onOuvrirPile={() => {}}
      {...extra}
    />
  )
}

describe('RangeeCartes', () => {
  it('porte son etiquette et ses cartes dans l\'ordre', () => {
    rendre([{ cle: 'g', unites: [unite('1', 'Spider-Man'), unite('2', 'Black Cat')] }])
    expect(screen.getByRole('region', { name: 'Ton héros' })).toBeInTheDocument()
    const noms = [...document.querySelectorAll('.carte-posee')].map((c) => c.getAttribute('aria-label'))
    expect(noms).toEqual(['Spider-Man', 'Black Cat'])
  })

  it('dit « Vide » quand aucune carte, sans perdre son etiquette', () => {
    rendre([{ cle: 'g', unites: [] }])
    expect(screen.getByText('Vide')).toBeInTheDocument()
    expect(screen.getByText('Ton héros')).toBeInTheDocument()
  })

  it('separe deux groupes (deux heros) par un trait, et marque le groupe actif', () => {
    rendre([
      { cle: 'j0', unites: [unite('1', 'Spider-Man')], actif: true },
      { cle: 'j1', unites: [unite('2', 'Black Cat')] },
    ])
    expect(screen.getAllByRole('separator')).toHaveLength(1)
    const groupes = document.querySelectorAll('.rangee-cartes-groupe')
    expect(groupes[0]).toHaveClass('est-actif')
    expect(groupes[1]).not.toHaveClass('est-actif')
  })

  it('compte les cibles legales sur son etiquette', () => {
    rendre([{ cle: 'g', unites: [unite('1', 'A', 'targetable'), unite('2', 'B', 'disabled')] }], { cibles: 1 })
    expect(document.querySelector('.rangee-cartes-cibles')).toHaveTextContent('1')
  })

  it('ramene la premiere cible dans le champ quand un ciblage commence', () => {
    const { rerender } = rendre([{ cle: 'g', unites: [unite('1', 'A'), unite('2', 'B', 'targetable')] }])
    const cible = document.querySelector<HTMLElement>('.carte-posee:has(.state-targetable)')
    const recentrer = vi.fn()
    // jsdom n'implemente pas scrollIntoView ; on verifie l'APPEL, pas le defilement.
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', { value: recentrer, configurable: true })
    rerender(
      <RangeeCartes
        cle="heros"
        titre="Ton héros"
        groupes={[{ cle: 'g', unites: [unite('1', 'A'), unite('2', 'B', 'targetable')] }]}
        piles={[]}
        cibles={1}
        onOuvrirCarte={() => {}}
        onOuvrirPile={() => {}}
      />
    )
    expect(recentrer).toHaveBeenCalled()
    expect(cible).not.toBeNull()
  })

  it('affiche le voile +N et avance d\'un ecran au tap', () => {
    rendre([{ cle: 'g', unites: Array.from({ length: 6 }, (_, i) => unite(String(i), `C${i}`)) }])
    const defilement = document.querySelector<HTMLElement>('.rangee-cartes-defilement')!
    // jsdom ne mesure rien : on pose des mesures a la main, comme un vrai rendu.
    Object.defineProperty(defilement, 'clientWidth', { value: 400, configurable: true })
    ;[...defilement.querySelectorAll<HTMLElement>('.carte-posee')].forEach((carte, i) => {
      Object.defineProperty(carte, 'offsetLeft', { value: i * 108, configurable: true })
      Object.defineProperty(carte, 'offsetWidth', { value: 100, configurable: true })
    })
    fireEvent.scroll(defilement)
    const voile = screen.getByRole('button', { name: /3/ })
    expect(voile).toHaveClass('rangee-cartes-suite')
    const scrollBy = vi.fn()
    defilement.scrollBy = scrollBy
    fireEvent.click(voile)
    expect(scrollBy).toHaveBeenCalledWith({ left: 400, behavior: 'smooth' })
  })
})
```

Note sur le 5ᵉ test : jsdom ne supporte pas `:has()` dans `querySelector` dans toutes les versions ; si cette ligne lève, remplacer la recherche par `document.querySelector('.state-targetable')?.closest('.carte-posee')` dans le test ET dans le composant.

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/RangeeCartes.test.tsx
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `RangeeCartes.tsx`**

```tsx
// Une rangee du plateau paysage : son etiquette, ses cartes, ses piles.
//
// Les cartes DEFILENT horizontalement quand elles ne tiennent plus, avec
// accroche carte par carte. Rien n'est condense ni replie : douze sbires font
// douze cartes, et le voile « +N » au bord droit dit combien sont hors champ.
// Les piles (deck, defausse) sont epinglees a droite, hors du defilement.
//
// Pendant un ciblage, la rangee ramene sa premiere cible dans le champ : on ne
// doit pas avoir a chercher ce que le moteur demande de choisir.

import { Fragment, useCallback, useEffect, useRef, useState } from 'react'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import { CartePosee } from './CartePosee'
import { PilesEpinglees } from './PilesEpinglees'
import { mesurerHorsChamp } from './hors-champ'
import type { CleRangee } from './rangees'
import './paysage.css'

export type GroupeRangee = {
  cle: string
  unites: UniteAffichee[]
  /** Le groupe du heros ACTIF (solo a deux heros) : trait de couleur dessous. */
  actif?: boolean
}

export type RangeeCartesProps = {
  cle: CleRangee
  titre: string
  groupes: GroupeRangee[]
  piles: UniteAffichee[]
  /** Nombre de cibles legales ici pendant un ciblage. */
  cibles?: number
  /** Variations de compteurs en cours, par identifiant de carte. */
  effets?: Map<number, CardEffectDelta>
  onOuvrirCarte: (carte: ScanCardProps) => void
  onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void
}

export function RangeeCartes({
  cle,
  titre,
  groupes,
  piles,
  cibles,
  effets,
  onOuvrirCarte,
  onOuvrirPile,
}: RangeeCartesProps) {
  const defilement = useRef<HTMLDivElement>(null)
  const [horsChamp, setHorsChamp] = useState(0)
  const vide = groupes.every((groupe) => groupe.unites.length === 0)

  const mesurer = useCallback(() => {
    if (defilement.current) setHorsChamp(mesurerHorsChamp(defilement.current))
  }, [])

  // Remesure quand les cartes changent, et quand la fenetre change de taille
  // (rotation, barre du navigateur). ResizeObserver n'existe pas sous jsdom.
  useEffect(() => {
    mesurer()
    const element = defilement.current
    if (!element || typeof ResizeObserver === 'undefined') return
    const observateur = new ResizeObserver(mesurer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [mesurer, groupes])

  // Un ciblage commence : la premiere cible revient dans le champ.
  useEffect(() => {
    if (!cibles || !defilement.current) return
    const cible = defilement.current.querySelector<HTMLElement>('.state-targetable')?.closest<HTMLElement>('.carte-posee')
    if (cible && typeof cible.scrollIntoView === 'function') {
      cible.scrollIntoView({ inline: 'nearest', block: 'nearest', behavior: 'smooth' })
    }
  }, [cibles])

  const avancer = () => {
    const element = defilement.current
    if (element) element.scrollBy({ left: element.clientWidth, behavior: 'smooth' })
  }

  return (
    <section className={`rangee-cartes rangee-${cle}`} role="region" aria-label={titre}>
      <div className="rangee-cartes-titre">
        <span className="rangee-cartes-nom">{titre}</span>
        {cibles ? (
          <span className="rangee-cartes-cibles" aria-label={`${cibles} ${t('cibles ici')}`}>
            {cibles}
          </span>
        ) : null}
      </div>
      <div className="rangee-cartes-corps">
        <div className="rangee-cartes-defilement" ref={defilement} onScroll={mesurer}>
          {vide ? (
            <span className="rangee-cartes-vide">{t('Vide')}</span>
          ) : (
            groupes.map((groupe, index) => (
              <Fragment key={groupe.cle}>
                {index > 0 ? <span className="rangee-cartes-separateur" role="separator" /> : null}
                <div className={`rangee-cartes-groupe${groupe.actif ? ' est-actif' : ''}`}>
                  {groupe.unites.map((unite) => (
                    <CartePosee
                      key={unite.cle}
                      unite={unite}
                      effet={effets?.get(Number(unite.carte.id))}
                      onOuvrir={onOuvrirCarte}
                    />
                  ))}
                </div>
              </Fragment>
            ))
          )}
        </div>
        {horsChamp > 0 ? (
          <button
            type="button"
            className="rangee-cartes-suite"
            data-tactile="suite"
            aria-label={`${horsChamp} ${t('cartes hors champ')}`}
            onClick={avancer}
          >
            +{horsChamp}
          </button>
        ) : null}
        {piles.length > 0 ? <PilesEpinglees piles={piles} onOuvrirPile={onOuvrirPile} /> : null}
      </div>
    </section>
  )
}
```

- [ ] **Step 4 : Ajouter les règles CSS de la rangée dans `paysage.css`**

Dans le bloc `@layer composants`, avant les règles des piles :

```css
  /* --- Une rangee ----------------------------------------------------------- */

  .rangee-cartes {
    display: grid;
    grid-template-rows: var(--pp-etiquette-h, 14px) minmax(0, 1fr);
    min-height: 0;
  }

  .rangee-cartes-titre {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 10px;
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.55);
    line-height: var(--pp-etiquette-h, 14px);
  }

  .rangee-ennemie .rangee-cartes-titre { color: rgba(248, 113, 113, 0.8); }
  .rangee-heros .rangee-cartes-titre { color: rgba(96, 165, 250, 0.85); }

  .rangee-cartes-cibles {
    min-width: 16px;
    padding: 0 5px;
    border-radius: 99px;
    text-align: center;
    color: var(--fond);
    background: var(--menace);
  }

  .rangee-cartes-corps {
    position: relative;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    min-height: 0;
  }

  .rangee-cartes-defilement {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 4px 8px 0;
    overflow-x: auto;
    overflow-y: hidden;
    overscroll-behavior-x: contain;
    scroll-snap-type: x proximity;
    scrollbar-width: none;
  }

  .rangee-cartes-defilement::-webkit-scrollbar {
    display: none;
  }

  .rangee-cartes-groupe {
    display: flex;
    flex: none;
    gap: 8px;
    padding-bottom: 3px;
    border-bottom: 3px solid transparent;
  }

  .rangee-cartes-groupe.est-actif {
    border-bottom-color: #34d399;
  }

  .rangee-cartes-separateur {
    flex: none;
    align-self: stretch;
    width: 2px;
    margin: 0 4px;
    background: rgba(255, 255, 255, 0.25);
  }

  .rangee-cartes-vide {
    align-self: center;
    padding: 0 12px;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.35);
  }

  /* Le voile au bord droit de la zone defilante, AVANT les piles epinglees. */
  .rangee-cartes-suite {
    position: absolute;
    top: 0;
    bottom: 0;
    right: var(--pp-piles-w, 0px);
    width: 48px;
    border: 0;
    font: inherit;
    font-size: 0.9rem;
    font-weight: 900;
    color: #fff;
    background: linear-gradient(90deg, transparent, rgba(13, 15, 19, 0.96) 55%);
    cursor: pointer;
  }

  .rangee-cartes-corps:has(.piles-epinglees) {
    --pp-piles-w: 140px;
  }

  /* Pendant un ciblage ou un paiement, tout ce qui n'est pas visable s'eteint. */
  .plateau-paysage.est-en-ciblage .carte-posee {
    opacity: 0.28;
  }

  .plateau-paysage.est-en-ciblage .carte-posee:has(.scan-card.state-targetable),
  .plateau-paysage.est-en-ciblage .carte-posee:has(.scan-card.state-playable),
  .plateau-paysage.est-en-ciblage .carte-posee:has(.scan-card.state-selected) {
    opacity: 1;
  }
```

- [ ] **Step 5 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/RangeeCartes.test.tsx && npx tsc --noEmit
```

Attendu : 6 tests verts, `tsc` silencieux.

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/RangeeCartes.tsx ui-app/src/board/mobile/RangeeCartes.test.tsx ui-app/src/board/mobile/paysage.css
git commit -m "feat(plateau-mobile): une rangee de cartes qui defile, avec son voile +N

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 10 : EcranPortrait.tsx, « Tourne ton téléphone »

**Files:**
- Create: `ui-app/src/board/mobile/EcranPortrait.tsx`
- Test: `ui-app/src/board/mobile/EcranPortrait.test.tsx`
- Modify: `ui-app/src/board/mobile/paysage.css`, `ui-app/src/board/dico-en.ts`

**Interfaces:**
- Produces: `export function EcranPortrait()` (aucune prop). Un `div.ecran-portrait` avec `role="dialog"`, `aria-modal="true"`, `aria-label` « Tourne ton téléphone ».

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/EcranPortrait.test.tsx` :

```tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EcranPortrait } from './EcranPortrait'

describe('EcranPortrait', () => {
  it('est un dialogue modal qui demande de tourner le telephone', () => {
    render(<EcranPortrait />)
    const voile = screen.getByRole('dialog', { name: 'Tourne ton téléphone' })
    expect(voile).toHaveAttribute('aria-modal', 'true')
    expect(voile).toHaveClass('ecran-portrait')
    expect(screen.getByText('Le plateau se joue en paysage.')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/EcranPortrait.test.tsx
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `EcranPortrait.tsx`**

```tsx
// « Tourne ton telephone » : le voile qui couvre le plateau en portrait.
//
// Le plateau paysage n'a PAS de rendu portrait (spec du 07/09/2026, §3). Ce
// voile ne demonte rien : la partie continue dessous, la connexion au moteur
// aussi, et une question posee pendant la rotation est toujours la au retour.

import { t } from '../langue'
import './paysage.css'

export function EcranPortrait() {
  return (
    <div className="ecran-portrait" role="dialog" aria-modal="true" aria-label={t('Tourne ton téléphone')}>
      <span className="ecran-portrait-icone" aria-hidden="true" />
      <p>
        <strong>{t('Tourne ton téléphone')}</strong>
        <br />
        {t('Le plateau se joue en paysage.')}
      </p>
    </div>
  )
}
```

- [ ] **Step 4 : CSS et traductions**

Dans `paysage.css`, bloc `@layer composants`, ajouter :

```css
  /* --- L'ecran portrait ------------------------------------------------------ */

  .ecran-portrait {
    position: fixed;
    inset: 0;
    z-index: 900;
    display: grid;
    place-items: center;
    align-content: center;
    gap: 18px;
    padding: 24px;
    text-align: center;
    color: #f8fafc;
    background: #0d0f13;
    font-size: 1rem;
    line-height: 1.5;
  }

  .ecran-portrait-icone {
    width: 34px;
    height: 62px;
    border: 3px solid #f8fafc;
    border-radius: 8px;
    animation: ecran-portrait-tourne 1.6s ease-in-out infinite alternate;
  }

  @keyframes ecran-portrait-tourne {
    from { transform: rotate(0deg); }
    to { transform: rotate(-90deg); }
  }

  @media (prefers-reduced-motion: reduce) {
    .ecran-portrait-icone {
      animation: none;
      transform: rotate(-90deg);
    }
  }
```

Dans `ui-app/src/board/dico-en.ts`, ajouter dans l'objet `DICO_EN_BASE`, à la fin de la section « Partagé » (après la ligne `'Fermer': 'Close',`) :

```ts
  // ---- Plateau paysage (mobile/) ----
  'Tourne ton téléphone': 'Turn your phone',
  'Le plateau se joue en paysage.': 'The board is played in landscape.',
  'cartes hors champ': 'cards out of view',
  'cibles ici': 'targets here',
```

Si `'cibles ici'` existe déjà dans le dictionnaire (le médaillon l'utilise), ne pas le dupliquer : vérifier avec `grep -n "'cibles ici'" ui-app/src/board/dico-en.ts`.

- [ ] **Step 5 : Lancer le test, il doit passer**

```bash
npx vitest run src/board/mobile/EcranPortrait.test.tsx && npx tsc --noEmit
```

Attendu : 1 test vert.

- [ ] **Step 6 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/EcranPortrait.tsx ui-app/src/board/mobile/EcranPortrait.test.tsx ui-app/src/board/mobile/paysage.css ui-app/src/board/dico-en.ts
git commit -m "feat(plateau-mobile): l'ecran « Tourne ton telephone » en portrait

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 11 : PlateauPaysage.tsx, la composition

**Files:**
- Create: `ui-app/src/board/mobile/PlateauPaysage.tsx`
- Test: `ui-app/src/board/mobile/PlateauPaysage.test.tsx`
- Modify: `ui-app/src/board/mobile/PlateauMobile.tsx` (l'aiguillage rend `PlateauPaysage` par défaut)
- Modify: `ui-app/src/board/mobile/paysage.css` (grille du plateau, tailles de carte, cartouche du déroulé)

**Interfaces:**
- Consumes: `BoardProps`, `avecInteraction`, `phaseAffichee` de `../Board` ; `repartirEnRangees`, `unitesDe`, `mainDe` (tâche 2) ; `RangeeCartes`, `GroupeRangee` (tâche 9) ; `EcranPortrait` (tâche 10) ; `usePleinEcranAuPremierGeste`, `doitMontrerEcranPortrait` (tâche 6) ; `groupesParJoueur`, `ordreDAffichage`, `carteIdentite` de `./joueurs` ; `useCouches`, `useCouchesBoard` de `./couches` ; `MainEventail`, `BarreBas`, `CarteOuverte`, `useOrientation` existants.
- Produces: `export function PlateauPaysage(props: BoardProps)`.

Comportement, dans l'ordre du rendu : `div.plateau-mobile.plateau-paysage.est-<orientation>` (+ `est-en-ciblage`, `est-en-paiement`), `div.pp-rangees` avec les deux `RangeeCartes`, `MainEventail`, la barre (bouton Payer ou `BarreBas`, copié de `PlateauMedaillons`), `CarteOuverte`, la pile regardée (copiée de `PlateauMedaillons`), `EcranPortrait` en portrait. Pendant le montage, `document.body` porte la classe `mode-plateau-paysage` (le cartouche du déroulé s'y adosse, §4.7).

Rangée héros à deux héros : `terrain-soutien` est éclaté par joueur (`groupesParJoueur`), un `GroupeRangee` par joueur, dans l'ordre `ordreDAffichage(joueurs, joueurActif)`, où `joueurActif` est le joueur dont la carte d'identité (`carteIdentite`) porte l'id `heroActifId`, sinon `playerId`. Les autres emplacements de la rangée (`deck-special`, `reserve`, `nemesis`) forment un dernier groupe `annexes-heros`. L'identité du joueur actif reçoit `estActif: true`.

- [ ] **Step 1 : Écrire le test**

`ui-app/src/board/mobile/PlateauPaysage.test.tsx` :

```tsx
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauPaysage } from './PlateauPaysage'
import { REQUETE_PAYSAGE } from './useOrientation'
import type { EtatInteractif } from '../interaction'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { World } from '../world'

const MONDE = { phase: 'Player 1 Turn', round_id: 3, prompt: '', players: [] } as unknown as World

const unite = (id: string, name: string, kind: UniteAffichee['carte']['kind'], extra: Partial<UniteAffichee['carte']> = {}): UniteAffichee => ({
  cle: `u${id}`,
  carte: { id, name, kind, imageUrl: '', ...extra },
  attachees: [],
})

function plateau(emplacements: EmplacementAffiche[]): Plateau {
  return {
    emplacements,
    nombreDeCartes: emplacements.length,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

const PLATEAU = plateau([
  { cle: 'rencontre', titre: 'Méchant', nombreSurLaLigne: 1, groupes: [[unite('1', 'Rhino', 'villain', { allyHp: '12/22' })]] },
  { cle: 'piles-rencontre', titre: 'Piles', nombreSurLaLigne: 1, groupes: [[{ ...unite('20', 'Encounter deck', 'villain', { facedown: true, pileCount: 23 }), pileTitre: 'Deck de rencontre' }]] },
  {
    cle: 'terrain-soutien', titre: 'Héros', nombreSurLaLigne: 3,
    groupes: [[unite('2', 'Spider-Man', 'hero')], [unite('3', 'Black Cat', 'hero')], [unite('4', 'Aunt May', 'ally')]],
    proprietaires: [0, 1, 1],
  },
  { cle: 'main', titre: 'Main', nombreSurLaLigne: 2, groupes: [[unite('5', 'Backflip', 'event'), unite('6', 'Enhanced Spider-Sense', 'event')]] },
])

/** Orientation simulee : paysage par defaut. */
function orienter(paysage: boolean) {
  vi.stubGlobal('matchMedia', (requete: string) => ({
    media: requete,
    matches: requete === REQUETE_PAYSAGE ? paysage : false,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  }))
}

const cartePosee = (id: string) =>
  document.querySelector<HTMLElement>(`.carte-posee:has(.scan-card[data-card-id="${id}"])`)

describe('PlateauPaysage', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    document.body.className = ''
  })

  it('dessine les deux rangees, la main et la barre, sans ecran portrait en paysage', () => {
    orienter(true)
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} />)
    expect(screen.getByRole('region', { name: 'Méchant' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: /Ton héros/ })).toBeInTheDocument()
    expect(cartePosee('1')).not.toBeNull()
    expect(screen.getByText('12/22')).toBeInTheDocument()
    expect(screen.getByText('Deck de rencontre')).toBeInTheDocument()
    expect(document.querySelector('.main-eventail')).toBeInTheDocument()
    expect(document.querySelector('.pm-barre')).toBeInTheDocument()
    expect(screen.queryByRole('dialog', { name: 'Tourne ton téléphone' })).toBeNull()
    expect(document.body).toHaveClass('mode-plateau-paysage')
  })

  it('couvre le plateau de l\'ecran portrait sans le demonter', () => {
    orienter(false)
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} />)
    expect(screen.getByRole('dialog', { name: 'Tourne ton téléphone' })).toBeInTheDocument()
    expect(cartePosee('1')).not.toBeNull()
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-portrait')
  })

  it('separe deux heros en deux groupes, le heros actif en premier et marque', () => {
    orienter(true)
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} heroActifId={3} />)
    const groupes = [...document.querySelectorAll<HTMLElement>('.rangee-heros .rangee-cartes-groupe')]
    // Black Cat (joueur 1) est active : son groupe passe devant celui de Spider-Man.
    expect(groupes[0]).toHaveClass('est-actif')
    expect(groupes[0].querySelector('.scan-card')).toHaveAttribute('data-card-id', '3')
    expect(groupes[1].querySelector('.scan-card')).toHaveAttribute('data-card-id', '2')
    expect(screen.getAllByRole('separator')).toHaveLength(1)
    // Le badge « Active » de ScanCard suit heroActifId.
    expect(groupes[0].querySelector('.scan-card')?.textContent).toMatch(/Active|Actif/)
  })

  it('le tap sur une carte l\'ouvre en grand, et l\'action part de la carte ouverte', () => {
    orienter(true)
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'porteur', choisie: false, agir }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    fireEvent.click(cartePosee('1')!)
    expect(agir).not.toHaveBeenCalled()
    expect(screen.getByRole('dialog', { name: 'Rhino' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Utiliser cette carte/ }))
    expect(agir).toHaveBeenCalledOnce()
  })

  it('pendant un ciblage, la rangee compte ses cibles et le plateau s\'eteint', () => {
    orienter(true)
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'cible', choisie: false, agir: () => {} }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    expect(document.querySelector('.rangee-ennemie .rangee-cartes-cibles')).toHaveTextContent('1')
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-en-ciblage')
  })

  it('un paiement demande montre « Payer » avant d\'eteindre le plateau', () => {
    orienter(true)
    const interactifs = new Map<number, EtatInteractif>([[5, { role: 'ressource', choisie: false, agir: () => {} }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    expect(document.querySelector('.plateau-paysage')).not.toHaveClass('est-en-paiement')
    fireEvent.click(screen.getByRole('button', { name: 'Payer' }))
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-en-paiement')
  })

  it('etale une pile epinglee au tap', () => {
    orienter(true)
    const defausse: EmplacementAffiche = {
      cle: 'piles-joueur', titre: 'Piles', nombreSurLaLigne: 1,
      groupes: [[{ ...unite('30', 'Backflip', 'event', { discard: true }), pileTitre: 'Défausse', pileContenu: [unite('31', 'Backflip', 'event').carte] }]],
    }
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={plateau([...PLATEAU.emplacements, defausse])} />)
    fireEvent.click(screen.getByRole('button', { name: /Défausse/ }))
    expect(screen.getByRole('dialog', { name: 'Défausse' })).toBeInTheDocument()
  })
})
```

Si jsdom refuse `:has()` dans `querySelector`, remplacer l'aide `cartePosee` par `document.querySelector(`.scan-card[data-card-id="${id}"]`)?.closest<HTMLElement>('.carte-posee') ?? null`.

- [ ] **Step 2 : Lancer le test, il doit échouer**

```bash
npx vitest run src/board/mobile/PlateauPaysage.test.tsx
```

Attendu : échec, import introuvable.

- [ ] **Step 3 : Écrire `PlateauPaysage.tsx`**

```tsx
// Le plateau en PAYSAGE : deux rangees de vraies cartes.
//
// Spec : docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md §4.
// Ce n'est ni le plateau PC en petit (65 px de carte a l'echelle, illisible),
// ni le modele a medaillons d'aout (des jetons ronds qui perdaient trop d'un
// terrain qui est grand). C'est la table, lue en deux lignes :
//
//   rangee ENNEMIE : mechant, manigances, sbires, environnement | piles rencontre
//   rangee HEROS   : identite(s), allies, soutiens, ameliorations | piles joueur
//   la MAIN en eventail, la BARRE du bas
//
// Une rangee qui deborde DEFILE. Rien n'est condense. En portrait, EcranPortrait
// couvre tout sans rien demonter. Il accepte exactement les BoardProps du
// plateau PC : c'est ce qui permet a board.tsx de choisir l'un ou l'autre.

import { useEffect, useMemo, useState } from 'react'
import { avecInteraction, phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { EmplacementAffiche, UniteAffichee } from '../zones'
import { BarreBas } from './BarreBas'
import { CarteOuverte } from './CarteOuverte'
import { EcranPortrait } from './EcranPortrait'
import { MainEventail } from './MainEventail'
import { RangeeCartes, type GroupeRangee } from './RangeeCartes'
import { useCouches, useCouchesBoard } from './couches'
import { carteIdentite, groupesParJoueur, ordreDAffichage } from './joueurs'
import { doitMontrerEcranPortrait, usePleinEcranAuPremierGeste } from './plein-ecran'
import { mainDe, repartirEnRangees, unitesDe, type RangeeAffichee } from './rangees'
import { useOrientation } from './useOrientation'
import './medaillon.css'
import './paysage.css'

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()
const AUCUN_EFFET: Map<number, CardEffectDelta> = new Map()

/** Les emplacements de la rangee heros qui ne sont pas l'aire des joueurs. */
const ANNEXES_HEROS = new Set<EmplacementAffiche['cle']>(['deck-special', 'reserve', 'nemesis'])

function decorerUnite(
  unite: UniteAffichee,
  decorer: (carte: ScanCardProps) => ScanCardProps
): UniteAffichee {
  return { ...unite, carte: decorer(unite.carte), attachees: unite.attachees.map(decorer) }
}

/**
 * La rangee heros, groupe par groupe : un groupe par joueur (le joueur actif
 * d'abord), puis les annexes (deck special, reserve, nemesis). En solo a un
 * heros, `proprietaires` est absent et tout revient au joueur 0 : un seul
 * groupe, comme avant.
 */
function groupesHeros(rangee: RangeeAffichee, joueurActif: number): GroupeRangee[] {
  const aire = rangee.defilants.find((emplacement) => emplacement.cle === 'terrain-soutien')
  const groupes: GroupeRangee[] = []
  if (aire) {
    const parJoueur = groupesParJoueur(aire)
    for (const joueur of ordreDAffichage([...parJoueur.keys()], joueurActif)) {
      groupes.push({
        cle: `joueur-${joueur}`,
        unites: (parJoueur.get(joueur) ?? []).flat(),
        actif: parJoueur.size > 1 && joueur === joueurActif,
      })
    }
  }
  const annexes = unitesDe(rangee.defilants.filter((emplacement) => ANNEXES_HEROS.has(emplacement.cle)))
  if (annexes.length > 0) groupes.push({ cle: 'annexes-heros', unites: annexes })
  return groupes
}

/** Le joueur dont l'identite porte `heroActifId`, sinon le joueur local. */
function joueurDeLIdentite(rangee: RangeeAffichee, heroActifId: number | undefined, defaut: number): number {
  if (heroActifId === undefined) return defaut
  const aire = rangee.defilants.find((emplacement) => emplacement.cle === 'terrain-soutien')
  if (!aire) return defaut
  for (const [joueur, groupes] of groupesParJoueur(aire)) {
    if (Number(carteIdentite(groupes)?.id) === heroActifId) return joueur
  }
  return defaut
}

export function PlateauPaysage({
  world,
  playerId,
  plateau,
  bas,
  outils,
  actionsPartie,
  interactifs = AUCUNE_INTERACTION,
  effets = AUCUN_EFFET,
  heroActifId,
  carteFocalisee,
  onFermerCarte,
  selecteurOuvert = false,
  onFermerSelecteur,
  onCardClick,
}: BoardProps) {
  const orientation = useOrientation()
  const couches = useCouches()
  useCouchesBoard(carteFocalisee, selecteurOuvert, couches, onFermerCarte, onFermerSelecteur)
  usePleinEcranAuPremierGeste(true)

  // Le cartouche du deroule (DeroulePhase, rendu par la page a cote du
  // plateau) s'adosse a la barre du bas quand cette classe est la : voir
  // paysage.css. Posee sur body parce que le cartouche n'est pas dans cet arbre.
  useEffect(() => {
    document.body.classList.add('mode-plateau-paysage')
    return () => document.body.classList.remove('mode-plateau-paysage')
  }, [])

  const [pileRegardee, setPileRegardee] = useState<{ titre: string; cartes: ScanCardProps[] } | undefined>()
  const [carteOuverte, setCarteOuverte] = useState<ScanCardProps | undefined>()

  // Les etats d'interaction sont poses sur chaque carte AVANT le decoupage ; le
  // badge « Active » suit heroActifId, comme sur le plateau PC.
  const rangees = useMemo(() => {
    const decorer = (carte: ScanCardProps) => {
      const decoree = avecInteraction(carte, interactifs, effets)
      return heroActifId !== undefined && Number(carte.id) === heroActifId ? { ...decoree, estActif: true } : decoree
    }
    const decorerEmplacement = (emplacement: EmplacementAffiche): EmplacementAffiche => ({
      ...emplacement,
      groupes: emplacement.groupes.map((groupe) => groupe.map((unite) => decorerUnite(unite, decorer))),
    })
    return repartirEnRangees(plateau).map((rangee) => ({
      ...rangee,
      defilants: rangee.defilants.map(decorerEmplacement),
      epingles: rangee.epingles.map(decorerEmplacement),
    }))
  }, [plateau, interactifs, effets, heroActifId])

  const [ennemie, heros] = rangees
  const joueurActif = joueurDeLIdentite(heros, heroActifId, playerId)

  const ciblesDe = (rangee: RangeeAffichee): number =>
    unitesDe(rangee.defilants).filter((unite) => {
      const etat = interactifs.get(Number(unite.carte.id))
      return etat?.role === 'cible' || etat?.role === 'cible-preview'
    }).length
  const ciblesEnnemie = ciblesDe(ennemie)
  const ciblesHeros = ciblesDe(heros)
  const enCiblage = ciblesEnnemie + ciblesHeros > 0

  // Un PAIEMENT est en cours des qu'une carte porte le role « ressource ». Tant
  // qu'on n'a pas touche « Payer », le plateau reste normal : on peut reculer.
  const paiementDemande = useMemo(
    () => [...interactifs.values()].some((etat) => etat.role === 'ressource'),
    [interactifs]
  )
  const [paiementAccepte, setPaiementAccepte] = useState(false)
  useEffect(() => {
    if (!paiementDemande) setPaiementAccepte(false)
  }, [paiementDemande])
  const enPaiement = paiementDemande && paiementAccepte

  const main = useMemo(
    () => mainDe(plateau).map((unite) => avecInteraction(unite.carte, interactifs, effets)),
    [plateau, interactifs, effets]
  )

  // Depuis la MAIN (appui long) ou la carte ouverte : on agit directement.
  const jouerCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }
  const ouvrirPile = (titre: string, cartes: ScanCardProps[]) => setPileRegardee({ titre, cartes })

  return (
    <div
      className={
        `plateau-mobile plateau-paysage est-${orientation}` +
        (enCiblage || enPaiement ? ' est-en-ciblage' : '') +
        (enPaiement ? ' est-en-paiement' : '')
      }
    >
      <div className="pp-rangees">
        <RangeeCartes
          cle="ennemie"
          titre={ennemie.titre}
          groupes={[{ cle: 'ennemie', unites: unitesDe(ennemie.defilants) }]}
          piles={unitesDe(ennemie.epingles)}
          cibles={ciblesEnnemie || undefined}
          effets={effets}
          onOuvrirCarte={setCarteOuverte}
          onOuvrirPile={ouvrirPile}
        />
        <RangeeCartes
          cle="heros"
          titre={`${heros.titre} · ${phaseAffichee(world.phase)}`}
          groupes={groupesHeros(heros, joueurActif)}
          piles={unitesDe(heros.epingles)}
          cibles={ciblesHeros || undefined}
          effets={effets}
          onOuvrirCarte={setCarteOuverte}
          onOuvrirPile={ouvrirPile}
        />
      </div>

      <MainEventail cartes={main} modePaiement={enPaiement} onJouer={jouerCarte} />

      {paiementDemande && !paiementAccepte ? (
        <div className="pm-barre pm-barre-demande">
          <button type="button" className="pm-payer" onClick={() => setPaiementAccepte(true)}>
            {t('Payer')}
          </button>
          {bas}
        </div>
      ) : (
        <BarreBas demande={bas} outils={actionsPartie} onglets={outils} />
      )}

      {carteOuverte ? (
        <CarteOuverte carte={carteOuverte} onFermer={() => setCarteOuverte(undefined)} />
      ) : null}

      {pileRegardee ? (
        <div className="focus-voile" onPointerDown={() => setPileRegardee(undefined)}>
          <section
            className="focus"
            role="dialog"
            aria-label={pileRegardee.titre}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="focus-entete">
              <h2>{pileRegardee.titre}</h2>
              <button type="button" className="focus-fermer" onClick={() => setPileRegardee(undefined)}>
                {t('Fermer')}
              </button>
            </header>
            <div className="focus-corps">
              <div className="focus-cartes">
                {pileRegardee.cartes.map((carte) => (
                  <span key={carte.id}>
                    <img className="pile-carte" src={carte.imageUrl} alt={carte.name} />
                  </span>
                ))}
              </div>
            </div>
          </section>
        </div>
      ) : null}

      {doitMontrerEcranPortrait(orientation) ? <EcranPortrait /> : null}
    </div>
  )
}
```

Note : les classes `focus-voile`, `focus`, `focus-entete`, `focus-corps`, `focus-cartes` de la pile regardée vivent dans `mobile.css` (chargé par `MainEventail`). Elles y restent jusqu'au sous-projet 3.

- [ ] **Step 4 : Brancher l'aiguillage**

Dans `PlateauMobile.tsx` (tâche 1), remplacer les deux dernières lignes de la fonction par :

```tsx
import { PlateauPaysage } from './PlateauPaysage'
// ...
export function PlateauMobile(props: BoardProps) {
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  return <PlateauPaysage {...props} />
}
```

et retirer le commentaire « PlateauPaysage arrive a la tache 11 ».

- [ ] **Step 5 : La grille du plateau, les tailles de carte et le cartouche, dans `paysage.css`**

Dans le bloc `@layer composants`, tout en haut (avant « Une carte posée ») :

```css
  /* --- Le plateau ------------------------------------------------------------
     Deux rangees de hauteur egale, la main qui flotte par-dessus (hors flux,
     voir .main-eventail dans medaillon.css), la barre du bas. La largeur de
     carte se DEDUIT de la hauteur : meme formule que taille-carte.ts. */
  .plateau-paysage {
    --pp-etiquette-h: 14px;
    --pp-main-h: 90px;
    --pm-barre-h: 48px;
    --pp-card-w: clamp(84px, calc((100dvh - 166px) / 2 * 63 / 88), 150px);
    box-sizing: border-box;
    position: relative;
    display: grid;
    grid-template-rows: minmax(0, 1fr) auto;
    height: 100dvh;
    padding-top: env(safe-area-inset-top, 0px);
    overflow: hidden;
    background: var(--fond, #0d0f13);
  }

  .pp-rangees {
    display: grid;
    grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
    min-height: 0;
    /* La main en eventail recouvre ce bas de plateau : on le laisse vide. */
    padding-bottom: var(--pp-main-h);
  }

  /* Le cartouche du deroule (DeroulePhase, board.css) est pose en fixed a
     31vh du bas pour la scene PC. Ici il prend la place de la main : elle n'est
     pas jouable pendant la phase du mechant, et la hauteur ne permet pas les
     deux. */
  body.mode-plateau-paysage .deroule-phase {
    bottom: var(--pm-barre-h, 48px);
    width: calc(100vw - 24px);
    max-height: calc(100dvh - 48px - 16px);
    padding: 10px 14px 12px;
  }
```

À la fin du fichier, dans le bloc `@layer utilitaires` créé à la tâche 8, ajouter :

```css
  .plateau-paysage .carte-posee .scan-card {
    --card-w: var(--pp-card-w);
    --inspect-scale: 1;
  }

  /* Une manigance se pose en paysage : meme HAUTEUR que ses voisines. ScanCard
     donne a une carte paysage une hauteur de --card-w * 127 / 176 ; pour
     retrouver la hauteur d'une carte portrait (--pp-card-w * 176 / 127), la
     largeur vaut donc --pp-card-w * (176 / 127)². */
  .plateau-paysage .carte-posee .scan-card.is-landscape {
    --card-w: calc(var(--pp-card-w) * 176 / 127 * 176 / 127);
  }

  /* La main s'aligne sur la largeur des cartes posees. */
  .plateau-paysage .main-eventail {
    --main-carte-w: var(--pp-card-w);
  }
```

- [ ] **Step 6 : Lancer les tests et les types**

```bash
npx vitest run src/board/mobile && npx tsc --noEmit
```

Attendu : tout vert (les anciens tests `PlateauMedaillons.test.tsx` compris), `tsc` silencieux.

- [ ] **Step 7 : La suite complète**

```bash
npx vitest run
```

Attendu : même nombre de verts qu'avant le plan, plus les nouveaux ; aucun rouge nouveau. Noter le nombre dans le message de commit.

- [ ] **Step 8 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/mobile/PlateauPaysage.tsx ui-app/src/board/mobile/PlateauPaysage.test.tsx ui-app/src/board/mobile/PlateauMobile.tsx ui-app/src/board/mobile/paysage.css
git commit -m "feat(plateau-mobile): le plateau paysage, deux rangees de vraies cartes

Rendu par defaut du mode mobile. Deux heros en deux groupes, le cartouche du
deroule adosse a la barre, l'ecran portrait par-dessus. vitest : N verts.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 12 : Le filet Playwright en 1050 x 480, et l'écran portrait

**Files:**
- Create: `ui-check/tests/plateau-paysage.spec.ts`
- Modify: `ui-check/playwright.config.ts:23-29` (gabarit), `:65-90` (projets)
- Modify: `ui-check/package.json` (script `plateau-paysage`)

**Interfaces:**
- Consumes: la page `/fixtures.html` qui expose `window.FIXTURES` (34 entrées `{ fichier, titre }`), la page `/app/board.html?etat=<fichier>` qui monte le plateau depuis un état enregistré.
- Produces: la commande `npm run plateau-paysage` dans `ui-check`.

Prérequis d'exécution : le jeu doit tourner sur un port. `serveur-dev.py` vise par défaut `~/marvel-work/fusion/marvel-lcg-src`, qui **n'existe plus** (supprimé le 31/08/2026, voir `ui-app/deployer.sh`) : passer `--jeu` explicitement. Le build de `ui-app` doit avoir été déployé (`bash ui-app/deployer.sh`) avant, sinon la page sert l'ancien bundle.

- [ ] **Step 1 : Le gabarit et les projets Playwright**

Dans `ui-check/playwright.config.ts`, remplacer le bloc `GABARITS` par :

```ts
const GABARITS = {
  pc: { width: 1920, height: 1080 }, // Ordinateur
  tablette: { width: 1180, height: 820 }, // iPad Air, paysage
  mobile: { width: 390, height: 844 }, // iPhone 12/13/14
  // Samsung S24 Ultra en portrait : sert a verifier l'ecran « Tourne ton
  // telephone » du plateau paysage, et l'ancien rendu a medaillons (?medaillons).
  s24: { width: 480, height: 1050 },
  // Samsung S24 Ultra en PAYSAGE, plein ecran : l'appareil de reference du
  // plateau paysage (spec du 07/09/2026).
  s24paysage: { width: 1050, height: 480 },
};
```

Dans `projects`, remplacer `.filter(([name]) => name !== 's24')` par `.filter(([name]) => name !== 's24' && name !== 's24paysage')`, puis remplacer le `testMatch` du projet `s24` par `testMatch: /plateau-(mobile|paysage)\.spec\.ts$/,` et ajouter après ce projet :

```ts
    {
      name: 's24-paysage',
      testMatch: /plateau-paysage\.spec\.ts$/,
      use: {
        viewport: GABARITS.s24paysage,
        hasTouch: true,
        isMobile: true,
        deviceScaleFactor: 1,
      },
    },
```

Dans `ui-check/package.json`, ajouter après la ligne `"plateau-mobile"` :

```json
    "plateau-paysage": "playwright test tests/plateau-paysage.spec.ts --project=s24-paysage --project=s24",
```

- [ ] **Step 2 : Écrire `plateau-paysage.spec.ts`**

```ts
// Le plateau paysage tient-il a l'ecran, en vraies cartes lisibles, au doigt ?
//
// Sur les 34 etats enregistres, en 1050 x 480 (projet s24-paysage) :
//   1. le plateau ne deborde JAMAIS verticalement ;
//   2. chaque carte posee mesure au moins 84 px de large (le plancher de
//      lisibilite de la spec) ;
//   3. toute cible tactile mesure au moins 44 px dans les deux axes ;
//   4. aucun ecran portrait n'est affiche.
// Et en 480 x 1050 (projet s24), sur trois etats : l'ecran « Tourne ton
// telephone » couvre toute la fenetre.
//
//   npm run plateau-paysage
//
// La page est ouverte avec ?etat=<fixture> : aucune partie n'a besoin de tourner.
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;
const CARTE_MINIMUM = 84;
const TOLERANCE_ARRONDI = 1;

type Entree = { fichier: string; titre: string };

async function catalogue(page: import('@playwright/test').Page): Promise<Entree[]> {
  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });
  expect(await page.title()).not.toBe(TITRE_PAGE_AVERTISSEMENT);
  const entrees: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );
  expect(entrees.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);
  return entrees;
}

test('En paysage, deux rangees de vraies cartes qui tiennent a l\'ecran', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24-paysage', 'Gabarit paysage seulement');
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  for (const entree of await catalogue(page)) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });

      const vue = page.locator('.plateau-paysage');
      await expect(vue, 'Le rendu paysage ne s\'est pas monte').toBeVisible();
      await expect(page.locator('.ecran-portrait'), 'Ecran portrait affiche en paysage').toHaveCount(0);

      // 1. Rien ne deborde verticalement.
      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `Le plateau deborde de ${debordement.contenu - debordement.visible} px`
      ).toBeLessThanOrEqual(debordement.visible + TOLERANCE_ARRONDI);

      // 2. Chaque carte posee se lit : au moins 84 px de large.
      const cartes = page.locator('.carte-posee > .scan-card');
      const nombreCartes = await cartes.count();
      expect(nombreCartes, 'Aucune carte posee dessinee').toBeGreaterThan(0);
      for (let index = 0; index < nombreCartes; index += 1) {
        const boite = await cartes.nth(index).boundingBox();
        if (!boite) continue;
        expect(boite.width, `Carte trop etroite (${Math.round(boite.width)} px)`).toBeGreaterThanOrEqual(CARTE_MINIMUM);
      }

      // 3. Toute cible tactile respecte le plancher de 44 px.
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

test('En portrait, l\'ecran « Tourne ton telephone » couvre tout', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24', 'Gabarit portrait seulement');
  const entrees = (await catalogue(page)).slice(0, 3);
  const fenetre = page.viewportSize();
  expect(fenetre).not.toBeNull();

  for (const entree of entrees) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const voile = page.locator('.ecran-portrait');
      await expect(voile).toBeVisible();
      const boite = await voile.boundingBox();
      expect(boite?.width).toBe(fenetre!.width);
      expect(boite?.height).toBe(fenetre!.height);
      // Le plateau est toujours la, dessous : rien n'a ete demonte.
      await expect(page.locator('.plateau-paysage')).toHaveCount(1);
    });
  }
});
```

- [ ] **Step 3 : Déployer le build et lancer le jeu**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && bash ui-app/deployer.sh
~/marvel-work/python/bin/python3.10 ui-check/scripts/serveur-dev.py --port 2346 \
  --jeu "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
```

Le serveur doit tourner en arrière-plan pendant le test (lancer dans un second terminal, ou avec `run_in_background`). Attendu : `deployer.sh` vert (build, garde-fou d'extensions), le serveur annonce son port.

- [ ] **Step 4 : Lancer le filet, l'ancien et le nouveau**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE
npm run plateau-paysage
npm run plateau-mobile
```

Attendu : `plateau-paysage` : 2 tests verts (paysage sur 34 états, portrait sur 3). `plateau-mobile` : 1 test vert (l'ancien rendu derrière `?medaillons`). Si le paysage échoue sur la largeur de carte ou un débordement, c'est le CSS de la tâche 11 qui est en cause : corriger `paysage.css`, redéployer, relancer. Ne pas assouplir les seuils.

- [ ] **Step 5 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-check/tests/plateau-paysage.spec.ts ui-check/playwright.config.ts ui-check/package.json
git commit -m "test(plateau-mobile): le filet Playwright du plateau paysage, 34 etats en 1050x480

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

### Task 13 : Premier regard sur le téléphone et journal de session

**Files:**
- Modify: `.twei/SESSION.md` (nouvelle section en tête)
- Modify: `.planning/ROADMAP.md:50` (phase 6, une ligne)

Cette tâche ne contient pas de code. Elle livre le plateau sur l'installation servie par le tunnel et note ce qui est prouvé et ce qui ne l'est pas. La partie terrain complète est le sous-projet 3.

- [ ] **Step 1 : Déployer et vérifier que le bundle servi est le bon**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && bash ui-app/deployer.sh
grep -l "plateau-paysage" Fusion/marvel-lcg-src/public/app/assets/*.css 2>/dev/null || grep -rl "plateau-paysage" Fusion/marvel-lcg-src/public/app | head -3
```

Attendu : au moins un fichier du bundle contient `plateau-paysage`.

- [ ] **Step 2 : Regarder sur le téléphone**

Demander à l'utilisateur d'ouvrir, depuis son S24 Ultra par le tunnel, une partie solo Rhino / Spider-Man, puis en paysage : les deux rangées, la main, la barre ; tourner en portrait : l'écran « Tourne ton téléphone » ; retourner en paysage : la partie intacte. Consigner ses retours tels quels dans SESSION.md. Ne rien corriger dans cette tâche : chaque retour devient un point du sous-projet 3 ou un correctif séparé.

- [ ] **Step 3 : Journal de session**

En tête de `.twei/SESSION.md`, ajouter une section « 7 septembre 2026 : LE PLATEAU PAYSAGE » qui dit : ce qui est livré (fichiers, commits), les nombres exacts (vitest, Playwright sur 34 états), la commande de relance avec `--jeu` (le défaut de `serveur-dev.py` est mort depuis le 31/08), ce qui reste (sous-projets 2 et 3 de la spec, suppression des médaillons après terrain), et les retours du téléphone.

Dans `.planning/ROADMAP.md`, ligne de la phase 6, ajouter en fin de ligne : « Revue le 07/09/2026 : paysage obligatoire, vraies cartes en deux rangées (`ui-app/src/board/mobile/PlateauPaysage.tsx`), filet `ui-check/tests/plateau-paysage.spec.ts`. Spec `docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md`. »

- [ ] **Step 4 : Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add .twei/SESSION.md .planning/ROADMAP.md
git commit -m "docs(session): le plateau paysage livre, retours du telephone consignes

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01A3bPgQydPKpeVwCGcj1NZz"
```

---

## Auto-revue du plan

**Couverture de la spec (§4, §5, §7.1 côté plateau) :**

| Exigence | Tâche |
|---|---|
| §4.1 composition, ordre des emplacements, piles épinglées | 2, 8, 9, 11 |
| §4.2 taille de carte (formule, plancher, plafond, manigance paysage) | 3, 11 (CSS) |
| §4.3 défilement, voile +N, recalage sur la première cible, extinction pendant ciblage | 5, 9 |
| §4.4 états en pastilles, améliorations glissées avec tap | 4, 7 |
| §4.5 deux héros, joueur actif en premier, badge Actif | 11 |
| §4.6 tap ouvre `CarteOuverte`, pile de couches conservée | 7, 11 |
| §4.7 cartouche du déroulé à la place de la main | 11 (CSS `body.mode-plateau-paysage`) |
| §4.8 plein écran au premier geste, écran portrait sans démontage | 6, 10, 11 |
| §4.9 médaillons conservés derrière `?medaillons` jusqu'au sous-projet 3 | 1 |
| §5.1 modules purs testés | 2, 3, 4, 5, 6 |
| §5.3 rangée vide, débordement, plein écran refusé, rotation en pleine question | 9 (`Vide`), 5, 6, 11 |
| §7.1 vitest, projet Playwright 1050 x 480, contrôle portrait | 12 |

Écart assumé : §5.3 « écran plus bas que 360 px » n'a pas de règle CSS dédiée dans ce plan ; le `clamp` à 84 px et `overflow: hidden` du plateau en tiennent lieu, et le filet Playwright ne le mesure pas. À traiter si le téléphone le montre.

**Cohérence des noms entre tâches :** `repartirEnRangees`, `unitesDe`, `mainDe`, `RangeeAffichee` (2) ; `largeurCarte`, `HAUTEUR_FIXE` (3) ; `separerAttachees`, `etatDe` (4) ; `mesurerHorsChamp`, `nombreHorsChamp` (5) ; `doitMontrerEcranPortrait`, `usePleinEcranAuPremierGeste`, `demanderPleinEcranPaysage` (6) ; `CartePosee` avec `data-tactile="carte"` (7) ; `PilesEpinglees` avec `onOuvrirPile(titre, cartes)` (8) ; `RangeeCartes`, `GroupeRangee` (9) ; `EcranPortrait` (10) ; `PlateauPaysage` (11) ; classes CSS `.plateau-paysage`, `.pp-rangees`, `.rangee-cartes*`, `.carte-posee*`, `.pile-epinglee*`, `.ecran-portrait` (7 à 12).
