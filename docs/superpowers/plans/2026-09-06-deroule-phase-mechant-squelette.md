# Déroulé détaillé de la phase du méchant — livraison 1, le squelette

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dérouler la phase du méchant étape par étape, chaque étape montrant sa carte et attendant une validation, jouable de bout en bout — sans aucun effet visuel.

**Architecture:** Un module pur (`deroule-phase.ts`) transforme les faits du moteur et les entrées du journal en une liste d'étapes ordonnées. Un composant (`DeroulePhase.tsx`) affiche l'étape courante dans un cartouche fixe et pilote la navigation. Aucun flux nouveau n'est demandé au moteur Python.

**Tech Stack:** React 19, TypeScript strict, Vitest, Testing Library.

**Spec:** `docs/superpowers/specs/2026-09-06-phase-mechant-deroule-detaille-design.md`

## Global Constraints

- **TypeScript strict, zéro `any`** sans justification écrite sur place.
- **Bilingue dès le départ** : tout texte affiché passe par `t()` de
  `src/board/langue.ts`, avec son entrée dans `src/board/dico-en.ts`.
- **Pas d'em dash** dans les textes affichés ni dans les commentaires.
- **Commentaires en français**, expliquant le POURQUOI, comme le reste de
  `src/board/`.
- **Aucune modification du moteur Python** dans cette livraison.
- **Aucun effet visuel** dans cette livraison : pas de bandeau, pas d'éclair,
  pas de trait, pas de secousse. Ils viennent en livraison 2.
- Rouge de référence pour plus tard, à ne pas utiliser ici : `#F0131E`.
- Lancer les tests depuis `ui-app/` : `npx vitest run <chemin>`.

---

### Task 1 : le modèle d'une étape et la lecture des faits du moteur

**Files:**
- Create: `ui-app/src/board/deroule-phase.ts`
- Test: `ui-app/src/board/deroule-phase.test.ts`

**Interfaces:**
- Consumes: `FaitMechant` de `./world`, `EntreeHistorique` de `./HistoriquePartie`.
- Produces:
  - `type TempsPhase = 'menace' | 'activations' | 'distribution' | 'revelation' | 'premier-joueur'`
  - `type BoostDeroule = { cle: string; nom: string; cibleId: number; apport: number }`
  - `type EtapeDeroule = { cle: string; temps: TempsPhase; titre: string; regle: string; carteId?: number; cibleId?: number; boosts: BoostDeroule[]; consequences: { cle: string; texte: string }[]; brut?: string }`
  - `function etapesDeroule(faits: FaitMechant[], entrees: EntreeHistorique[]): EtapeDeroule[]`

- [ ] **Step 1: Write the failing test**

Créer `ui-app/src/board/deroule-phase.test.ts` :

```ts
// Le decoupage de la phase du mechant en ETAPES a valider une par une.
//
// La source n'est pas une relecture du monde : le moteur envoie deja ses
// activations resolues (`FaitMechant`), avec la composition du coup — base,
// boost, defense — qu'aucune deduction ne saurait reconstituer. Le journal
// complete pour ce que les faits ne couvrent pas.
import { describe, expect, it } from 'vitest'
import { etapesDeroule } from './deroule-phase'
import type { FaitMechant } from './world'
import type { EntreeHistorique } from './HistoriquePartie'

const attaque = (extra: Partial<FaitMechant> = {}): FaitMechant => ({
  genre: 'attaque',
  phase: 'Enemy Activation',
  auteur: 'Ultron',
  auteur_id: 50,
  cible: 'Shuri',
  cible_id: 12,
  base: 3,
  boost: 2,
  defense: 0,
  inflige: 5,
  subi: 5,
  restant: 7,
  boosts: [],
  ...extra,
})

const entree = (extra: Partial<EntreeHistorique> = {}): EntreeHistorique =>
  ({
    cle: 'k1',
    type: 'threat',
    renderId: 1,
    round: 1,
    phase: 'Main Scheme Place Threat',
    titre: 'Menace posee',
    valeur: 1,
    ...extra,
  }) as EntreeHistorique

describe('etapesDeroule', () => {
  it('fait une etape par activation du moteur', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur: 'Drone', auteur_id: 60 })], [])
    const activations = etapes.filter((e) => e.temps === 'activations')
    expect(activations).toHaveLength(2)
  })

  it('met la carte qui agit en avant et retient sa cible', () => {
    const [etape] = etapesDeroule([attaque()], []).filter((e) => e.temps === 'activations')
    expect(etape.carteId).toBe(50)
    expect(etape.cibleId).toBe(12)
  })

  it('porte les boosts de l activation, dans l ordre', () => {
    const etapes = etapesDeroule(
      [attaque({ boosts: [{ nom: 'Boost A', id: 91, apport: 1 }, { nom: 'Boost B', id: 92, apport: 1 }] })],
      []
    )
    const [etape] = etapes.filter((e) => e.temps === 'activations')
    expect(etape.boosts.map((b) => b.nom)).toEqual(['Boost A', 'Boost B'])
    expect(etape.boosts.map((b) => b.cle)).toEqual(['boost:0:91', 'boost:1:92'])
  })

  it('range une activation declenchee par une carte revelee sous la revelation', () => {
    // Un vilain peut frapper une seconde fois hors de l'etape des activations :
    // le fait porte sa propre phase, on la suit plutot que de tout ranger sous
    // « activations ».
    const etapes = etapesDeroule([attaque({ phase: 'Reveal Encounter Cards' })], [])
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(1)
    expect(etapes.filter((e) => e.temps === 'activations')).toHaveLength(0)
  })

  it('fait une etape de menace a partir du journal', () => {
    const etapes = etapesDeroule([], [entree()])
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  it('donne une cle stable et unique a chaque etape', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur_id: 60 })], [entree()])
    const cles = etapes.map((e) => e.cle)
    expect(new Set(cles).size).toBe(cles.length)
  })

  it('rend les etapes dans l ordre des quatre temps', () => {
    const etapes = etapesDeroule(
      [attaque(), attaque({ phase: 'Reveal Encounter Cards', auteur_id: 60 })],
      [entree()]
    )
    expect(etapes.map((e) => e.temps)).toEqual(['menace', 'activations', 'revelation'])
  })

  it('ne rend aucune etape quand la phase n a rien produit', () => {
    expect(etapesDeroule([], [])).toEqual([])
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/deroule-phase.test.ts`
Expected: FAIL — `Failed to resolve import "./deroule-phase"`.

- [ ] **Step 3: Write minimal implementation**

Créer `ui-app/src/board/deroule-phase.ts` :

```ts
// La phase du mechant, decoupee en ETAPES a valider une par une.
//
// Deux sources, et aucune n'est une relecture du monde :
//
// 1. `FaitMechant` — les activations que le moteur a deja resolues. Lui seul
//    connait la composition d'un coup (base, boost, defense) ; une deduction
//    verrait le resultat sans jamais pouvoir dire « 5 = 3 + 2 », et compterait
//    plusieurs fois ce que le moteur rend plusieurs fois autour d'une seule
//    resolution.
// 2. Les entrees du journal, pour ce que les faits ne couvrent pas : la menace
//    posee, les cartes revelees.
//
// Ce module est PUR : aucun DOM, aucune traduction. Il rend des cles de texte
// que le composant met en langue. C'est ce qui le rend testable sans navigateur
// et verifiable dans les deux langues.

import type { EntreeHistorique } from './HistoriquePartie'
import type { FaitMechant } from './world'

export type TempsPhase =
  | 'menace'
  | 'activations'
  | 'distribution'
  | 'revelation'
  | 'premier-joueur'

/** Ordre des quatre temps de la carte de reference. */
const ORDRE: TempsPhase[] = [
  'menace',
  'activations',
  'distribution',
  'revelation',
  'premier-joueur',
]

/** Phase du moteur -> temps de la carte de reference. */
const TEMPS_PAR_PHASE: Record<string, TempsPhase> = {
  'Main Scheme Place Threat': 'menace',
  'Enemy Activation': 'activations',
  'Deal Encounter Cards': 'distribution',
  'Reveal Encounter Cards': 'revelation',
}

export type BoostDeroule = {
  cle: string
  nom: string
  cibleId: number
  apport: number
}

export type EtapeDeroule = {
  /** Identifiant stable, pour la cle React et le « Precedent ». */
  cle: string
  temps: TempsPhase
  /** Deja mis en phrase par le composant : ici, le texte brut de l'action. */
  titre: string
  /** Rappel de la regle appliquee. */
  regle: string
  /** Carte a mettre en avant sur le plateau. */
  carteId?: number
  /** Cible de l'action, pour le trait de la livraison 2. */
  cibleId?: number
  boosts: BoostDeroule[]
  consequences: { cle: string; texte: string }[]
  /** Texte du moteur quand on ne sait pas mettre le fait en phrase. */
  brut?: string
}

function tempsDe(phase: string | undefined): TempsPhase | undefined {
  return phase ? TEMPS_PAR_PHASE[phase] : undefined
}

/**
 * Les etapes de la phase, dans l'ordre de la carte de reference.
 *
 * Un fait porte SA phase : un vilain qu'une carte revelee fait frapper une
 * seconde fois se range sous la revelation, pas sous les activations, sans quoi
 * il paraissait attaquer deux fois sans raison.
 */
export function etapesDeroule(
  faits: FaitMechant[],
  entrees: EntreeHistorique[]
): EtapeDeroule[] {
  const etapes: EtapeDeroule[] = []

  const menace = entrees.filter(
    (e) => tempsDe(e.phase) === 'menace' && e.type === 'threat'
  )
  if (menace.length > 0) {
    etapes.push({
      cle: 'menace',
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      boosts: [],
      consequences: menace.map((e) => ({ cle: e.cle, texte: e.titre })),
    })
  }

  faits.forEach((fait, index) => {
    const temps = tempsDe(fait.phase) ?? 'activations'
    etapes.push({
      cle: `fait:${index}:${fait.auteur_id}`,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'activations' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      boosts: fait.boosts.map((boost, rang) => ({
        cle: `boost:${rang}:${boost.id}`,
        nom: boost.nom,
        cibleId: boost.id,
        apport: boost.apport,
      })),
      consequences: [],
    })
  })

  return etapes.sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/deroule-phase.test.ts`
Expected: PASS, 8 tests.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/deroule-phase.ts ui-app/src/board/deroule-phase.test.ts
git commit -m "feat(deroule): decouper la phase du mechant en etapes

Les activations viennent des faits du moteur, qui seul connait la
composition d'un coup ; le journal fournit la menace posee. Module pur,
sans DOM ni traduction : le composant met en langue."
```

---

### Task 2 : les cartes rencontre révélées, et le repli sur le texte brut

**Files:**
- Modify: `ui-app/src/board/deroule-phase.ts`
- Modify: `ui-app/src/board/deroule-phase.test.ts`

**Interfaces:**
- Consumes: `etapesDeroule` de la tâche 1.
- Produces: aucune signature nouvelle ; `EtapeDeroule.brut` est désormais renseigné.

- [ ] **Step 1: Write the failing test**

Ajouter à `deroule-phase.test.ts`, dans le `describe` existant :

```ts
  it('fait une etape par carte revelee', () => {
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c1',
        type: 'card',
        phase: 'Reveal Encounter Cards',
        titre: 'Icy Grip revelee',
        cibleId: 77,
      }),
    ])
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations).toHaveLength(1)
    expect(revelations[0].carteId).toBe(77)
  })

  it('garde le texte brut du moteur quand le fait n a pas de phrase', () => {
    // Une carte fan-made a l'effet inattendu : mieux vaut un texte technique
    // qu'un silence. On voit au moins qu'il s'est passe quelque chose.
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c2',
        type: 'text',
        phase: 'Reveal Encounter Cards',
        titre: '',
        brut: '[(50,01113) Klaw] would deal 2 damage',
      }),
    ])
    expect(etapes.some((e) => e.brut === '[(50,01113) Klaw] would deal 2 damage')).toBe(true)
  })

  it('ne fait pas d etape d une narration deja mise en phrase ailleurs', () => {
    // Le type `text` sans `brut` est la narration interne du moteur : elle a sa
    // place dans le journal, pas dans un deroule qu'on lit etape par etape.
    const etapes = etapesDeroule([], [
      entree({ cle: 'c3', type: 'text', phase: 'Reveal Encounter Cards', titre: 'Main scheme phase start' }),
    ])
    expect(etapes).toEqual([])
  })
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/deroule-phase.test.ts`
Expected: FAIL — les trois nouveaux cas échouent, aucune étape de révélation n'est produite.

- [ ] **Step 3: Write minimal implementation**

Dans `deroule-phase.ts`, insérer avant le `return etapes.sort(...)` :

```ts
  // Les cartes revelees, que les faits du moteur ne couvrent pas : lui ne rend
  // que les activations resolues.
  for (const e of entrees) {
    if (tempsDe(e.phase) !== 'revelation') continue
    if (e.type === 'card') {
      etapes.push({
        cle: `carte:${e.cle}`,
        temps: 'revelation',
        titre: e.titre,
        regle: 'regle:revelation',
        carteId: e.cibleId,
        boosts: [],
        consequences: [],
      })
      continue
    }
    // Narration que personne n'a su mettre en phrase : on la montre telle
    // quelle plutot que de la taire. Sans `brut`, c'est la narration interne
    // du moteur, qui reste au journal.
    if (e.type === 'text' && e.brut) {
      etapes.push({
        cle: `brut:${e.cle}`,
        temps: 'revelation',
        titre: e.titre,
        regle: 'regle:revelation',
        boosts: [],
        consequences: [],
        brut: e.brut,
      })
    }
  }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/deroule-phase.test.ts`
Expected: PASS, 11 tests.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/deroule-phase.ts ui-app/src/board/deroule-phase.test.ts
git commit -m "feat(deroule): une etape par carte revelee, et le repli sur le brut

Un fait qu'on ne sait pas mettre en phrase se montre quand meme, texte du
moteur a l'appui : mieux vaut technique que muet. La narration interne
sans identifiants, elle, reste au journal."
```

---

### Task 3 : les phrases, en français et en anglais

**Files:**
- Create: `ui-app/src/board/deroule-textes.ts`
- Create: `ui-app/src/board/deroule-textes.test.ts`
- Modify: `ui-app/src/board/dico-en.ts`

**Interfaces:**
- Consumes: `EtapeDeroule` de la tâche 1, `t()` de `./langue`.
- Produces:
  - `function titreEtape(etape: EtapeDeroule, noms: (id: number) => string): string`
  - `function regleEtape(etape: EtapeDeroule): string`

- [ ] **Step 1: Write the failing test**

Créer `ui-app/src/board/deroule-textes.test.ts` :

```ts
// Les phrases du deroule : ecrites par nous, pas la narration du moteur.
//
// « Ultron frappe Shuri » se lit ; « [(50,01113) Klaw] would deal 2 damage »
// se dechiffre. Et tout passe par le dictionnaire : le plateau est bilingue,
// rattraper les traductions apres coup coute plus cher que de les poser tout
// de suite.
import { describe, expect, it } from 'vitest'
import { regleEtape, titreEtape } from './deroule-textes'
import type { EtapeDeroule } from './deroule-phase'

const noms = (id: number) => ({ 50: 'Ultron', 12: 'Shuri' })[id] ?? `Carte ${id}`

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  carteId: 50,
  cibleId: 12,
  boosts: [],
  consequences: [],
  ...extra,
})

describe('phrases du deroule', () => {
  it('nomme l attaquant et sa cible', () => {
    expect(titreEtape(etape(), noms)).toBe('Ultron attaque Shuri')
  })

  it('dit la manigance autrement que l attaque', () => {
    expect(titreEtape(etape({ titre: 'manigance' }), noms)).toBe('Ultron complote contre Shuri')
  })

  it('annonce la menace sans nommer de cible', () => {
    expect(titreEtape(etape({ temps: 'menace', titre: 'menace', carteId: undefined, cibleId: undefined }), noms))
      .toBe('Menace sur la manigance principale')
  })

  it('rappelle la regle du point 1', () => {
    expect(regleEtape(etape({ regle: 'regle:menace' })))
      .toBe('Point 1 : chaque joueur ajoute 1 menace à la manigance principale.')
  })

  it('rappelle la regle des activations', () => {
    expect(regleEtape(etape())).toBe('Point 2 : chaque ennemi s’active contre le héros engagé avec lui.')
  })

  it('laisse passer un titre deja redige', () => {
    // Une carte revelee arrive avec son titre venu du journal : on ne le
    // reecrit pas.
    expect(titreEtape(etape({ temps: 'revelation', titre: 'Icy Grip révélée' }), noms))
      .toBe('Icy Grip révélée')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/deroule-textes.test.ts`
Expected: FAIL — `Failed to resolve import "./deroule-textes"`.

- [ ] **Step 3: Write minimal implementation**

Créer `ui-app/src/board/deroule-textes.ts` :

```ts
// Mise en phrase des etapes du deroule.
//
// Separe du decoupage (deroule-phase.ts) a dessein : le decoupage est une
// question de regles du jeu, la mise en phrase une question de langue. Les
// deux se testent separement, et le decoupage reste verifiable sans toucher
// au dictionnaire.

import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'

/** Cles de titre que ce module sait rediger. Tout autre titre passe tel quel. */
const REDIGES = new Set(['attaque', 'manigance', 'menace'])

export function titreEtape(etape: EtapeDeroule, noms: (id: number) => string): string {
  if (!REDIGES.has(etape.titre)) return etape.titre

  if (etape.titre === 'menace') return t('Menace sur la manigance principale')

  const auteur = etape.carteId !== undefined ? noms(etape.carteId) : ''
  const cible = etape.cibleId !== undefined ? noms(etape.cibleId) : ''
  return etape.titre === 'attaque'
    ? `${auteur} ${t('attaque')} ${cible}`
    : `${auteur} ${t('complote contre')} ${cible}`
}

const REGLES: Record<string, string> = {
  'regle:menace': 'Point 1 : chaque joueur ajoute 1 menace à la manigance principale.',
  'regle:activations': 'Point 2 : chaque ennemi s’active contre le héros engagé avec lui.',
  'regle:revelation': 'Point 4 : chaque joueur révèle sa carte rencontre et en applique l’effet.',
}

export function regleEtape(etape: EtapeDeroule): string {
  const regle = REGLES[etape.regle]
  return regle ? t(regle) : ''
}
```

- [ ] **Step 4: Add the English entries**

Dans `ui-app/src/board/dico-en.ts`, ajouter à la suite des entrées du panneau
Historique :

```ts
  // Deroule detaille de la phase du mechant.
  'Menace sur la manigance principale': 'Threat on the main scheme',
  'attaque': 'attacks',
  'complote contre': 'schemes against',
  'Point 1 : chaque joueur ajoute 1 menace à la manigance principale.':
    'Step 1: each player adds 1 threat to the main scheme.',
  'Point 2 : chaque ennemi s’active contre le héros engagé avec lui.':
    'Step 2: each enemy activates against the hero engaged with it.',
  'Point 4 : chaque joueur révèle sa carte rencontre et en applique l’effet.':
    'Step 4: each player reveals their encounter card and resolves it.',
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/deroule-textes.test.ts && npx tsc --noEmit`
Expected: PASS, 6 tests, et le typage sans erreur.

- [ ] **Step 6: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/deroule-textes.ts ui-app/src/board/deroule-textes.test.ts ui-app/src/board/dico-en.ts
git commit -m "feat(deroule): les phrases des etapes, en francais et en anglais

Le decoupage est une question de regles, la mise en phrase une question de
langue : deux modules, deux jeux de tests. Les traductions sont posees des
maintenant, les rattraper apres coute plus cher."
```

---

### Task 4 : le cartouche et la navigation

**Files:**
- Create: `ui-app/src/board/DeroulePhase.tsx`
- Create: `ui-app/src/board/DeroulePhase.test.tsx`
- Modify: `ui-app/src/board/board.css`

**Interfaces:**
- Consumes: `EtapeDeroule`, `titreEtape`, `regleEtape`.
- Produces: `function DeroulePhase(props: { etapes: EtapeDeroule[]; noms: (id: number) => string; onTerminer: () => void }): JSX.Element | null`

- [ ] **Step 1: Write the failing test**

Créer `ui-app/src/board/DeroulePhase.test.tsx` :

```tsx
// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais : l'oeil sait ou lire et la
// main ou cliquer des le deuxieme tour. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie — c'est une relecture, pas un undo.
import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'

const noms = (id: number) => ({ 50: 'Ultron', 12: 'Shuri' })[id] ?? `Carte ${id}`

const etapes: EtapeDeroule[] = [
  { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
  {
    cle: 'b',
    temps: 'activations',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId: 12,
    boosts: [],
    consequences: [],
  },
]

const suivant = () => screen.getByRole('button', { name: /Suivant/i })

describe('cartouche du deroule', () => {
  it('montre la premiere etape et rien d autre', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
  })

  it('avance d une etape au clic sur Suivant', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    suivant().click()
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('rappelle la regle de l etape courante', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.getByText(/Point 1/)).toBeInTheDocument()
  })

  it('revient en arriere sans rien rejouer', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    suivant().click()
    screen.getByRole('button', { name: /Précédent/i }).click()
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('n offre pas de Precedent sur la premiere etape', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.queryByRole('button', { name: /Précédent/i })).toBeNull()
  })

  it('previent quand la derniere etape est validee', () => {
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={onTerminer} />)
    suivant().click()
    suivant().click()
    expect(onTerminer).toHaveBeenCalledTimes(1)
  })

  it('ne rend rien sans etape', () => {
    const { container } = render(<DeroulePhase etapes={[]} noms={noms} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('montre les quatre temps, celui en cours mis en avant', () => {
    const { container } = render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(4)
    expect(container.querySelector('.deroule-temps li.est-courant')?.textContent).toMatch(/Menace/i)
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/DeroulePhase.test.tsx`
Expected: FAIL — `Failed to resolve import "./DeroulePhase"`.

- [ ] **Step 3: Write minimal implementation**

Créer `ui-app/src/board/DeroulePhase.tsx` :

```tsx
// Le cartouche du deroule detaille : une etape a la fois.
//
// FIXE en bas au centre, il ne bouge jamais d'une etape a l'autre : l'oeil sait
// ou lire et la main ou cliquer des le deuxieme tour. Un cartouche colle a la
// carte concernee aurait deplace le bouton a chaque clic.
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.

import { useEffect, useState } from 'react'
import type { EtapeDeroule, TempsPhase } from './deroule-phase'
import { regleEtape, titreEtape } from './deroule-textes'
import { t } from './langue'

/** Les quatre temps de la carte de reference, dans l'ordre. */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'activations', libelle: 'Activations' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  noms,
  onTerminer,
}: {
  etapes: EtapeDeroule[]
  noms: (id: number) => string
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
}) {
  const [index, setIndex] = useState(0)

  // Une nouvelle phase repart de sa premiere etape.
  useEffect(() => {
    setIndex(0)
  }, [etapes])

  const etape = etapes[index]
  if (!etape) return null

  const avancer = () => {
    if (index + 1 >= etapes.length) {
      onTerminer()
      return
    }
    setIndex(index + 1)
  }

  return (
    <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
      <ol className="deroule-temps">
        {TEMPS.map((temps) => (
          <li key={temps.cle} className={temps.cle === etape.temps ? 'est-courant' : ''}>
            {t(temps.libelle)}
          </li>
        ))}
      </ol>

      <p className="deroule-titre">{titreEtape(etape, noms)}</p>
      <p className="deroule-regle">{regleEtape(etape)}</p>
      {etape.brut ? <p className="deroule-brut">{etape.brut}</p> : null}

      <div className="deroule-boutons">
        {index > 0 ? (
          <button type="button" className="bh-bouton" onClick={() => setIndex(index - 1)}>
            {t('Précédent')}
          </button>
        ) : null}
        <button type="button" className="bh-bouton deroule-suivant" onClick={avancer}>
          {t('Suivant')}
        </button>
      </div>
    </section>
  )
}
```

- [ ] **Step 4: Add the English entries and the styles**

Dans `ui-app/src/board/dico-en.ts`, à la suite des entrées de la tâche 3 :

```ts
  'Phase du méchant': 'Villain phase',
  'Menace': 'Threat',
  'Activations': 'Activations',
  'Distribution': 'Dealing',
  'Révélation': 'Reveal',
  'Précédent': 'Previous',
  'Suivant': 'Next',
```

Dans `ui-app/src/board/board.css`, à la suite du bloc `.salon-panneau` :

```css
  /* --- Deroule detaille de la phase du mechant -------------------------------
     Cartouche FIXE en bas au centre : il ne bouge jamais d'une etape a l'autre.
     La mise en scene (bandeau, trait, secousses) viendra en livraison 2 ; ici,
     rien ne bouge. */
  .deroule-phase {
    position: fixed;
    left: 50%;
    bottom: 16px;
    transform: translateX(-50%);
    z-index: 540;
    width: min(560px, calc(100vw - 24px));
    padding: 12px 14px;
    color: #f8fafc;
    background: rgba(8, 10, 14, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    box-shadow: 0 24px 58px rgba(0, 0, 0, 0.64);
  }

  .deroule-temps {
    display: flex;
    gap: 10px;
    margin: 0 0 8px;
    padding: 0;
    list-style: none;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: rgba(248, 250, 252, 0.5);
  }

  .deroule-temps li.est-courant {
    color: #f8fafc;
    font-weight: 900;
  }

  .deroule-titre {
    margin: 0 0 4px;
    font-size: 1rem;
    font-weight: 700;
  }

  .deroule-regle {
    margin: 0 0 10px;
    font-size: 0.8rem;
    color: rgba(248, 250, 252, 0.62);
  }

  .deroule-brut {
    margin: 0 0 10px;
    font-family: ui-monospace, monospace;
    font-size: 0.72rem;
    color: rgba(248, 250, 252, 0.5);
    overflow-wrap: anywhere;
  }

  .deroule-boutons {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
  }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/DeroulePhase.test.tsx && npx tsc --noEmit`
Expected: PASS, 8 tests, typage propre.

- [ ] **Step 6: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/DeroulePhase.tsx ui-app/src/board/DeroulePhase.test.tsx ui-app/src/board/dico-en.ts ui-app/src/board/board.css
git commit -m "feat(deroule): le cartouche fixe, une etape a la fois

Fixe en bas au centre : l'oeil sait ou lire et la main ou cliquer des le
deuxieme tour. « Precedent » relit sans rien rejouer — c'est « Annuler »
qui fait reculer la partie, et il reste disponible."
```

---

### Task 5 : les raccourcis clavier

**Files:**
- Modify: `ui-app/src/board/DeroulePhase.tsx`
- Modify: `ui-app/src/board/DeroulePhase.test.tsx`

**Interfaces:**
- Consumes: le composant de la tâche 4.
- Produces: la prop optionnelle `onToutDerouler?: () => void` sur `DeroulePhase`.

- [ ] **Step 1: Write the failing test**

Ajouter à `DeroulePhase.test.tsx` :

```tsx
  it('avance a la touche Entree', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }))
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('avance aussi a la barre d espace', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    document.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('deroule tout a la touche Echap', () => {
    const onToutDerouler = vi.fn()
    render(
      <DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} onToutDerouler={onToutDerouler} />
    )
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    expect(onToutDerouler).toHaveBeenCalledTimes(1)
  })

  it('laisse le clavier tranquille quand on ecrit ailleurs', () => {
    // Le tchat est a portee de main pendant la phase : taper un espace dans son
    // champ ne doit pas faire avancer la phase du mechant.
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    const champ = document.createElement('input')
    document.body.append(champ)
    champ.focus()
    champ.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    champ.remove()
  })
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/DeroulePhase.test.tsx`
Expected: FAIL — les quatre nouveaux cas échouent, aucun écouteur clavier n'existe.

- [ ] **Step 3: Write minimal implementation**

Dans `DeroulePhase.tsx`, ajouter la prop et l'effet. Signature :

```tsx
export function DeroulePhase({
  etapes,
  noms,
  onTerminer,
  onToutDerouler,
}: {
  etapes: EtapeDeroule[]
  noms: (id: number) => string
  onTerminer: () => void
  /** « Tout derouler » : les etapes restantes defilent sans attendre. */
  onToutDerouler?: () => void
}) {
```

Puis, après la déclaration de `avancer` :

```tsx
  useEffect(() => {
    const auClavier = (evenement: KeyboardEvent) => {
      // On ecrit peut-etre ailleurs — le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
      }
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        avancer()
        return
      }
      if (evenement.key === 'Escape' && onToutDerouler) {
        evenement.preventDefault()
        onToutDerouler()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })
```

Note pour l'implémenteur : cet effet est volontairement SANS tableau de
dépendances. `avancer` se referme sur `index`, et une liste figée validerait
toujours la première étape. Le coût est un ré-abonnement par rendu, négligeable
pour un seul écouteur.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/DeroulePhase.test.tsx && npx tsc --noEmit`
Expected: PASS, 12 tests.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/DeroulePhase.tsx ui-app/src/board/DeroulePhase.test.tsx
git commit -m "feat(deroule): Entree, Espace et Echap pour derouler la phase

Un cas verrouille ce qui se casse le plus facilement : taper un espace dans
le champ du tchat ne fait pas avancer la phase du mechant."
```

---

### Task 6 : le mode « Détaillé », et le branchement sur la partie

**Files:**
- Modify: `ui-app/src/board/moteur.ts:47` (le type `ModePhaseMechant` et `MODES`)
- Modify: `ui-app/src/board.tsx` (montage du composant, à côté de `RecapPhaseMechant`, vers la ligne 2181)
- Create: `ui-app/src/board/mode-detaille.test.ts`

**Interfaces:**
- Consumes: `DeroulePhase`, `etapesDeroule`.
- Produces: `'detaille'` ajouté à `ModePhaseMechant`, et placé en tête de `MODES`.

- [ ] **Step 1: Write the failing test**

Créer `ui-app/src/board/mode-detaille.test.ts` :

```ts
// Le mode « Detaille » existe, et c'est celui qu'on a en arrivant.
//
// Il remplace « manuel » comme defaut : la phase du mechant se deroule
// desormais etape par etape a moins qu'on ne demande explicitement d'aller
// plus vite. Les trois anciens modes restent disponibles.
import { describe, expect, it } from 'vitest'
import { lireModePhaseMechant, MODES } from './moteur'

describe('mode detaille', () => {
  it('figure dans la liste des modes', () => {
    expect(MODES).toContain('detaille')
  })

  it('est le mode par defaut, sans rien de memorise', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  it('respecte encore l ancienne case a cocher de ceux qui l avaient reglee', () => {
    // Migration : son ABSENCE ne dit rien et ne doit pas priver un nouveau venu
    // du mode detaille ; sa presence, elle, est un choix a honorer.
    window.localStorage.clear()
    window.localStorage.setItem('marvel-board-phase-rapide', 'off')
    expect(lireModePhaseMechant()).toBe('manuel')
  })

  it('laisse les trois anciens modes disponibles', () => {
    expect(MODES).toEqual(expect.arrayContaining(['manuel', 'pas-a-pas', 'instantane']))
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/mode-detaille.test.ts`
Expected: FAIL — `MODES` n'est pas exporté, ou ne contient pas `'detaille'`.

- [ ] **Step 3: Write minimal implementation**

Dans `ui-app/src/board/moteur.ts`, ligne 47 environ :

```ts
export type ModePhaseMechant = 'detaille' | 'manuel' | 'pas-a-pas' | 'instantane'
```

et, ligne 56 environ, exporter la liste en plaçant le nouveau mode en tête :

```ts
// « detaille » d'abord : c'est le mode par defaut, celui qu'on a en arrivant.
export const MODES: ModePhaseMechant[] = ['detaille', 'manuel', 'pas-a-pas', 'instantane']
```

Puis corriger `lireModePhaseMechant()` (ligne 66). Elle retombe aujourd'hui sur
`'pas-a-pas'` : la ligne 70 migre l'ANCIENNE case a cocher, et son `else` sert
aussi de defaut a qui n'a jamais rien regle. Il faut distinguer les deux cas —
un reglage a migrer, et pas de reglage du tout :

```ts
export function lireModePhaseMechant(): ModePhaseMechant {
  try {
    const brut = window.localStorage.getItem(CLE_MODE_PHASE)
    if (brut && (MODES as string[]).includes(brut)) return brut as ModePhaseMechant
    // MIGRATION de l'ancienne case a cocher, qui ne connaissait que deux etats.
    // Elle ne vaut que pour qui l'avait reglee : son absence ne dit rien, et ne
    // doit pas priver un nouveau venu du mode detaille.
    const ancienne = window.localStorage.getItem(CLE_PHASE_RAPIDE)
    if (ancienne === 'off') return 'manuel'
    if (ancienne !== null) return 'pas-a-pas'
    return 'detaille'
  } catch {
    return 'detaille'
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/mode-detaille.test.ts`
Expected: PASS, 3 tests.

- [ ] **Step 5: Brancher le composant**

Dans `ui-app/src/board.tsx`, juste avant `<RecapPhaseMechant ... />` (vers la
ligne 2181) :

```tsx
      {/* Deroule detaille : une etape a la fois, validee avant la suivante.
          Le recap ci-dessous garde son role de bilan de fin, pour les modes
          rapides ou l'on n'a rien vu passer. */}
      {modePhase === 'detaille' ? (
        <DeroulePhase
          etapes={etapesDeroule(etat.monde?.faits_mechant ?? [], historique.entrees)}
          noms={(id) => cartesMondeParId.get(id)?.name ?? `#${id}`}
          onTerminer={() => undefined}
        />
      ) : null}
```

et les imports en tête de fichier :

```tsx
import { DeroulePhase } from './board/DeroulePhase'
import { etapesDeroule } from './board/deroule-phase'
```

Les deux noms sont verifies : `World.faits_mechant?: FaitMechant[]`
(`world.ts:137`, OPTIONNEL, d'ou le `?? []`) et `cartesMondeParId`
(`board.tsx:1597`), une `Map` dont les valeurs portent `.name`. `RecapPhaseMechant`
consomme deja les deux, juste en dessous.

- [ ] **Step 6: Run the whole suite**

Run: `cd ui-app && npx tsc --noEmit && npx vitest run`
Expected: tous les tests passent, aucune régression.

- [ ] **Step 7: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/moteur.ts ui-app/src/board.tsx ui-app/src/board/mode-detaille.test.ts
git commit -m "feat(deroule): le mode « Detaille » devient le defaut

Il remplace « manuel » a cette place ; pas-a-pas et instantane restent la
pour qui veut accelerer. Le recap garde son role de bilan de fin, utile
justement dans ces modes rapides."
```

---

### Task 7 : contrôle en partie réelle

**Files:** aucun. Cette tâche vérifie, elle ne code pas.

- [ ] **Step 1: Construire et déployer en local**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
```

- [ ] **Step 2: Lancer le jeu local**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 launcher_fast.py --no-browser
```

Compter environ une minute : le launcher compile les sources avant de répondre.
Attendre avec une boucle plutôt qu'un sleep :

```bash
until curl -s -o /dev/null -m 3 http://127.0.0.1:2345/; do sleep 5; done; echo pret
```

- [ ] **Step 3: Jouer une partie jusqu'à la phase du méchant**

Ouvrir `http://127.0.0.1:2345/prepare.html`, lancer une partie solo aléatoire,
puis passer son tour jusqu'à la phase du méchant.

Vérifier, une par une :

1. Le cartouche apparaît en bas au centre, et n'a pas bougé d'une étape à l'autre.
2. Le fil montre les quatre temps, celui en cours mis en avant.
3. Chaque activation est une étape distincte, avec sa phrase en français.
4. « Suivant », Entrée et Espace avancent tous les trois.
5. « Précédent » revient sans que le plateau ne recule.
6. La règle rappelée correspond au temps affiché.
7. Le plateau reste consultable : survoler une carte l'agrandit toujours.

- [ ] **Step 4: Vérifier l'anglais**

Basculer la langue avec le bouton FR de la barre du haut, refaire une phase,
vérifier que le cartouche est entièrement en anglais — titres, règles, boutons
et fil.

- [ ] **Step 5: Arrêter le jeu local**

```bash
pkill -f launcher_fast
```

- [ ] **Step 6: Commit du rapport**

Consigner ce qui a été observé dans `.planning/todos/`, en notant tout écart
avec la spec pour la livraison 2.

---

## Ce que cette livraison ne fait PAS

Volontairement absents, ils feront la livraison 2 :

- Le bandeau rouge, l'éclair, le trait fléché, les secousses, les sons.
- La mise en avant de la carte sur le plateau (agrandissement + voile).
- Le retournement des boosts un par un.
- Le « Tout dérouler » (la prop existe, personne ne la branche encore).
- Les étapes de distribution et de premier joueur.
- Le raccourcissement du récapitulatif de fin.
- Les cas particuliers : étourdi, étape vide, héros vaincu, défaite en phase.
- Le menu Options à quatre choix expliqués.
- Le mobile.
