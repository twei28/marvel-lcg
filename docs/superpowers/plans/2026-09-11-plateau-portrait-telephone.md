# Plateau portrait sur téléphone — plan d'implémentation

> **Pour un agent exécutant :** SOUS-SKILL REQUIS — `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans`, tâche par tâche. Les étapes sont des cases à cocher (`- [ ]`).

**But :** le téléphone joue le plateau en portrait, sur un seul écran sans défilement, calqué sur `play.marvelsimulator.com`.

**Architecture :** un composant `PlateauPortrait` accepte exactement les `BoardProps` du plateau PC, comme le fait déjà `PlateauPaysage`. Il empile des blocs en colonne : bandeau, vilain, complot, rencontre, engagés, héros, main, barre. La répartition « quel emplacement va dans quel bloc » vit dans un module pur et testable, `blocs-portrait.ts`. Le panneau de décision est `AssistantAction`, déjà en place.

**Pile technique :** React 19, TypeScript 6, Vite 8, vitest + @testing-library/react, CSS en `@layer` (`composants` puis `utilitaires`).

**Spec :** `docs/superpowers/specs/2026-09-11-plateau-portrait-telephone-design.md`

## Contraintes globales

- Français dans tout le code, commentaires compris. Les commentaires disent **pourquoi**, jamais **quoi**.
- TDD strict : le test échoue AVANT l'implémentation, on le regarde échouer.
- `npm run typecheck` propre et `npm test` entièrement vert avant chaque commit.
- Aucun `any` non justifié en commentaire local.
- Les fichiers CSS nouveaux se rangent en `@layer composants`.
- Ne jamais modifier `PlateauPaysage.tsx`, `paysage.css`, `PlateauMedaillons.tsx`, `medaillon.css` : ils restent en place, simplement plus servis sur téléphone.
- Commandes depuis `ui-app/` : `npm test -- <fichier>`, `npm run typecheck`, `npm run build`.
- Attribution des commits : `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` puis `Claude-Session: https://claude.ai/code/session_0174FEXTRk4Vd1jhGJTcDNBF`.

---

### Tâche 1 : l'aiguillage par le petit côté de l'écran

**Fichiers :**
- Modifier : `ui-app/src/board/mobile/useModeMobile.ts`
- Test : `ui-app/src/board/mobile/useModeMobile.test.ts`

**Interfaces :**
- Produit : `REQUETE_MOBILE` (constante, nouvelle valeur), `modeEffectif(reglage: ReglageMode, correspond: boolean): ModeRendu` (signature inchangée).

- [ ] **Étape 1 : écrire le test qui échoue**

Ajouter dans `useModeMobile.test.ts` :

```ts
import { REQUETE_MOBILE } from './useModeMobile'

/** Une media query évaluée à la main, pour éprouver la règle sans navigateur. */
function correspond(requete: string, largeur: number, hauteur: number): boolean {
  return requete.split(',').some((clause) => {
    const max = /\(max-(width|height):\s*(\d+)px\)/.exec(clause.trim())
    if (!max) return false
    return (max[1] === 'width' ? largeur : hauteur) <= Number(max[2])
  })
}

describe('REQUETE_MOBILE : le petit côté décide', () => {
  it('prend les téléphones, debout comme couchés', () => {
    expect(correspond(REQUETE_MOBILE, 390, 844)).toBe(true)
    expect(correspond(REQUETE_MOBILE, 844, 390)).toBe(true)
  })

  it('LAISSE les tablettes au plateau PC, dans les deux sens', () => {
    expect(correspond(REQUETE_MOBILE, 768, 1024)).toBe(false)
    expect(correspond(REQUETE_MOBILE, 1024, 768)).toBe(false)
  })

  it('laisse un ordinateur au plateau PC', () => {
    expect(correspond(REQUETE_MOBILE, 1440, 900)).toBe(false)
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/useModeMobile.test.ts`
Attendu : ÉCHEC, la tablette 768x1024 rend `true` (la règle actuelle est `max-width: 900px`).

- [ ] **Étape 3 : écrire la règle**

Dans `useModeMobile.ts`, remplacer la constante et son commentaire :

```ts
/**
 * Le PETIT COTE de l'ecran decide, pas la largeur.
 *
 * La regle etait `(max-width: 900px), (pointer: coarse)`. Elle attrapait les
 * tablettes, que l'on veut desormais sur le plateau PC (spec du 11/09/2026) :
 * un iPad en paysage a la place d'une vraie table, lui demander de tourner
 * serait absurde. Et `pointer: coarse` seul ne distingue pas un telephone
 * couche d'une tablette.
 *
 *   telephone debout  390x844  -> largeur 390 <= 600  : mobile
 *   telephone couche  844x390  -> hauteur 390 <= 500  : mobile
 *   tablette          768x1024 -> ni l'un ni l'autre  : plateau PC
 */
export const REQUETE_MOBILE = '(max-width: 600px), (max-height: 500px)'
```

- [ ] **Étape 4 : vérifier que le test passe**

`npm test -- src/board/mobile/useModeMobile.test.ts` puis `npm test` entier.
Attendu : tout vert. Si un test du paysage dépendait de l'ancienne règle, le corriger en gardant son intention.

- [ ] **Étape 5 : commit**

```bash
git add ui-app/src/board/mobile/useModeMobile.ts ui-app/src/board/mobile/useModeMobile.test.ts
git commit -m "feat(mobile): le petit cote de l'ecran decide du mode, pas la largeur"
```

---

### Tâche 2 : le téléphone ne joue qu'en portrait

**Fichiers :**
- Créer : `ui-app/src/board/mobile/EcranPaysage.tsx`
- Créer : `ui-app/src/board/mobile/PlateauPortrait.tsx` (coquille, remplie ensuite)
- Créer : `ui-app/src/board/mobile/portrait.css`
- Modifier : `ui-app/src/board/mobile/PlateauMobile.tsx`
- Test : `ui-app/src/board/mobile/PlateauMobile.test.tsx`

**Interfaces :**
- Consomme : `BoardProps` (`../Board`), `useOrientation(): 'portrait' | 'paysage'`.
- Produit : `EcranPaysage()`, `PlateauPortrait(props: BoardProps)`.

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { PlateauMobile } from './PlateauMobile'
import type { BoardProps } from '../Board'

vi.mock('./useOrientation', () => ({ useOrientation: () => orientation }))
let orientation: 'portrait' | 'paysage' = 'portrait'

const props = {
  world: { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] },
  playerId: 0,
  plateau: { emplacements: [], nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 },
} as unknown as BoardProps

describe('le telephone ne joue qu en portrait', () => {
  it('monte le plateau portrait quand l ecran est debout', () => {
    orientation = 'portrait'
    const { container } = render(<PlateauMobile {...props} />)
    expect(container.querySelector('.plateau-portrait')).not.toBeNull()
    expect(screen.queryByText(/remets ton/i)).toBeNull()
  })

  it('demande de remettre l ecran droit quand il est couche', () => {
    orientation = 'paysage'
    render(<PlateauMobile {...props} />)
    expect(screen.getByText(/remets ton téléphone droit/i)).toBeInTheDocument()
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/PlateauMobile.test.tsx`
Attendu : ÉCHEC, `.plateau-portrait` absent (`PlateauMobile` monte `PlateauPaysage`).

- [ ] **Étape 3 : écrire les trois fichiers**

`EcranPaysage.tsx` :

```tsx
// « Remets ton telephone droit » : le voile qui couvre le plateau en paysage.
//
// C'est l'exact inverse d'EcranPortrait, qui disait le contraire jusqu'au
// 11/09/2026. Le telephone joue desormais DEBOUT : c'est ainsi qu'on le tient,
// et la hauteur est ce qui permet au panneau de decision de vivre en bas.
//
// Comme son predecesseur, ce voile ne demonte rien : la partie continue
// dessous, la connexion au moteur aussi, et une question posee pendant la
// rotation est toujours la au retour.
import { t } from '../langue'
import './portrait.css'

export function EcranPaysage() {
  return (
    <div
      className="ecran-paysage"
      role="dialog"
      aria-modal="true"
      aria-label={t('Remets ton téléphone droit')}
    >
      <span className="ecran-paysage-icone" aria-hidden="true" />
      <p>
        <strong>{t('Remets ton téléphone droit')}</strong>
        <br />
        {t('Le plateau se joue debout.')}
      </p>
    </div>
  )
}
```

`PlateauPortrait.tsx`, coquille que les tâches suivantes remplissent :

```tsx
// Le plateau en PORTRAIT : une colonne, un seul ecran, aucun defilement.
//
// Spec : docs/superpowers/specs/2026-09-11-plateau-portrait-telephone-design.md
//
// Releve mesure sur play.marvelsimulator.com : leur page ne defile pas
// (scrollHeight == innerHeight), et cela ne tient que parce que la table n'est
// PAS faite de cartes jouables. Le vilain, le complot et les allies sont la
// vraie carte en petit, avec leurs chiffres en gros A COTE. Seule la main est
// en cartes qu'on lit a vue.
//
// Il accepte exactement les BoardProps du plateau PC, comme PlateauPaysage :
// c'est ce qui permet a board.tsx de choisir sans rien adapter.
import type { BoardProps } from '../Board'
import './portrait.css'

export function PlateauPortrait(_props: BoardProps) {
  return <main className="plateau-portrait" />
}
```

`portrait.css` :

```css
@layer composants {
  /* Une colonne, la hauteur de l'ecran, et RIEN qui deborde : le plateau
     portrait ne defile jamais (spec du 11/09/2026). Les blocs se partagent la
     hauteur, la main et la barre restent collees en bas. */
  .plateau-portrait {
    position: fixed;
    inset: 0;
    display: grid;
    grid-template-rows: auto 1fr auto;
    overflow: hidden;
    background: var(--fond);
  }

  .ecran-paysage {
    position: fixed;
    inset: 0;
    z-index: 900;
    display: grid;
    place-content: center;
    gap: 14px;
    justify-items: center;
    text-align: center;
    color: #f8fafc;
    background: var(--fond);
  }

  .ecran-paysage-icone {
    width: 42px;
    height: 66px;
    border: 3px solid currentColor;
    border-radius: 9px;
    transform: rotate(90deg);
  }
}
```

`PlateauMobile.tsx` : remplacer le corps du composant.

```tsx
export function PlateauMobile(props: BoardProps) {
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  // Le telephone joue DEBOUT (spec du 11/09/2026). Couche, on le lui dit sans
  // rien demonter : la partie continue derriere le voile.
  if (useOrientation() === 'paysage') return <EcranPaysage />
  return <PlateauPortrait {...props} />
}
```

⚠ `useOrientation()` est un hook : il doit être appelé AVANT tout `return` conditionnel. Écrire :

```tsx
export function PlateauMobile(props: BoardProps) {
  const orientation = useOrientation()
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  if (orientation === 'paysage') return <EcranPaysage />
  return <PlateauPortrait {...props} />
}
```

- [ ] **Étape 4 : ajouter les deux libellés au dictionnaire anglais**

Dans `ui-app/src/board/dico-en.ts`, à côté des libellés mobiles existants :

```ts
  'Remets ton téléphone droit': 'Turn your phone upright',
  'Le plateau se joue debout.': 'The board is played upright.',
```

- [ ] **Étape 5 : vérifier que le test passe**

`npm test -- src/board/mobile/PlateauMobile.test.tsx` puis `npm test` et `npm run typecheck`.

- [ ] **Étape 6 : commit**

```bash
git add ui-app/src/board/mobile/EcranPaysage.tsx ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/portrait.css ui-app/src/board/mobile/PlateauMobile.tsx ui-app/src/board/mobile/PlateauMobile.test.tsx ui-app/src/board/dico-en.ts
git commit -m "feat(portrait): le telephone joue debout, le paysage demande de le redresser"
```

---

### Tâche 3 : la répartition des blocs, module pur

**Fichiers :**
- Créer : `ui-app/src/board/mobile/blocs-portrait.ts`
- Test : `ui-app/src/board/mobile/blocs-portrait.test.ts`

**Interfaces :**
- Consomme : `Plateau`, `EmplacementAffiche`, `UniteAffichee`, `CleEmplacement` (`../zones`).
- Produit :
  ```ts
  export type CleBloc = 'vilain' | 'complot' | 'rencontre' | 'engages' | 'heros' | 'main'
  export type BlocPortrait = { cle: CleBloc; titre: string; unites: UniteAffichee[] }
  export function repartirEnBlocs(plateau: Plateau): BlocPortrait[]
  ```

- [ ] **Étape 1 : écrire le test qui échoue**

```ts
import { describe, expect, it } from 'vitest'
import { repartirEnBlocs } from './blocs-portrait'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { CleEmplacement } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'minion' }, attachees: [] }) as unknown as UniteAffichee

const emplacement = (cle: CleEmplacement, noms: string[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [noms.map(unite)], nombreSurLaLigne: noms.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

describe('repartirEnBlocs', () => {
  it('range chaque emplacement dans son bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(
        emplacement('terrain-combat', ['Rhino']),
        emplacement('complot-principal', ['L’Effraction']),
        emplacement('piles-rencontre', ['Deck']),
        emplacement('terrain-soutien', ['Steve Rogers']),
        emplacement('main', ['Quinjet']),
      )
    )
    const par = (cle: string) => blocs.find((b) => b.cle === cle)?.unites.map((u) => u.cle)
    expect(par('vilain')).toEqual(['Rhino'])
    expect(par('complot')).toEqual(['L’Effraction'])
    expect(par('rencontre')).toEqual(['Deck'])
    expect(par('heros')).toEqual(['Steve Rogers'])
    expect(par('main')).toEqual(['Quinjet'])
  })

  it('rend TOUJOURS les six blocs, meme vides', () => {
    const blocs = repartirEnBlocs(plateau())
    expect(blocs.map((b) => b.cle)).toEqual(['vilain', 'complot', 'rencontre', 'engages', 'heros', 'main'])
    expect(blocs.every((b) => b.unites.length === 0)).toBe(true)
  })

  it('garde l ordre des emplacements a l interieur d un bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(emplacement('complot-principal', ['Principal']), emplacement('complots-secondaires', ['Annexe']))
    )
    expect(blocs.find((b) => b.cle === 'complot')?.unites.map((u) => u.cle)).toEqual(['Principal', 'Annexe'])
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/blocs-portrait.test.ts`
Attendu : ÉCHEC, `repartirEnBlocs is not a function`.

- [ ] **Étape 3 : écrire le module**

```ts
// Quel emplacement de la table va dans quel bloc du portrait.
//
// Isole du rendu, et pur : c'est la seule chose qu'on peut se tromper sans
// qu'un test de composant ne le voie. Les six blocs sont TOUJOURS rendus, meme
// vides : le portrait ne defile pas, sa hauteur doit donc etre previsible d'un
// tour a l'autre — un bloc qui apparait ferait sauter tous les autres.
import type { CleEmplacement, Plateau, UniteAffichee } from '../zones'

export type CleBloc = 'vilain' | 'complot' | 'rencontre' | 'engages' | 'heros' | 'main'

export type BlocPortrait = {
  cle: CleBloc
  titre: string
  unites: UniteAffichee[]
}

/** L'ordre est celui de l'ecran, de haut en bas. */
const BLOCS: Array<{ cle: CleBloc; titre: string; emplacements: CleEmplacement[] }> = [
  { cle: 'vilain', titre: 'Méchant', emplacements: ['terrain-combat'] },
  { cle: 'complot', titre: 'Manigances', emplacements: ['complot-principal', 'complots-secondaires'] },
  { cle: 'rencontre', titre: 'Rencontre', emplacements: ['piles-rencontre', 'rencontre', 'deck-special'] },
  { cle: 'engages', titre: 'Engagés', emplacements: ['nemesis', 'annexes'] },
  { cle: 'heros', titre: 'Ton héros', emplacements: ['terrain-soutien', 'reserve', 'piles-joueur'] },
  { cle: 'main', titre: 'Ta main', emplacements: ['main'] },
]

export function repartirEnBlocs(plateau: Plateau): BlocPortrait[] {
  return BLOCS.map(({ cle, titre, emplacements }) => ({
    cle,
    titre,
    unites: emplacements.flatMap((voulu) =>
      plateau.emplacements
        .filter((emplacement) => emplacement.cle === voulu)
        .flatMap((emplacement) => emplacement.groupes.flat())
    ),
  }))
}
```

- [ ] **Étape 4 : vérifier que le test passe**

`npm test -- src/board/mobile/blocs-portrait.test.ts`

- [ ] **Étape 5 : commit**

```bash
git add ui-app/src/board/mobile/blocs-portrait.ts ui-app/src/board/mobile/blocs-portrait.test.ts
git commit -m "feat(portrait): la repartition des blocs, isolee et testee"
```

---

### Tâche 4 : le bandeau de statut et le bloc vilain

**Fichiers :**
- Créer : `ui-app/src/board/mobile/BandeauPortrait.tsx`
- Créer : `ui-app/src/board/mobile/CarteAvecChiffres.tsx`
- Modifier : `ui-app/src/board/mobile/PlateauPortrait.tsx`, `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/BandeauPortrait.test.tsx`, `ui-app/src/board/mobile/CarteAvecChiffres.test.tsx`

**Interfaces :**
- Consomme : `libelleRound(monde)`, `libellePhase(monde)`, `libelleQuiAgit(monde, etat)` de `../etat-partie` ; `ScanCard` et `ScanCardProps` de `../../components/ScanCard`.
- Produit :
  ```ts
  export function BandeauPortrait({ monde, aNous, connecte, demande }: {
    monde: World | undefined; aNous: boolean; connecte: boolean; demande?: unknown
  }): ReactElement

  export function CarteAvecChiffres({ carte, nom, surtitre, chiffres, onOuvrir }: {
    carte: ScanCardProps
    nom: string
    surtitre?: string
    chiffres: Array<{ valeur: string; libelle: string }>
    onOuvrir?: () => void
  }): ReactElement
  ```

- [ ] **Étape 1 : écrire les tests qui échouent**

`CarteAvecChiffres.test.tsx` :

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { CarteAvecChiffres } from './CarteAvecChiffres'
import type { ScanCardProps } from '../../components/ScanCard'

const carte: ScanCardProps = { id: '1', name: 'Rhino', kind: 'villain', imageUrl: '/scan/01097' }

describe('CarteAvecChiffres', () => {
  it('met les chiffres A COTE de la carte, jamais dessus', () => {
    const { container } = render(
      <CarteAvecChiffres carte={carte} nom="RHINO" surtitre="Stade 1" chiffres={[{ valeur: '14/14', libelle: 'PV' }]} />
    )
    // La carte et les chiffres sont FRERES : aucun chiffre a l'interieur du scan.
    expect(container.querySelector('.scan-card .portrait-chiffre')).toBeNull()
    expect(container.querySelector('.portrait-carte-chiffres .portrait-chiffre')).not.toBeNull()
    expect(screen.getByText('14/14')).toBeInTheDocument()
    expect(screen.getByText('PV')).toBeInTheDocument()
    expect(screen.getByText('RHINO')).toBeInTheDocument()
    expect(screen.getByText('Stade 1')).toBeInTheDocument()
  })

  it('sans chiffre, n affiche pas de colonne vide', () => {
    const { container } = render(<CarteAvecChiffres carte={carte} nom="RHINO" chiffres={[]} />)
    expect(container.querySelector('.portrait-carte-chiffres')).toBeNull()
  })
})
```

`BandeauPortrait.test.tsx` :

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { BandeauPortrait } from './BandeauPortrait'
import type { World } from '../world'

const monde = (phase: string, round = 2): World =>
  ({ render_id: 1, round_id: round, phase, players: [{ area_hero: [{ name: '* Steve Rogers' }] }] }) as unknown as World

describe('BandeauPortrait', () => {
  it('dit le round, la phase et a qui de jouer', () => {
    render(<BandeauPortrait monde={monde('Player 1 Turn')} aNous connecte demande={{}} />)
    expect(screen.getByText('Round 2')).toBeInTheDocument()
    expect(screen.getByText('Tour de Steve Rogers')).toBeInTheDocument()
    expect(screen.getByText('À toi de jouer')).toBeInTheDocument()
  })

  it('dit qui on attend quand ce n est pas notre tour', () => {
    render(<BandeauPortrait monde={monde('Enemy Activation')} aNous={false} connecte />)
    expect(screen.getByText('Le méchant agit')).toBeInTheDocument()
  })
})
```

- [ ] **Étape 2 : regarder les tests échouer**

`npm test -- src/board/mobile/CarteAvecChiffres.test.tsx src/board/mobile/BandeauPortrait.test.tsx`
Attendu : ÉCHEC, les deux composants n'existent pas.

- [ ] **Étape 3 : écrire les deux composants**

`CarteAvecChiffres.tsx` :

```tsx
// Une carte de la table en PETIT, avec ses chiffres en gros A COTE.
//
// C'est le geste central du portrait, releve sur play.marvelsimulator.com le
// 11/09/2026 : ils ne posent JAMAIS un chiffre sur l'illustration. Sur un
// telephone, une bulle « 14/14 » collee sur une carte de 70 px devient
// illisible et cache le dessin ; le meme chiffre pose a cote, en gros, se lit
// sans effort et laisse la carte entiere.
import type { ReactElement } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'

export function CarteAvecChiffres({
  carte,
  nom,
  surtitre,
  chiffres,
  onOuvrir,
}: {
  carte: ScanCardProps
  nom: string
  surtitre?: string
  chiffres: Array<{ valeur: string; libelle: string }>
  onOuvrir?: () => void
}): ReactElement {
  return (
    <div className="portrait-carte">
      <ScanCard {...carte} highlight={false} onSelect={onOuvrir} />
      <div className="portrait-carte-texte">
        {surtitre ? <span className="portrait-surtitre">{surtitre}</span> : null}
        <strong className="portrait-nom">{nom}</strong>
      </div>
      {chiffres.length > 0 ? (
        <div className="portrait-carte-chiffres">
          {chiffres.map(({ valeur, libelle }) => (
            <span className="portrait-chiffre" key={libelle}>
              <b>{valeur}</b>
              <small>{libelle}</small>
            </span>
          ))}
        </div>
      ) : null}
    </div>
  )
}
```

`BandeauPortrait.tsx` :

```tsx
// Le bandeau colle en haut du portrait : ou on en est, et qui doit agir.
//
// Trois segments, comme la barre du plateau PC depuis le 11/09/2026 et comme
// le « Turn 1 | PLAYER PHASE | STEVE ROGERS TO ACT » de l'autre site. C'est la
// premiere chose qu'on lit en reprenant son telephone.
import type { ReactElement } from 'react'
import { libellePhase, libelleQuiAgit, libelleRound } from '../etat-partie'
import type { World } from '../world'

export function BandeauPortrait({
  monde,
  aNous,
  connecte,
  demande,
}: {
  monde: World | undefined
  aNous: boolean
  connecte: boolean
  demande?: unknown
}): ReactElement {
  const quiAgit = libelleQuiAgit(monde, { aNous, connecte, demande })
  return (
    <header className="portrait-bandeau" role="status">
      <strong>{libelleRound(monde)}</strong>
      <span>{libellePhase(monde)}</span>
      {quiAgit ? <em>{quiAgit}</em> : null}
    </header>
  )
}
```

- [ ] **Étape 4 : brancher dans `PlateauPortrait` et habiller**

Dans `PlateauPortrait.tsx`, remplacer le corps :

```tsx
export function PlateauPortrait(props: BoardProps) {
  const blocs = repartirEnBlocs(props.plateau)
  const vilain = blocs.find((bloc) => bloc.cle === 'vilain')?.unites ?? []
  return (
    <main className="plateau-portrait">
      <BandeauPortrait monde={props.world} aNous connecte />
      <div className="portrait-table">
        {vilain.map((unite) => (
          <CarteAvecChiffres
            key={unite.cle}
            carte={unite.carte}
            nom={unite.carte.name}
            chiffres={(unite.carte.stats ?? []).map((stat) => ({
              valeur: String(stat.value),
              libelle: stat.label,
            }))}
          />
        ))}
      </div>
    </main>
  )
}
```

Dans `portrait.css`, en `@layer composants` :

```css
  .portrait-bandeau {
    display: flex;
    align-items: baseline;
    gap: 10px;
    padding: 8px 12px;
    background: var(--cadre);
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  }

  .portrait-bandeau strong {
    font-size: 0.95rem;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--menace);
  }

  .portrait-bandeau span {
    font-size: 0.82rem;
    color: #cbd5e1;
  }

  .portrait-bandeau em {
    margin-left: auto;
    font-style: normal;
    font-size: 0.78rem;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--info);
  }

  /* La carte en petit, son nom, et les chiffres a cote : trois colonnes. */
  .portrait-carte {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 10px;
    padding: 6px 12px;
    --card-w: 64px;
  }

  .portrait-surtitre {
    display: block;
    font-size: 0.68rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--info);
  }

  .portrait-nom {
    font-size: 1.25rem;
    line-height: 1.05;
    text-transform: uppercase;
  }

  .portrait-carte-chiffres {
    display: flex;
    gap: 12px;
  }

  .portrait-chiffre {
    display: grid;
    justify-items: center;
  }

  .portrait-chiffre b {
    font-size: 1.5rem;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }

  .portrait-chiffre small {
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8a94a3;
  }
```

- [ ] **Étape 5 : vérifier**

`npm test` entier et `npm run typecheck`.

- [ ] **Étape 6 : commit**

```bash
git add ui-app/src/board/mobile/BandeauPortrait.tsx ui-app/src/board/mobile/BandeauPortrait.test.tsx ui-app/src/board/mobile/CarteAvecChiffres.tsx ui-app/src/board/mobile/CarteAvecChiffres.test.tsx ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/portrait.css
git commit -m "feat(portrait): le bandeau de statut et le vilain, chiffres a cote de la carte"
```

---

### Tâche 5 : le complot principal et sa barre segmentée, les compteurs de rencontre

**Fichiers :**
- Créer : `ui-app/src/board/mobile/BarreMenace.tsx`
- Créer : `ui-app/src/board/mobile/CompteursPortrait.tsx`
- Modifier : `ui-app/src/board/mobile/PlateauPortrait.tsx`, `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/BarreMenace.test.tsx`

**Interfaces :**
- Produit :
  ```ts
  export function BarreMenace({ pose, total }: { pose: number; total: number }): ReactElement
  export function CompteursPortrait({ compteurs }: {
    compteurs: Array<{ valeur: number; libelle: string }>
  }): ReactElement
  ```

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { BarreMenace } from './BarreMenace'

describe('BarreMenace', () => {
  it('dessine une case par point de menace, et remplit celles qui sont posees', () => {
    const { container } = render(<BarreMenace pose={1} total={6} />)
    expect(container.querySelectorAll('.barre-menace-case')).toHaveLength(6)
    expect(container.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(1)
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('/6')).toBeInTheDocument()
  })

  it('dit son etat aux lecteurs d ecran', () => {
    render(<BarreMenace pose={3} total={6} />)
    const jauge = screen.getByRole('meter')
    expect(jauge).toHaveAttribute('aria-valuenow', '3')
    expect(jauge).toHaveAttribute('aria-valuemax', '6')
  })

  it('ne dessine RIEN quand le total est inconnu', () => {
    // Un complot sans seuil (certaines manigances annexes) : une barre de zero
    // case serait un trait vide, pire que pas de barre.
    const { container } = render(<BarreMenace pose={2} total={0} />)
    expect(container.querySelector('.barre-menace')).toBeNull()
  })

  it('ne deborde pas quand la menace depasse le seuil', () => {
    const { container } = render(<BarreMenace pose={9} total={6} />)
    expect(container.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(6)
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/BarreMenace.test.tsx`
Attendu : ÉCHEC, `BarreMenace` n'existe pas.

- [ ] **Étape 3 : écrire les deux composants**

`BarreMenace.tsx` :

```tsx
// La menace en CASES, pas en pourcentage.
//
// Releve sur play.marvelsimulator.com : une barre decoupee en autant de cases
// que le seuil, et le chiffre geant a cote. On lit « il reste cinq coups » d'un
// coup d'oeil, la ou « 16,7 % » demande un calcul.
import type { ReactElement } from 'react'
import { t } from '../langue'

export function BarreMenace({ pose, total }: { pose: number; total: number }): ReactElement | null {
  // Sans seuil connu, une barre de zero case serait un trait vide : on se tait.
  if (total <= 0) return null
  const remplies = Math.min(pose, total)
  return (
    <div className="barre-menace-bloc">
      <div
        className="barre-menace"
        role="meter"
        aria-valuenow={pose}
        aria-valuemin={0}
        aria-valuemax={total}
        aria-label={t('Menace')}
      >
        {Array.from({ length: total }, (_, index) => (
          <span className={`barre-menace-case${index < remplies ? ' est-pose' : ''}`} key={index} />
        ))}
      </div>
      <span className="barre-menace-compte">
        <b>{pose}</b>
        <small>/{total}</small>
        <em>{t('Menace')}</em>
      </span>
    </div>
  )
}
```

`CompteursPortrait.tsx` :

```tsx
// Les compteurs de la rencontre : gros chiffre, libelle minuscule.
//
// « 33 RENCONTRE · 0 DÉFAUSSE · 5 DE CÔTÉ ». Meme hierarchie que le reste du
// portrait : le chiffre saute aux yeux, le mot se lit si on le cherche.
import type { ReactElement } from 'react'

export function CompteursPortrait({
  compteurs,
}: {
  compteurs: Array<{ valeur: number; libelle: string }>
}): ReactElement | null {
  if (compteurs.length === 0) return null
  return (
    <div className="portrait-compteurs">
      {compteurs.map(({ valeur, libelle }) => (
        <span className="portrait-chiffre" key={libelle}>
          <b>{valeur}</b>
          <small>{libelle}</small>
        </span>
      ))}
    </div>
  )
}
```

- [ ] **Étape 4 : brancher, et lire la menace depuis le monde**

Dans `PlateauPortrait.tsx`, le bloc complot rend `CarteAvecChiffres` pour la manigance principale, suivi de `BarreMenace`. La menace posée et le seuil se lisent sur la carte du monde : `carte.stats` porte déjà les valeurs que la table affiche. Écrire un accesseur local, testé par les tests de composant :

```tsx
/** La menace posee et le seuil d'une manigance, lus sur ses stats. */
function menaceDe(carte: ScanCardProps): { pose: number; total: number } {
  const stats = carte.stats ?? []
  const valeur = (label: string) => stats.find((stat) => stat.label === label)?.value ?? 0
  return { pose: valeur('MEN'), total: valeur('MAX') }
}
```

⚠ Vérifier les vrais libellés dans `card-model.ts` (`toScanCard`) avant de figer `'MEN'` et `'MAX'` : si les labels diffèrent, corriger ici plutôt que d'inventer. Chercher avec `grep -n "label:" ui-app/src/board/card-model.ts`.

Ajouter à `portrait.css` :

```css
  .barre-menace-bloc {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 12px 6px;
  }

  .barre-menace {
    display: flex;
    flex: 1;
    gap: 3px;
  }

  .barre-menace-case {
    flex: 1;
    height: 10px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.18);
  }

  .barre-menace-case.est-pose {
    background: var(--menace);
    border-color: var(--menace-clair);
  }

  .barre-menace-compte b {
    font-size: 1.5rem;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }

  .barre-menace-compte small {
    font-size: 0.8rem;
    color: #8a94a3;
  }

  .barre-menace-compte em {
    margin-left: 6px;
    font-style: normal;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8a94a3;
  }

  .portrait-compteurs {
    display: flex;
    gap: 18px;
    padding: 4px 12px 8px;
  }
```

- [ ] **Étape 5 : vérifier**

`npm test` entier et `npm run typecheck`.

- [ ] **Étape 6 : commit**

```bash
git add ui-app/src/board/mobile/BarreMenace.tsx ui-app/src/board/mobile/BarreMenace.test.tsx ui-app/src/board/mobile/CompteursPortrait.tsx ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/portrait.css
git commit -m "feat(portrait): la menace en cases, et les compteurs de rencontre"
```

---

### Tâche 6 : ennemis engagés, héros et alliés

**Fichiers :**
- Modifier : `ui-app/src/board/mobile/PlateauPortrait.tsx`, `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/PlateauPortrait.test.tsx`

**Interfaces :**
- Consomme : `repartirEnBlocs` (tâche 3), `CarteAvecChiffres` (tâche 4).

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PlateauPortrait } from './PlateauPortrait'
import type { BoardProps } from '../Board'
import type { EmplacementAffiche, UniteAffichee, CleEmplacement } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'minion', imageUrl: '/s' }, attachees: [] }) as unknown as UniteAffichee

const props = (...emplacements: Array<[CleEmplacement, string[]]>): BoardProps =>
  ({
    world: { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] },
    playerId: 0,
    plateau: {
      emplacements: emplacements.map(([cle, noms]) => ({
        cle, titre: cle, groupes: [noms.map(unite)], nombreSurLaLigne: noms.length,
      })) as EmplacementAffiche[],
      nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0,
    },
  }) as unknown as BoardProps

describe('PlateauPortrait, les blocs du milieu', () => {
  it('dit qu aucun ennemi n est engage quand le bloc est vide', () => {
    render(<PlateauPortrait {...props()} />)
    expect(screen.getByText('Aucun ennemi engagé')).toBeInTheDocument()
  })

  it('montre les ennemis engages quand il y en a', () => {
    render(<PlateauPortrait {...props(['nemesis', ['Baron Zemo']])} />)
    expect(screen.getByText('Baron Zemo')).toBeInTheDocument()
    expect(screen.queryByText('Aucun ennemi engagé')).toBeNull()
  })

  it('montre le heros et ses allies', () => {
    render(<PlateauPortrait {...props(['terrain-soutien', ['Steve Rogers', 'Hope Summers']])} />)
    expect(screen.getByText('Steve Rogers')).toBeInTheDocument()
    expect(screen.getByText('Hope Summers')).toBeInTheDocument()
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/PlateauPortrait.test.tsx`
Attendu : ÉCHEC, « Aucun ennemi engagé » absent.

- [ ] **Étape 3 : implémenter les blocs**

Dans `PlateauPortrait.tsx`, ajouter après le bloc complot :

```tsx
      <section className="portrait-bloc portrait-engages">
        <h2 className="portrait-bloc-titre">{t('Engagés')}</h2>
        {engages.length === 0 ? (
          <p className="portrait-vide">{t('Aucun ennemi engagé')}</p>
        ) : (
          engages.map((unite) => (
            <CarteAvecChiffres
              key={unite.cle}
              carte={unite.carte}
              nom={unite.carte.name}
              chiffres={chiffresDe(unite.carte)}
            />
          ))
        )}
      </section>

      <section className="portrait-bloc portrait-heros">
        <h2 className="portrait-bloc-titre">{t('Ton héros')}</h2>
        {heros.map((unite) => (
          <CarteAvecChiffres
            key={unite.cle}
            carte={unite.carte}
            nom={unite.carte.name}
            chiffres={chiffresDe(unite.carte)}
          />
        ))}
      </section>
```

avec, en haut du fichier :

```tsx
/** Les stats d'une carte, dans la forme qu'attend CarteAvecChiffres. */
function chiffresDe(carte: ScanCardProps): Array<{ valeur: string; libelle: string }> {
  return (carte.stats ?? []).map((stat) => ({ valeur: String(stat.value), libelle: stat.label }))
}
```

Ajouter les libellés à `dico-en.ts` :

```ts
  'Aucun ennemi engagé': 'No enemies engaged',
  'Engagés': 'Engaged',
```

- [ ] **Étape 4 : vérifier**

`npm test -- src/board/mobile/PlateauPortrait.test.tsx` puis `npm test` entier.

- [ ] **Étape 5 : commit**

```bash
git add ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/PlateauPortrait.test.tsx ui-app/src/board/mobile/portrait.css ui-app/src/board/dico-en.ts
git commit -m "feat(portrait): les ennemis engages, le heros et ses allies"
```

---

### Tâche 7 : la main qui défile et la barre du bas

**Fichiers :**
- Créer : `ui-app/src/board/mobile/MainPortrait.tsx`
- Modifier : `ui-app/src/board/mobile/PlateauPortrait.tsx`, `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/MainPortrait.test.tsx`

**Interfaces :**
- Produit :
  ```ts
  export function MainPortrait({ unites, onOuvrir, onJouer }: {
    unites: UniteAffichee[]
    onOuvrir: (unite: UniteAffichee) => void
    onJouer?: (unite: UniteAffichee) => void
  }): ReactElement
  ```

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { MainPortrait } from './MainPortrait'
import type { UniteAffichee } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'event', imageUrl: '/s' }, attachees: [] }) as unknown as UniteAffichee

describe('MainPortrait', () => {
  it('rend une rangee qui defile, une carte par unite', () => {
    const { container } = render(
      <MainPortrait unites={[unite('Quinjet'), unite('Backflip')]} onOuvrir={() => {}} />
    )
    expect(container.querySelectorAll('.main-portrait .scan-card')).toHaveLength(2)
    expect(container.querySelector('.main-portrait')).toHaveClass('defile')
  })

  it('dit combien de cartes on a en main', () => {
    render(<MainPortrait unites={[unite('a'), unite('b'), unite('c')]} onOuvrir={() => {}} />)
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('en main')).toBeInTheDocument()
  })

  it('un tap ouvre la carte', () => {
    const onOuvrir = vi.fn()
    const { container } = render(<MainPortrait unites={[unite('Quinjet')]} onOuvrir={onOuvrir} />)
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onOuvrir).toHaveBeenCalledTimes(1)
  })

  it('main vide : on le dit au lieu de laisser un trou', () => {
    render(<MainPortrait unites={[]} onOuvrir={() => {}} />)
    expect(screen.getByText('Ta main est vide')).toBeInTheDocument()
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/MainPortrait.test.tsx`

- [ ] **Étape 3 : écrire le composant**

```tsx
// La main, en rangee qui defile horizontalement.
//
// Choix de l'utilisateur le 11/09/2026, contre l'eventail : les cartes gardent
// une taille LISIBLE et on fait glisser le doigt. C'est la seule zone du
// portrait ou les cartes se lisent a vue ; tout le reste de la table est en
// petit avec ses chiffres a cote.
import type { ReactElement } from 'react'
import { ScanCard } from '../../components/ScanCard'
import { t } from '../langue'
import type { UniteAffichee } from '../zones'

export function MainPortrait({
  unites,
  onOuvrir,
}: {
  unites: UniteAffichee[]
  onOuvrir: (unite: UniteAffichee) => void
}): ReactElement {
  if (unites.length === 0) {
    return <p className="portrait-vide main-portrait-vide">{t('Ta main est vide')}</p>
  }
  return (
    <div className="main-portrait-bloc">
      <div className="main-portrait defile">
        {unites.map((unite) => (
          <ScanCard
            {...unite.carte}
            key={unite.cle}
            highlight={false}
            onSelect={() => onOuvrir(unite)}
          />
        ))}
      </div>
      <span className="portrait-chiffre main-portrait-compte">
        <b>{unites.length}</b>
        <small>{t('en main')}</small>
      </span>
    </div>
  )
}
```

Ajouter à `portrait.css` :

```css
  .main-portrait-bloc {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
  }

  /* Elle DEFILE : c'est la seule zone ou les cartes gardent une taille lisible,
     et sept cartes ne tiennent pas dans 500 px. */
  .main-portrait.defile {
    display: flex;
    flex: 1;
    gap: 6px;
    overflow-x: auto;
    overscroll-behavior-x: contain;
    scroll-snap-type: x proximity;
    --card-w: 96px;
  }

  .main-portrait.defile > .scan-card {
    flex: 0 0 auto;
    scroll-snap-align: center;
  }
```

Et les libellés dans `dico-en.ts` :

```ts
  'Ta main est vide': 'Your hand is empty',
  'en main': 'in hand',
```

- [ ] **Étape 4 : brancher dans `PlateauPortrait`**

La main va dans la troisième rangée de la grille (`grid-template-rows: auto 1fr auto`), avec la barre du bas. Réutiliser `BarreBas` si sa signature convient ; sinon, poser une barre locale portant `Journal`, `Annuler`, `Fin du tour`, `Fin du tour` seul coloré, comme le plateau PC depuis le 11/09.

- [ ] **Étape 5 : vérifier puis commit**

```bash
npm test && npm run typecheck
git add ui-app/src/board/mobile/MainPortrait.tsx ui-app/src/board/mobile/MainPortrait.test.tsx ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/portrait.css ui-app/src/board/dico-en.ts
git commit -m "feat(portrait): la main qui defile, et la barre du bas"
```

---

### Tâche 8 : tap pour lire, re-tap pour fermer, appui long pour jouer

**Fichiers :**
- Créer : `ui-app/src/board/mobile/geste-carte.ts`
- Modifier : `ui-app/src/board/mobile/MainPortrait.tsx`, `ui-app/src/board/mobile/PlateauPortrait.tsx`
- Test : `ui-app/src/board/mobile/geste-carte.test.ts`

**Interfaces :**
- Consomme : `useAppuiLong(action: (() => void) | undefined): AppuiLong` (`./useAppuiLong`).
- Produit :
  ```ts
  export type GesteCarte = { ouverte: string | undefined; taper: (id: string) => void; fermer: () => void }
  export function prochaineOuverte(ouverte: string | undefined, tapee: string): string | undefined
  ```

- [ ] **Étape 1 : écrire le test qui échoue**

```ts
import { describe, expect, it } from 'vitest'
import { prochaineOuverte } from './geste-carte'

describe('prochaineOuverte : tap ouvre, re-tap ferme', () => {
  it('ouvre une carte quand rien n est ouvert', () => {
    expect(prochaineOuverte(undefined, 'quinjet')).toBe('quinjet')
  })

  it('FERME la carte quand on retape la meme', () => {
    expect(prochaineOuverte('quinjet', 'quinjet')).toBeUndefined()
  })

  it('passe a l autre carte quand on en tape une differente', () => {
    expect(prochaineOuverte('quinjet', 'backflip')).toBe('backflip')
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/geste-carte.test.ts`

- [ ] **Étape 3 : écrire le module**

```ts
// Le geste sur une carte, en portrait : TAP pour lire, RE-TAP pour fermer,
// APPUI LONG pour jouer.
//
// Choix de l'utilisateur le 11/09/2026. Le tap est reversible et n'engage
// rien : sur un telephone, une carte de 96 px se joue autrement du doigt qu'a
// la souris, et ouvrir pour lire doit rester gratuit. Le jeu, lui, demande une
// intention — d'ou l'appui long, que `useAppuiLong` porte deja.
//
// La bascule est isolee ici, pure, parce que c'est la seule regle qu'on peut
// se tromper sans qu'un test de composant ne le voie.

/** L'identifiant ouvert apres un tap sur `tapee`. */
export function prochaineOuverte(ouverte: string | undefined, tapee: string): string | undefined {
  return ouverte === tapee ? undefined : tapee
}
```

- [ ] **Étape 4 : brancher le geste**

Dans `MainPortrait`, remplacer `onSelect` par la paire tap / appui long :

```tsx
const appui = useAppuiLong(onJouer ? () => onJouer(unite) : undefined)
// `onSelect` reste le TAP ; l'appui long est capte par les gestionnaires de
// pointeur qu'`useAppuiLong` fournit, et il annule le tap quand il se declenche.
```

Suivre le contrat exact d'`AppuiLong` : lire `ui-app/src/board/mobile/useAppuiLong.ts` et poser les gestionnaires qu'il expose, sans en inventer.

- [ ] **Étape 5 : vérifier puis commit**

```bash
npm test && npm run typecheck
git add ui-app/src/board/mobile/geste-carte.ts ui-app/src/board/mobile/geste-carte.test.ts ui-app/src/board/mobile/MainPortrait.tsx ui-app/src/board/mobile/PlateauPortrait.tsx
git commit -m "feat(portrait): tap pour lire, re-tap pour fermer, appui long pour jouer"
```

---

### Tâche 9 : le panneau de décision et la scène du méchant, ancrés en bas

**Fichiers :**
- Modifier : `ui-app/src/board.tsx` (passer `bas` au plateau portrait), `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/PlateauPortrait.test.tsx`

**Interfaces :**
- Consomme : `BoardProps.bas` (déjà dans le contrat), `AssistantAction`, `DeroulePhase`.

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
it('loge le panneau de decision en bas de l ecran', () => {
  const { container } = render(
    <PlateauPortrait {...props()} bas={<button type="button">Jouer Quinjet</button>} />
  )
  const bas = container.querySelector('.portrait-bas')
  expect(bas).not.toBeNull()
  expect(bas?.textContent).toContain('Jouer Quinjet')
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/PlateauPortrait.test.tsx`

- [ ] **Étape 3 : rendre `bas`**

Dans `PlateauPortrait`, sous la main :

```tsx
      {props.bas ? <div className="portrait-bas">{props.bas}</div> : null}
```

Dans `portrait.css` :

```css
  /* Le panneau de decision et la scene du mechant vivent sur la MOITIE BASSE,
     au pouce, le plateau assombri au-dessus (demande de l'utilisateur,
     11/09/2026, calquee sur play.marvelsimulator.com). */
  .portrait-bas {
    max-height: 50dvh;
    overflow-y: auto;
    border-top: 2px solid var(--menace);
    background: rgba(20, 20, 20, 0.96);
  }

  /* La scene de la phase du mechant n'est plus un panneau flottant centre :
     en portrait elle se pose en bas, pleine largeur. */
  .plateau-portrait .deroule-phase {
    position: static;
    width: 100%;
    max-width: none;
    max-height: 50dvh;
    transform: none;
    border-radius: 0;
  }
```

- [ ] **Étape 4 : vérifier que `board.tsx` passe bien `bas` en mode mobile**

Lire `board.tsx` autour de `<RenduPartie` et confirmer que `bas` et `actionsPartie` sont transmis dans les deux modes. Si `bas` n'est passé qu'en `modeActions === 'detailed'`, le rendre inconditionnel pour le portrait.

- [ ] **Étape 5 : vérifier puis commit**

```bash
npm test && npm run typecheck
git add ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/PlateauPortrait.test.tsx ui-app/src/board/mobile/portrait.css ui-app/src/board.tsx
git commit -m "feat(portrait): le panneau de decision et la scene du mechant, ancres en bas"
```

---

### Tâche 10 : les onglets du multijoueur

**Fichiers :**
- Créer : `ui-app/src/board/mobile/OngletsJoueurs.tsx`
- Modifier : `ui-app/src/board/mobile/PlateauPortrait.tsx`, `ui-app/src/board/mobile/portrait.css`
- Test : `ui-app/src/board/mobile/OngletsJoueurs.test.tsx`

**Interfaces :**
- Consomme : `groupesParJoueur`, `ordreDAffichage`, `carteIdentite` (`./joueurs`).
- Produit :
  ```ts
  export function OngletsJoueurs({ joueurs, actif, choisir }: {
    joueurs: Array<{ id: number; nom: string }>
    actif: number
    choisir: (id: number) => void
  }): ReactElement | null
  ```

- [ ] **Étape 1 : écrire le test qui échoue**

```tsx
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { OngletsJoueurs } from './OngletsJoueurs'

describe('OngletsJoueurs', () => {
  it('ne montre RIEN en solo : un onglet unique est du bruit', () => {
    const { container } = render(
      <OngletsJoueurs joueurs={[{ id: 0, nom: 'Steve Rogers' }]} actif={0} choisir={() => {}} />
    )
    expect(container.firstChild).toBeNull()
  })

  it('un onglet par heros, celui qu on regarde est marque', () => {
    render(
      <OngletsJoueurs
        joueurs={[{ id: 0, nom: 'Steve Rogers' }, { id: 1, nom: 'Hulk' }]}
        actif={1}
        choisir={() => {}}
      />
    )
    expect(screen.getByRole('tab', { name: 'Hulk' })).toHaveAttribute('aria-selected', 'true')
    expect(screen.getByRole('tab', { name: 'Steve Rogers' })).toHaveAttribute('aria-selected', 'false')
  })

  it('taper un onglet change de joueur', () => {
    const choisir = vi.fn()
    render(
      <OngletsJoueurs
        joueurs={[{ id: 0, nom: 'Steve Rogers' }, { id: 1, nom: 'Hulk' }]}
        actif={0}
        choisir={choisir}
      />
    )
    fireEvent.click(screen.getByRole('tab', { name: 'Hulk' }))
    expect(choisir).toHaveBeenCalledWith(1)
  })
})
```

- [ ] **Étape 2 : regarder le test échouer**

`npm test -- src/board/mobile/OngletsJoueurs.test.tsx`

- [ ] **Étape 3 : écrire le composant**

```tsx
// Un onglet par heros, en coop.
//
// Choix de l'utilisateur le 11/09/2026 : sur un telephone, on ne tient pas
// quatre tables a la fois. On regarde la sienne, et on bascule du pouce pour
// voir celle d'un autre — mains comprises, le jeu est cooperatif et
// l'information ouverte aide a se coordonner.
//
// En solo, le composant se tait : un onglet unique serait une ligne de bruit
// en haut d'un ecran ou chaque pixel compte.
import type { ReactElement } from 'react'

export function OngletsJoueurs({
  joueurs,
  actif,
  choisir,
}: {
  joueurs: Array<{ id: number; nom: string }>
  actif: number
  choisir: (id: number) => void
}): ReactElement | null {
  if (joueurs.length < 2) return null
  return (
    <div className="portrait-onglets" role="tablist">
      {joueurs.map(({ id, nom }) => (
        <button
          type="button"
          role="tab"
          key={id}
          aria-selected={id === actif}
          className={`portrait-onglet${id === actif ? ' est-actif' : ''}`}
          onClick={() => choisir(id)}
        >
          {nom}
        </button>
      ))}
    </div>
  )
}
```

Dans `portrait.css` :

```css
  .portrait-onglets {
    display: flex;
    gap: 4px;
    padding: 4px 8px;
    overflow-x: auto;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  }

  .portrait-onglet {
    flex: 0 0 auto;
    min-height: 34px;
    padding: 0 12px;
    font: inherit;
    font-size: 0.78rem;
    font-weight: 800;
    color: #cbd5e1;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
  }

  .portrait-onglet.est-actif {
    color: var(--fond);
    background: var(--menace);
    border-color: var(--menace-clair);
  }
```

- [ ] **Étape 4 : brancher dans `PlateauPortrait`**

Un état local `joueurRegarde`, initialisé à `props.playerId`. Les blocs `engages` et `heros` se filtrent sur ce joueur via `emplacement.proprietaires` (déjà renseigné pour `terrain-soutien`, voir `zones.ts`). Le bandeau, le vilain, le complot et la rencontre sont communs et ne changent pas d'onglet.

- [ ] **Étape 5 : vérifier puis commit**

```bash
npm test && npm run typecheck
git add ui-app/src/board/mobile/OngletsJoueurs.tsx ui-app/src/board/mobile/OngletsJoueurs.test.tsx ui-app/src/board/mobile/PlateauPortrait.tsx ui-app/src/board/mobile/portrait.css
git commit -m "feat(portrait): un onglet par heros en coop"
```

---

### Tâche 11 : la vérification visuelle, et la livraison

**Fichiers :** aucun. C'est la recette.

- [ ] **Étape 1 : construire et installer en local**

```bash
cd ui-app && npm run build && npm run verifier-sortie
rsync -a --delete dist/ ../Fusion/marvel-lcg-src/public/app/
```

- [ ] **Étape 2 : lancer le moteur et ouvrir le plateau**

Le moteur tourne sur `127.0.0.1:2345` (`JOUER-SOLO.bat`, ou depuis WSL
`cd Fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 launcher_fast.py`).
Ouvrir `http://127.0.0.1:2345/app/board.html?mobile`.

- [ ] **Étape 3 : capturer à la taille d'un téléphone**

Le navigateur piloté passe par `cmd.exe` (voir la mémoire de session) :

```bash
CDT="C:\\Users\\arnau\\AppData\\Roaming\\npm\\chrome-devtools.cmd"
cd /mnt/c/Users/arnau && cmd.exe /c "$CDT resize_page <N> 500 844"
cmd.exe /c "$CDT take_screenshot <N> --filePath C:\\Users\\arnau\\Desktop\\Medida\\portrait.png --format png"
```

⚠ Une fenêtre Chrome ne descend pas sous 500 px de large : 500x844 est le plus étroit qu'on puisse mesurer.

- [ ] **Étape 4 : contrôler ce qui compte**

- la page NE DÉFILE PAS : `document.documentElement.scrollHeight === innerHeight` ;
- le bandeau et la barre du bas sont visibles sans geste ;
- aucun chiffre posé sur une illustration ;
- un tap ouvre une carte, un re-tap la ferme ;
- en paysage, « Remets ton téléphone droit ».

- [ ] **Étape 5 : montrer la capture, et ne rien déployer sans accord**

## Auto-revue du plan

**Couverture de la spec.** Orientation portrait seule → tâche 2. `PlateauPaysage` conservé sans être monté → tâche 2. Tablettes sur le plateau PC → tâche 1. Vraie carte en petit avec chiffres à côté → tâche 4 (`CarteAvecChiffres`), réutilisée en 5 et 6. Aucun défilement → tâche 2 (`overflow: hidden` sur la grille) et vérifié en tâche 11. Tap/re-tap/appui long → tâche 8. Main qui défile → tâche 7. Phase du méchant sur la moitié basse → tâche 9. Onglets multijoueur, tout visible → tâche 10. Ambiance gardée → aucune tâche, c'est le comportement actuel qu'on ne touche pas. Le point technique du petit côté → tâche 1.

**Cohérence des types.** `UniteAffichee`, `EmplacementAffiche`, `Plateau`, `CleEmplacement` viennent tous de `../zones` et gardent leurs noms. `CleBloc` et `BlocPortrait` sont définis en tâche 3 et consommés en 4, 6, 7, 10. `chiffresDe` (tâche 6) et `menaceDe` (tâche 5) vivent dans `PlateauPortrait.tsx`. `prochaineOuverte` (tâche 8) est pure et sans dépendance.

**Deux inconnues assumées, à lever en lisant le code plutôt qu'en devinant :** les libellés exacts des `stats` d'une carte (tâche 5, étape 4) et le contrat d'`AppuiLong` (tâche 8, étape 4). Les deux étapes le disent explicitement.
