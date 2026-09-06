# Déroulé de la phase du méchant, livraison 2 : la mise en scène

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Donner à la phase du méchant sa mise en scène : annonce, mise en avant de la carte qui agit, trait fléché vers sa cible, boosts retournés un par un.

**Architecture:** Le squelette existe et fonctionne (livraison 1). Tout ce qui suit est de la décoration posée sur le DOM en impératif, sur le modèle de `halo-statut.ts` et `pas-a-pas.ts` : classes CSS ajoutées puis retirées sur les éléments réels, jamais un re-rendu du plateau pour un effet transitoire. Aucune logique de jeu n'est touchée.

**Tech Stack:** React 19, TypeScript strict, Vitest, Testing Library, CSS dans `board.css`.

**Spec:** `docs/superpowers/specs/2026-09-06-phase-mechant-deroule-detaille-design.md`

## Global Constraints

- **TypeScript strict, zéro `any`** sans justification écrite sur place.
- **Bilingue** : tout texte affiché passe par `t()` de `src/board/langue.ts`, avec son entrée dans `src/board/dico-en.ts`.
- **Aucun caractère em dash (—)** dans le code ni les commentaires.
- **Commentaires en français**, expliquant le POURQUOI.
- **Règles des hooks** : `DeroulePhase.tsx` a un `return null` conditionnel (ligne 150). Tous les hooks avant lui, sans exception. Ce composant a déjà fait tomber le plateau sur ce point.
- **Ne jamais modifier un composant pour faire passer un test.** Si un test échoue sur du timing React, corriger le TEST (`fireEvent`, `act`, `advanceTimersByTimeAsync`). Un `flushSync` a déjà dû être défait.
- **Tout effet est débrayable** : rien ne doit bouger sous `body.plateau-sans-animations` ni sous `@media (prefers-reduced-motion: reduce)`. Les étapes, textes et validations restent identiques dans ce cas.
- **Rouge de référence : `#F0131E`.**
- Aucune modification du moteur Python.
- Ne commiter que les fichiers de la tâche, listés explicitement. Jamais `git add -A`.
- Tests depuis `ui-app/` : `npx vitest run`.

## Structure des fichiers

| Fichier | Responsabilité |
|---|---|
| `src/board/deroule-phase.ts` | existant, module pur. Étendu seulement si une étape doit porter une donnée nouvelle. |
| `src/board/DeroulePhase.tsx` | existant, le cartouche. Reçoit les nouvelles props d'orchestration. |
| `src/board/deroule-scene.ts` | **nouveau**, pur : décide QUELLES classes poser sur QUELLES cartes pour une étape. Testable sans DOM. |
| `src/board/useDerouleScene.ts` | **nouveau**, le hook qui applique ces décisions au DOM en impératif, comme `pas-a-pas.ts`. |
| `src/board/BandeauPhase.tsx` | **nouveau**, l'annonce de phase. |
| `src/board/board.css` | existant : les styles et les animations. |

---

### Task 1 : les trois tests manquants de la livraison 1

Dette signalée par la revue finale. À solder avant d'empiler du neuf.

**Files:**
- Modify: `ui-app/src/board/deroule-textes.test.ts`
- Modify: `ui-app/src/board/DeroulePhase.test.tsx`
- Modify: `ui-app/src/board/deroule-phase.test.ts`

**Interfaces:**
- Consumes: `regleEtape`, `titreEtape`, `etapesDeroule`, `DeroulePhase`.
- Produces: rien de neuf.

- [ ] **Step 1: Écrire les trois tests**

Dans `deroule-textes.test.ts`, au `describe` existant. La règle de révélation
est affichée par la majorité des étapes d'une phase et n'est couverte par rien :

```ts
  it('rappelle la regle des cartes revelees', () => {
    expect(regleEtape(etape({ regle: 'regle:revelation' })))
      .toBe('Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.')
  })

  it('ne dit rien d une regle inconnue plutot que d inventer', () => {
    expect(regleEtape(etape({ regle: 'regle:inexistante' }))).toBe('')
  })
```

Dans `DeroulePhase.test.tsx`. Depuis le correctif de fermeture, c'est
`avancer()` qui fait disparaître le cartouche : le chemin clavier vers cette
disparition n'est vérifié par rien.

```tsx
  it('ferme le cartouche quand la derniere etape est validee au CLAVIER', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(document.querySelector('.deroule-phase')).toBeNull()
  })
```

Dans `deroule-phase.test.ts`, resserrer l'assertion faible repérée par la revue.
Remplacer le corps du cas `garde le texte brut du moteur quand le fait n a pas de
phrase` par une assertion sur la liste complète, un `some()` restant vert même si
le code produisait en plus une étape parasite :

```ts
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c2',
        type: 'text',
        phase: 'Reveal Encounter Cards',
        titre: '',
        brut: '[(50,01113) Klaw] would deal 2 damage',
      }),
    ], 1)
    expect(etapes).toHaveLength(1)
    expect(etapes[0]?.brut).toBe('[(50,01113) Klaw] would deal 2 damage')
```

Note : `etapesDeroule` prend un troisième paramètre depuis le correctif du
round. Vérifie sa signature exacte dans `deroule-phase.ts` avant d'écrire, et
adapte les appels si elle diffère.

- [ ] **Step 2: Lancer et vérifier l'échec**

Run: `cd ui-app && npx vitest run src/board/deroule-textes.test.ts src/board/DeroulePhase.test.tsx src/board/deroule-phase.test.ts`
Expected: les deux premiers échouent (règle non couverte, fermeture au clavier). Le troisième peut déjà passer : c'est un resserrement, pas une correction. Note lequel échoue.

- [ ] **Step 3: Corriger ce qui doit l'être**

Si un test échoue pour une vraie raison, corrige le CODE, pas le test. Si les
trois passent d'emblée, dis-le dans ton rapport : ils verrouillent alors un
comportement correct mais non couvert, ce qui reste leur intérêt.

- [ ] **Step 4: Vérifier**

Run: `cd ui-app && npx vitest run && npx tsc --noEmit`
Expected: tout vert, aucune régression.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/deroule-textes.test.ts ui-app/src/board/DeroulePhase.test.tsx ui-app/src/board/deroule-phase.test.ts
git commit -m "test(deroule): couvrir la regle de revelation, la fermeture au clavier

Dette relevee par la revue finale de la livraison 1. La regle de revelation
est affichee par la majorite des etapes d'une phase et n'etait couverte par
rien ; la fermeture du cartouche n'etait verifiee qu'au clic, alors que le
clavier passe par le meme chemin depuis le correctif. L'assertion du texte
brut passe d'un some() a la liste complete : elle restait verte si le code
produisait en plus une etape parasite."
```

---

### Task 2 : décider de la mise en scène d'une étape

Un module PUR qui dit quoi mettre en avant. Aucun DOM ici : c'est ce qui le rend testable et vérifiable.

**Files:**
- Create: `ui-app/src/board/deroule-scene.ts`
- Test: `ui-app/src/board/deroule-scene.test.ts`

**Interfaces:**
- Consumes: `EtapeDeroule` de `./deroule-phase`.
- Produces:
  - `type SceneEtape = { carteEnAvant?: number; cible?: number; trait: boolean; voile: boolean }`
  - `function sceneDe(etape: EtapeDeroule): SceneEtape`

- [ ] **Step 1: Write the failing test**

```ts
// Ce qu'une etape demande a l'ecran : quelle carte mettre en avant, faut-il
// tracer un trait vers une cible, faut-il assombrir le reste.
//
// Module PUR, sans DOM : la decision se teste ici, la pose se fait ailleurs
// (useDerouleScene.ts). C'est le meme partage que pas-a-pas.ts, ou le rythme
// vit dans moteur.ts et la decoration dans le hook.
import { describe, expect, it } from 'vitest'
import { sceneDe } from './deroule-scene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

describe('mise en scene d une etape', () => {
  it('met en avant la carte qui agit', () => {
    expect(sceneDe(etape({ carteId: 50 })).carteEnAvant).toBe(50)
  })

  it('trace un trait quand l etape a un auteur ET une cible', () => {
    const scene = sceneDe(etape({ carteId: 50, cibleId: 12 }))
    expect(scene.trait).toBe(true)
    expect(scene.cible).toBe(12)
  })

  it('ne trace aucun trait sans cible', () => {
    expect(sceneDe(etape({ carteId: 50 })).trait).toBe(false)
  })

  it('ne trace aucun trait quand l auteur est sa propre cible', () => {
    // Un trait qui part d'une carte pour y revenir ne montre rien.
    expect(sceneDe(etape({ carteId: 50, cibleId: 50 })).trait).toBe(false)
  })

  it('assombrit le plateau des qu une carte est mise en avant', () => {
    expect(sceneDe(etape({ carteId: 50 })).voile).toBe(true)
  })

  it('n assombrit rien sur une etape sans carte', () => {
    // « Aucun sbire en jeu », le passage du premier joueur : le cartouche parle
    // seul, l'ecran ne bouge pas pour rien.
    const scene = sceneDe(etape({ carteId: undefined }))
    expect(scene.voile).toBe(false)
    expect(scene.carteEnAvant).toBeUndefined()
  })

  it('ne met rien en avant pour une etape technique qui defile seule', () => {
    // Elle passe en une demi-seconde : agrandir une carte pour la reduire
    // aussitot donnerait un clignotement.
    const scene = sceneDe(etape({ carteId: 50, auto: true }))
    expect(scene.carteEnAvant).toBeUndefined()
    expect(scene.voile).toBe(false)
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/deroule-scene.test.ts`
Expected: FAIL, `Failed to resolve import "./deroule-scene"`.

- [ ] **Step 3: Write minimal implementation**

```ts
// Ce qu'une etape demande a l'ecran.
//
// PUR : aucun DOM, aucune classe CSS. Le hook useDerouleScene applique ces
// decisions ; ici on ne fait que decider. Ce partage rend la regle verifiable
// sans navigateur, et c'est celui de pas-a-pas.ts.

import type { EtapeDeroule } from './deroule-phase'

export type SceneEtape = {
  /** Carte a agrandir, si l'etape en designe une. */
  carteEnAvant?: number
  /** Cible du trait, quand il y en a un. */
  cible?: number
  /** Faut-il tracer le trait de l'auteur vers la cible. */
  trait: boolean
  /** Faut-il assombrir le reste du plateau. */
  voile: boolean
}

const RIEN: SceneEtape = { trait: false, voile: false }

export function sceneDe(etape: EtapeDeroule): SceneEtape {
  // Une etape technique defile en une demi-seconde : agrandir une carte pour
  // la reduire aussitot donnerait un clignotement, pas une mise en scene.
  if (etape.auto) return RIEN
  if (etape.carteId === undefined) return RIEN

  // Un trait qui part d'une carte pour y revenir ne montre rien.
  const trait = etape.cibleId !== undefined && etape.cibleId !== etape.carteId

  return {
    carteEnAvant: etape.carteId,
    cible: trait ? etape.cibleId : undefined,
    trait,
    voile: true,
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ui-app && npx vitest run src/board/deroule-scene.test.ts`
Expected: PASS, 7 tests.

- [ ] **Step 5: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/deroule-scene.ts ui-app/src/board/deroule-scene.test.ts
git commit -m "feat(deroule): decider de la mise en scene d'une etape

Module pur : quelle carte mettre en avant, faut-il un trait, faut-il un
voile. La pose sur le DOM viendra a part, comme pas-a-pas.ts separe le
rythme de la decoration. Une etape technique ne met rien en avant : elle
defile en une demi-seconde, agrandir une carte pour la reduire aussitot
donnerait un clignotement."
```

---

### Task 3 : poser la mise en avant et le voile sur le plateau

**Files:**
- Create: `ui-app/src/board/useDerouleScene.ts`
- Modify: `ui-app/src/board/board.css`
- Modify: `ui-app/src/board/DeroulePhase.tsx`
- Test: `ui-app/src/board/useDerouleScene.test.ts`

**Interfaces:**
- Consumes: `sceneDe`, `SceneEtape` de `./deroule-scene`.
- Produces: `function useDerouleScene(etape: EtapeDeroule | undefined, actif: boolean): void`

- [ ] **Step 1: Write the failing test**

```ts
// La pose des classes sur les vraies cartes du plateau.
//
// Imperatif, comme halo-statut.ts et pas-a-pas.ts : on ajoute des classes sur
// l'element reel, on les retire ensuite. Passer par React ferait re-rendre le
// plateau entier a chaque etape, pour une decoration transitoire.
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useDerouleScene } from './useDerouleScene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

/** Une fausse carte sur un faux plateau, comme le DOM reel les porte. */
function poserCarte(id: number): HTMLElement {
  let scene = document.querySelector('.plateau-scene')
  if (!scene) {
    scene = document.createElement('div')
    scene.className = 'plateau-scene'
    document.body.append(scene)
  }
  const carte = document.createElement('article')
  carte.className = 'scan-card'
  carte.setAttribute('data-card-id', String(id))
  scene.append(carte)
  return carte
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('pose de la mise en scene', () => {
  it('marque la carte qui agit', () => {
    const carte = poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(carte.classList.contains('deroule-en-avant')).toBe(true)
  })

  it('marque la cible a part', () => {
    const auteur = poserCarte(50)
    const cible = poserCarte(12)
    renderHook(() => useDerouleScene(etape({ carteId: 50, cibleId: 12 }), true))
    expect(auteur.classList.contains('deroule-en-avant')).toBe(true)
    expect(cible.classList.contains('deroule-cible')).toBe(true)
  })

  it('assombrit le plateau', () => {
    poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(document.body.classList.contains('deroule-voile')).toBe(true)
  })

  it('nettoie tout quand l etape change', () => {
    const carte = poserCarte(50)
    const { rerender } = renderHook(
      ({ e }: { e: EtapeDeroule | undefined }) => useDerouleScene(e, true),
      { initialProps: { e: etape({ carteId: 50 }) as EtapeDeroule | undefined } }
    )
    rerender({ e: etape({ cle: 'k2', carteId: undefined }) })
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
    expect(document.body.classList.contains('deroule-voile')).toBe(false)
  })

  it('nettoie tout au demontage', () => {
    // Sans cela, quitter la phase laisserait une carte agrandie et un plateau
    // assombri pour le reste de la partie.
    const carte = poserCarte(50)
    const { unmount } = renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    unmount()
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
    expect(document.body.classList.contains('deroule-voile')).toBe(false)
  })

  it('ne pose rien quand la mise en scene est coupee', () => {
    const carte = poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), false))
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
  })

  it('ne tombe pas sur une carte absente du plateau', () => {
    // Une carte peut avoir quitte la table entre le fait et son affichage.
    expect(() =>
      renderHook(() => useDerouleScene(etape({ carteId: 999 }), true))
    ).not.toThrow()
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/useDerouleScene.test.ts`
Expected: FAIL, `Failed to resolve import "./useDerouleScene"`.

- [ ] **Step 3: Write minimal implementation**

```ts
// Pose la mise en scene d'une etape sur les vraies cartes du plateau.
//
// IMPERATIF, comme halo-statut.ts et pas-a-pas.ts : classes ajoutees puis
// retirees sur l'element reel. Passer par React ferait re-rendre le plateau
// entier a chaque etape pour une decoration transitoire, et le plateau est
// lourd (plusieurs dizaines de cartes).
//
// Le nettoyage est fait a CHAQUE changement d'etape et au demontage : sans
// lui, quitter la phase laisserait une carte agrandie et un plateau assombri
// pour le reste de la partie.

import { useEffect } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

const EN_AVANT = 'deroule-en-avant'
const CIBLE = 'deroule-cible'
const VOILE = 'deroule-voile'

function carteDe(id: number): HTMLElement | null {
  return document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${id}"]`
  )
}

export function useDerouleScene(etape: EtapeDeroule | undefined, actif: boolean): void {
  useEffect(() => {
    if (!actif || !etape) return
    const scene = sceneDe(etape)

    const auteur = scene.carteEnAvant !== undefined ? carteDe(scene.carteEnAvant) : null
    const cible = scene.cible !== undefined ? carteDe(scene.cible) : null

    auteur?.classList.add(EN_AVANT)
    cible?.classList.add(CIBLE)
    if (scene.voile) document.body.classList.add(VOILE)

    return () => {
      auteur?.classList.remove(EN_AVANT)
      cible?.classList.remove(CIBLE)
      document.body.classList.remove(VOILE)
    }
  }, [etape, actif])
}
```

- [ ] **Step 4: Add the styles**

Dans `ui-app/src/board/board.css`, à la suite du bloc `.deroule-phase` :

```css
  /* --- Mise en scene d'une etape du deroule -------------------------------
     La carte qui agit grandit sur place, le reste du plateau s'assombrit sans
     devenir illisible : on doit continuer a voir la manigance monter ou un
     heros encaisser ailleurs. Tout ceci est debraye plus bas. */
  .deroule-voile .plateau-scene::after {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 60;
    background: rgba(4, 6, 10, 0.55);
    pointer-events: none;
  }

  .plateau-scene .scan-card.deroule-en-avant,
  .plateau-scene .scan-card.deroule-cible {
    position: relative;
    z-index: 70;
  }

  .plateau-scene .scan-card.deroule-en-avant .scan-visuel {
    transform: scale(2.36);
    transition: transform 220ms ease;
  }

  .plateau-scene .scan-card.deroule-cible .scan-frame {
    box-shadow:
      0 0 0 3px #F0131E,
      0 0 22px 6px rgba(240, 19, 30, 0.55);
  }

  body.plateau-sans-animations .plateau-scene .scan-card.deroule-en-avant .scan-visuel {
    transition: none;
  }
```

et dans le bloc `@media (prefers-reduced-motion: reduce)` existant :

```css
    .plateau-scene .scan-card.deroule-en-avant .scan-visuel {
      transition: none;
    }
```

- [ ] **Step 5: Brancher le hook**

Dans `ui-app/src/board/DeroulePhase.tsx`, appeler le hook AVANT le `return null`
conditionnel, avec les autres hooks :

```tsx
  // Mise en scene de l'etape courante. Appele ici, avec les autres hooks :
  // ce composant a un `return null` plus bas, et un hook place apres lui fait
  // tomber tout le plateau (React compte alors un hook de plus au rendu
  // suivant).
  useDerouleScene(etape, !termine)
```

Note pour l'implémenteur : `etape` est déjà calculé plus haut dans le
composant. Vérifie sa position exacte et place l'appel après lui mais avant le
`return null` de la ligne 150 environ.

- [ ] **Step 6: Run tests**

Run: `cd ui-app && npx vitest run && npx tsc --noEmit`
Expected: tout vert.

- [ ] **Step 7: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/useDerouleScene.ts ui-app/src/board/useDerouleScene.test.ts ui-app/src/board/DeroulePhase.tsx ui-app/src/board/board.css
git commit -m "feat(deroule): la carte qui agit grandit, le plateau s'assombrit

Pose imperative, comme halo-statut.ts : re-rendre le plateau entier pour une
decoration transitoire couterait trop cher. Le nettoyage a lieu a chaque
changement d'etape ET au demontage, sans quoi quitter la phase laisserait
une carte agrandie et un plateau assombri pour le reste de la partie."
```

---

### Task 4 : le trait de l'auteur vers sa cible

**Files:**
- Create: `ui-app/src/board/TraitCible.tsx`
- Test: `ui-app/src/board/TraitCible.test.tsx`
- Modify: `ui-app/src/board/DeroulePhase.tsx`
- Modify: `ui-app/src/board/board.css`

**Interfaces:**
- Consumes: `sceneDe` de `./deroule-scene`.
- Produces: `function TraitCible(props: { etape: EtapeDeroule | undefined; actif: boolean }): JSX.Element | null`

- [ ] **Step 1: Write the failing test**

```tsx
// Le trait qui relie l'attaquant a sa cible : on lit la scene d'un coup d'oeil.
//
// Un SVG pose par-dessus le plateau, en position fixe, recalcule a chaque
// etape depuis la position reelle des deux cartes.
import { afterEach, describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { TraitCible } from './TraitCible'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

function poserCarte(id: number, x: number, y: number): void {
  let scene = document.querySelector('.plateau-scene')
  if (!scene) {
    scene = document.createElement('div')
    scene.className = 'plateau-scene'
    document.body.append(scene)
  }
  const carte = document.createElement('article')
  carte.className = 'scan-card'
  carte.setAttribute('data-card-id', String(id))
  carte.getBoundingClientRect = () =>
    ({ left: x, top: y, width: 100, height: 140, right: x + 100, bottom: y + 140, x, y }) as DOMRect
  scene.append(carte)
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('trait vers la cible', () => {
  it('trace une ligne entre les deux cartes', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif />
    )
    expect(container.querySelector('line')).not.toBeNull()
  })

  it('ne trace rien sans cible', () => {
    poserCarte(50, 100, 100)
    const { container } = render(<TraitCible etape={etape({ carteId: 50 })} actif />)
    expect(container.querySelector('line')).toBeNull()
  })

  it('ne trace rien quand une des deux cartes a quitte la table', () => {
    // La cible peut etre morte entre le fait et son affichage.
    poserCarte(50, 100, 100)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 999 })} actif />
    )
    expect(container.querySelector('line')).toBeNull()
  })

  it('ne trace rien quand la mise en scene est coupee', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif={false} />
    )
    expect(container.querySelector('line')).toBeNull()
  })

  it('porte une pointe de fleche sur la cible', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif />
    )
    expect(container.querySelector('marker')).not.toBeNull()
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/TraitCible.test.tsx`
Expected: FAIL, import non resolu.

- [ ] **Step 3: Write minimal implementation**

```tsx
// Le trait qui relie l'attaquant a sa cible.
//
// Un SVG en position fixe par-dessus le plateau, jamais un dessin dans les
// cartes : il doit traverser la table sans etre rogne par les cadres, qui ont
// tous `overflow: hidden`.
//
// Les positions viennent de getBoundingClientRect au moment du rendu de
// l'etape. C'est suffisant : le plateau ne bouge pas pendant qu'une etape est
// affichee, et le trait disparait des que l'etape change.

import { useEffect, useState } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

type Segment = { x1: number; y1: number; x2: number; y2: number }

function centreDe(id: number): { x: number; y: number } | undefined {
  const el = document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${id}"]`
  )
  if (!el) return undefined
  const r = el.getBoundingClientRect()
  return { x: r.left + r.width / 2, y: r.top + r.height / 2 }
}

export function TraitCible({
  etape,
  actif,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
}) {
  const [segment, setSegment] = useState<Segment | undefined>(undefined)

  useEffect(() => {
    if (!actif || !etape) {
      setSegment(undefined)
      return
    }
    const scene = sceneDe(etape)
    if (!scene.trait || scene.carteEnAvant === undefined || scene.cible === undefined) {
      setSegment(undefined)
      return
    }
    const depart = centreDe(scene.carteEnAvant)
    const arrivee = centreDe(scene.cible)
    // Une carte a pu quitter la table entre le fait et son affichage : on ne
    // trace pas un trait vers le vide.
    if (!depart || !arrivee) {
      setSegment(undefined)
      return
    }
    setSegment({ x1: depart.x, y1: depart.y, x2: arrivee.x, y2: arrivee.y })
  }, [etape, actif])

  if (!segment) return null

  return (
    <svg className="deroule-trait" aria-hidden="true">
      <defs>
        <marker
          id="deroule-pointe"
          markerWidth="8"
          markerHeight="8"
          refX="7"
          refY="4"
          orient="auto"
        >
          <path d="M0,0 L8,4 L0,8 z" fill="#F0131E" />
        </marker>
      </defs>
      <line
        x1={segment.x1}
        y1={segment.y1}
        x2={segment.x2}
        y2={segment.y2}
        markerEnd="url(#deroule-pointe)"
      />
    </svg>
  )
}
```

- [ ] **Step 4: Add the styles**

Dans `ui-app/src/board/board.css`, à la suite du bloc de la tâche 3 :

```css
  /* Le trait traverse la table : il est POSE PAR-DESSUS, jamais dessine dans
     une carte, dont le cadre rogne son contenu. */
  .deroule-trait {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 530;
    pointer-events: none;
  }

  .deroule-trait line {
    stroke: #F0131E;
    stroke-width: 2.5;
    filter: drop-shadow(0 0 4px rgba(240, 19, 30, 0.7));
    /* Le trait se TRACE de l'attaquant vers sa cible : on lit le sens de
       l'attaque, on ne le devine pas. */
    stroke-dasharray: 1200;
    stroke-dashoffset: 1200;
    animation: deroule-tracer 260ms ease-out forwards;
  }

  @keyframes deroule-tracer {
    to {
      stroke-dashoffset: 0;
    }
  }

  body.plateau-sans-animations .deroule-trait line {
    animation: none;
    stroke-dashoffset: 0;
  }
```

et dans le bloc `@media (prefers-reduced-motion: reduce)` :

```css
    .deroule-trait line {
      animation: none;
      stroke-dashoffset: 0;
    }
```

- [ ] **Step 5: Brancher dans le cartouche**

Dans `ui-app/src/board/DeroulePhase.tsx`, à l'intérieur du `return`, avant la
balise `<section>`, envelopper dans un fragment :

```tsx
  return (
    <>
      <TraitCible etape={etape} actif={!termine} />
      <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
```

et fermer le fragment après `</section>`.

- [ ] **Step 6: Run tests**

Run: `cd ui-app && npx vitest run && npx tsc --noEmit`

- [ ] **Step 7: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/TraitCible.tsx ui-app/src/board/TraitCible.test.tsx ui-app/src/board/DeroulePhase.tsx ui-app/src/board/board.css
git commit -m "feat(deroule): un trait fleche de l'attaquant vers sa cible

SVG pose par-dessus le plateau, jamais dessine dans une carte : tous les
cadres ont overflow hidden et le rogneraient. Il se trace de l'un vers
l'autre, ce qui donne le sens de l'attaque. Rien n'est trace si une des deux
cartes a quitte la table entre le fait et son affichage."
```

---

### Task 5 : l'annonce de la phase

**Files:**
- Create: `ui-app/src/board/BandeauPhase.tsx`
- Test: `ui-app/src/board/BandeauPhase.test.tsx`
- Modify: `ui-app/src/board/board.css`
- Modify: `ui-app/src/board/dico-en.ts`
- Modify: `ui-app/src/board.tsx`

**Interfaces:**
- Produces: `function BandeauPhase(props: { round: number; actif: boolean }): JSX.Element | null`

- [ ] **Step 1: Write the failing test**

```tsx
// L'annonce de la phase du mechant : un bandeau rouge qui traverse l'ecran.
//
// Il se raccourcit a partir du round 4 : deux secondes de solennite a chaque
// round d'une partie qui en compte douze finiraient par lasser.
import { describe, expect, it, vi, afterEach } from 'vitest'
import { render, act } from '@testing-library/react'
import { BandeauPhase, DUREE_LONGUE_MS, DUREE_COURTE_MS } from './BandeauPhase'

afterEach(() => {
  vi.useRealTimers()
})

describe('annonce de phase', () => {
  it('s affiche quand la phase commence', () => {
    const { container } = render(<BandeauPhase round={1} actif />)
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
  })

  it('ne s affiche pas hors phase', () => {
    const { container } = render(<BandeauPhase round={1} actif={false} />)
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('annonce le round', () => {
    const { container } = render(<BandeauPhase round={3} actif />)
    expect(container.textContent).toContain('3')
  })

  it('disparait de lui-meme', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={1} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_LONGUE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('dure moins longtemps a partir du round 4', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={4} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_COURTE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('tient encore la duree longue au round 3', () => {
    vi.useFakeTimers()
    const { container } = render(<BandeauPhase round={3} actif />)
    act(() => {
      vi.advanceTimersByTime(DUREE_COURTE_MS + 100)
    })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/BandeauPhase.test.tsx`
Expected: FAIL, import non resolu.

- [ ] **Step 3: Write minimal implementation**

```tsx
// L'annonce de la phase du mechant.
//
// Un bandeau rouge qui traverse l'ecran, avec un eclair. Il ne coute AUCUN
// clic et ne bloque rien : la premiere etape est deja derriere lui.
//
// Il se raccourcit a partir du round 4. Deux secondes de solennite valent pour
// l'ouverture d'une partie ; repetees douze fois, elles se subissent.

import { useEffect, useState } from 'react'
import { t } from './langue'

/** Rounds 1 a 3 : on prend le temps de l'effet. */
export const DUREE_LONGUE_MS = 2000
/** A partir du round 4 : moitie moins. */
export const DUREE_COURTE_MS = 1000
/** Round a partir duquel l'annonce se raccourcit. */
export const ROUND_COURT = 4

export function BandeauPhase({ round, actif }: { round: number; actif: boolean }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!actif) {
      setVisible(false)
      return
    }
    setVisible(true)
    const duree = round >= ROUND_COURT ? DUREE_COURTE_MS : DUREE_LONGUE_MS
    const minuteur = window.setTimeout(() => setVisible(false), duree)
    return () => window.clearTimeout(minuteur)
  }, [actif, round])

  if (!visible) return null

  return (
    <div className="bandeau-phase" aria-hidden="true">
      <span className="bandeau-phase-eclair" />
      <p className="bandeau-phase-texte">
        {t('Phase du méchant')}
        <em>
          {t('Round')} {round}
        </em>
      </p>
    </div>
  )
}
```

- [ ] **Step 4: Add the styles and the English entry**

Dans `dico-en.ts` (vérifie d'abord que `'Round'` n'y est pas déjà) :

```ts
  'Round': 'Round',
```

Dans `board.css` :

```css
  /* --- Annonce de la phase du mechant --------------------------------------
     Un bandeau qui traverse l'ecran. Il ne coute aucun clic : la premiere
     etape est deja derriere lui. */
  .bandeau-phase {
    position: fixed;
    left: 0;
    right: 0;
    top: 38%;
    z-index: 560;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 18px 0;
    background: linear-gradient(
      90deg,
      transparent,
      #F0131E 12%,
      #F0131E 88%,
      transparent
    );
    box-shadow: 0 0 40px rgba(240, 19, 30, 0.6);
    pointer-events: none;
    animation: bandeau-traverse 520ms ease-out;
  }

  .bandeau-phase-texte {
    margin: 0;
    display: flex;
    align-items: baseline;
    gap: 14px;
    font-size: 1.6rem;
    font-weight: 900;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #ffffff;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.65);
  }

  .bandeau-phase-texte em {
    font-style: normal;
    font-size: 1rem;
    opacity: 0.85;
  }

  /* L'eclair : un trait clair qui file en travers du bandeau. */
  .bandeau-phase-eclair {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      100deg,
      transparent 40%,
      rgba(255, 255, 255, 0.85) 50%,
      transparent 60%
    );
    animation: bandeau-eclair 620ms ease-out;
  }

  @keyframes bandeau-traverse {
    from {
      transform: translateX(-100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes bandeau-eclair {
    from {
      transform: translateX(-60%);
    }
    to {
      transform: translateX(160%);
    }
  }

  body.plateau-sans-animations .bandeau-phase,
  body.plateau-sans-animations .bandeau-phase-eclair {
    animation: none;
  }
```

et dans le bloc `@media (prefers-reduced-motion: reduce)` :

```css
    .bandeau-phase,
    .bandeau-phase-eclair {
      animation: none;
    }
```

- [ ] **Step 5: Brancher dans le plateau**

Dans `ui-app/src/board.tsx`, à côté du montage de `DeroulePhase`, ajouter :

```tsx
      {modePhase === 'detaille' ? (
        <BandeauPhase
          round={etat.monde?.round_id ?? 1}
          actif={etapesDuDeroule.length > 0}
        />
      ) : null}
```

Note pour l'implémenteur : `etapesDuDeroule` est le nom de la variable
mémoïsée qui porte les étapes. Vérifie son nom exact dans `board.tsx` et
adapte. Vérifie aussi le nom du champ du round sur le monde (`round_id` dans
`world.ts`) avant de l'employer.

- [ ] **Step 6: Run tests**

Run: `cd ui-app && npx vitest run && npx tsc --noEmit`

- [ ] **Step 7: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/BandeauPhase.tsx ui-app/src/board/BandeauPhase.test.tsx ui-app/src/board/board.css ui-app/src/board/dico-en.ts ui-app/src/board.tsx
git commit -m "feat(deroule): l'annonce de la phase, bandeau rouge et eclair

Elle ne coute aucun clic : la premiere etape est deja derriere elle. Deux
secondes aux rounds 1 a 3, une seule a partir du round 4 : la solennite vaut
pour l'ouverture, repetee douze fois elle se subit."
```

---

### Task 6 : les boosts retournés un par un

**Files:**
- Modify: `ui-app/src/board/DeroulePhase.tsx`
- Modify: `ui-app/src/board/DeroulePhase.test.tsx`
- Modify: `ui-app/src/board/board.css`
- Modify: `ui-app/src/board/dico-en.ts`

**Interfaces:**
- Consumes: `EtapeDeroule.boosts` (déjà porté par le module pur, non affiché à ce jour).
- Produces: rien de neuf.

- [ ] **Step 1: Write the failing test**

Dans `DeroulePhase.test.tsx`, au `describe` existant :

```tsx
  it('retourne les boosts un par un', async () => {
    // Le moment de tension du jeu : chaque carte se lit avant la suivante.
    const avecBoosts: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'activations',
        titre: 'attaque',
        regle: 'regle:activations',
        carteId: 50,
        cibleId: 12,
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        boosts: [
          { cle: 'b0', nom: 'Boost A', cibleId: 91, apport: 1 },
          { cle: 'b1', nom: 'Boost B', cibleId: 92, apport: 2 },
        ],
        consequences: [],
      },
    ]
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
      expect(screen.getByText('Boost A')).toBeInTheDocument()
      expect(screen.queryByText('Boost B')).not.toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1600)
      })
      expect(screen.getByText('Boost B')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })

  it('n attend pas de clic pour les boosts : c est l etape qui attend', () => {
    const avecBoosts: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'activations',
        titre: 'attaque',
        regle: 'regle:activations',
        carteId: 50,
        boosts: [{ cle: 'b0', nom: 'Boost A', cibleId: 91, apport: 1 }],
        consequences: [],
      },
    ]
    render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
    expect(screen.getByRole('button', { name: /Suivant/i })).toBeInTheDocument()
  })

  it('n affiche aucun bloc de boost quand il n y en a pas', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-boosts')).toBeNull()
  })
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ui-app && npx vitest run src/board/DeroulePhase.test.tsx`
Expected: FAIL, les boosts ne sont pas rendus.

- [ ] **Step 3: Write minimal implementation**

Dans `DeroulePhase.tsx`, ajouter la constante en tête de fichier :

```tsx
/** Le temps de lire un boost a capacite avant le suivant. */
const DELAI_BOOST_MS = 1500
```

Ajouter l'état et l'effet AVANT le `return null` conditionnel, avec les autres
hooks :

```tsx
  // Combien de boosts sont deja retournes sur l'etape courante. Ils
  // s'enchainent SEULS : c'est l'etape qui attend la validation, pas chaque
  // carte. Une attaque a trois boosts couterait sinon quatre clics.
  const [boostsMontres, setBoostsMontres] = useState(0)

  useEffect(() => {
    setBoostsMontres(etape?.boosts.length ? 1 : 0)
  }, [etape])

  useEffect(() => {
    const total = etape?.boosts.length ?? 0
    if (boostsMontres === 0 || boostsMontres >= total) return
    const minuteur = window.setTimeout(
      () => setBoostsMontres((n) => n + 1),
      DELAI_BOOST_MS
    )
    return () => window.clearTimeout(minuteur)
  }, [boostsMontres, etape])
```

Dans le rendu, après le titre et avant la règle :

```tsx
      {etape.boosts.length > 0 ? (
        <ul className="deroule-boosts">
          {etape.boosts.slice(0, boostsMontres).map((boost) => (
            <li key={boost.cle}>
              <b>{boost.nom}</b>
              <span>+{boost.apport}</span>
            </li>
          ))}
        </ul>
      ) : null}
```

- [ ] **Step 4: Add the styles**

Dans `board.css`, à la suite du bloc `.deroule-consequences` :

```css
  /* Les cartes de boost, retournees une par une : c'est le moment de tension
     du jeu, il merite d'etre montre. */
  .deroule-boosts {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 0 0 10px;
    padding: 0;
    list-style: none;
  }

  .deroule-boosts li {
    display: flex;
    align-items: baseline;
    gap: 6px;
    padding: 4px 8px;
    font-size: 0.82rem;
    background: rgba(240, 19, 30, 0.16);
    border: 1px solid rgba(240, 19, 30, 0.5);
    border-radius: 6px;
    animation: deroule-boost-entre 220ms ease-out;
  }

  .deroule-boosts li span {
    font-weight: 900;
    color: #ffd24a;
  }

  @keyframes deroule-boost-entre {
    from {
      opacity: 0;
      transform: translateY(6px);
    }
    to {
      opacity: 1;
      transform: none;
    }
  }

  body.plateau-sans-animations .deroule-boosts li {
    animation: none;
  }
```

et dans le bloc `@media (prefers-reduced-motion: reduce)` :

```css
    .deroule-boosts li {
      animation: none;
    }
```

- [ ] **Step 5: Run tests**

Run: `cd ui-app && npx vitest run && npx tsc --noEmit`

- [ ] **Step 6: Commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/DeroulePhase.tsx ui-app/src/board/DeroulePhase.test.tsx ui-app/src/board/board.css
git commit -m "feat(deroule): les boosts se retournent un par un

C'est le moment de tension du jeu. Ils s'enchainent SEULS, a une seconde et
demie, et c'est l'etape qui attend la validation : une attaque a trois
boosts couterait sinon quatre clics."
```

---

### Task 7 : contrôle en partie réelle

**Files:** aucun. Cette tâche vérifie.

- [ ] **Step 1: Construire et lancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
cd Fusion/marvel-lcg-src
~/marvel-work/python/bin/python3.10 launcher_fast.py --no-browser
```

Attendre avec une boucle, jamais un sleep fixe (le launcher compile, cela prend
environ une minute) :

```bash
until curl -s -o /dev/null -m 3 http://127.0.0.1:2345/; do sleep 5; done; echo pret
```

- [ ] **Step 2: Jouer jusqu'à la phase du méchant**

Ouvrir `http://127.0.0.1:2345/prepare.html`, lancer une partie solo aléatoire,
passer le mulligan, finir le tour.

- [ ] **Step 3: Vérifier, point par point**

1. Le bandeau rouge traverse l'écran à l'ouverture de la phase, avec son éclair.
2. La carte qui agit grandit sur place, le reste du plateau s'assombrit sans devenir illisible.
3. Le trait fléché relie l'attaquant à sa cible, et se trace dans ce sens.
4. Les boosts se retournent un par un, sans clic.
5. Le cartouche reste lisible par-dessus le voile.
6. Rien ne reste affiché après la fin de la phase : ni voile, ni carte agrandie, ni trait.
7. **Jouer jusqu'au round 4** et vérifier que le bandeau se raccourcit.
8. **L'impact** : le chiffre qui jaillit sur la carte touchée et sa secousse. Ce mécanisme existe déjà (`useEffetsCartes` dans `board.tsx`, styles `card-effect-delta` et `a-delta-damage` dans `ScanCard.css`) et n'a demandé aucun développement ici. Ce qu'il faut vérifier, c'est qu'il tombe désormais AU BON MOMENT : le moteur attend nos validations depuis la livraison 1, donc l'effet doit apparaître pendant l'étape qui le raconte, et non tout d'un bloc en début de phase. Si ce n'est pas le cas, c'est un vrai constat à remonter.

- [ ] **Step 4: Vérifier le débrayage**

Couper les animations dans les options du plateau, refaire une phase : les
étapes, les textes et les validations doivent être identiques, sans aucun
mouvement, sans bandeau ni trait animé.

- [ ] **Step 5: Arrêter le jeu**

```bash
pkill -f launcher_fast
```

- [ ] **Step 6: Consigner**

Écrire ce qui a été observé, tout écart avec la spec, et tout défaut d'assemblage
que les tests ne pouvaient pas voir. Les deux défauts les plus graves de la
livraison 1 ont été trouvés ainsi.

---

## Ce que cette livraison ne fait PAS

**Les sons ne sont pas dans cette livraison, et c'est une décision.** La spec
demande un son sur les moments forts. Or `ui-app/src/board/sons.ts` ne choisit
rien : il joue le son que le MOTEUR annonce dans `monde.sound_name`, et son
cache ne connaît que des fichiers `.wav` servis à la racine. Ajouter des sons
propres au déroulé supposerait de nouveaux fichiers audio, que le dépôt n'a pas,
et référencer un fichier absent ne produirait qu'un silence et une requête en
erreur. À reprendre le jour où les fichiers existent, ou à retirer de la spec.

Réservé à la livraison 3 :

- Les cas particuliers : ennemi étourdi, étape sans contenu, héros vaincu, défaite en pleine phase, sbire entrant en cours de phase.
- Le récapitulatif de fin de phase raccourci, et sa réintroduction en mode détaillé.
- Le menu Options à quatre choix expliqués.
- La version mobile simplifiée.
- Les étapes de distribution et de passage du premier joueur.
- Le déroulé pour les effets subis pendant le tour du joueur.
