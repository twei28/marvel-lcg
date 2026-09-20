# Plan d'exécution : le mode manuel, moitié plateau

> **Pour un agent d'exécution :** SOUS-SKILL REQUISE : utiliser
> `superpowers:subagent-driven-development` (recommandé) ou
> `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les
> étapes sont en cases à cocher (`- [ ]`).

**But :** rendre le mode manuel jouable à la souris et au clavier. Le plateau
se tait, le menu de triche devient le menu normal, et la table se manipule
comme sur Tabletop Simulator.

**Architecture :** tout ce qui est propre au mode vit dans
`ui-app/src/board/manuel/`, un dossier qu'on peut retirer d'un bloc. Le plateau
existant n'est touché que par des gardes `mode_manuel ? null : ...` et par le
branchement de deux objets de réglages déjà prévus par le code
(`ReglagesGlisser`, et la couche du menu).

**Pile technique :** React 19 + TypeScript 6 + Vitest (`ui-app`), écran de
préparation en JavaScript nu (`Fusion/marvel-lcg-src/public/js/prepare`).

**Spec :** `docs/superpowers/specs/2026-09-18-mode-manuel-design.md`

**Prérequis :** le plan `2026-09-18-mode-manuel-moteur.md` doit être terminé et
vert. Ce plan consomme `WorldDescriptor.mode_manuel`, `Puzzle.MoveTo`,
`Puzzle.Shuffle`, `Puzzle.Attach`, `Puzzle.Engage` et la route
`POST /manuel_undo`.

## Contraintes globales

- **TypeScript strict, zéro `any`.**
- **Aucun texte en dur** : tout passe par `t()` (`board/langue.ts`) et sa
  contrepartie anglaise (`board/dico-en.ts`). Une gate refuse le reste.
- **Une seule copie vivante du moteur** : `Fusion/marvel-lcg-src/`.
- **Les tests tournent avec `npm test` depuis `ui-app`** (`vitest run`).
- **`npm run typecheck` doit rester vert** à chaque commit.
- **Aucun déploiement**, à aucune étape. Le mot « déploie » vient de
  l'utilisateur, et de lui seul.
- **Si quelqu'un joue, prévenir avant tout redémarrage.**
- **Le mode manuel n'enregistre aucun haut fait**, comme le bac à sable.
  ⚠ Sans portée visible : la bannière des hauts faits est débranchée à la
  demande de l'utilisateur, plus rien ne les montre. Le filtre est gardé
  pour le jour où elle serait rallumée.

---

### Tâche 1 : le plateau sait qu'il est en mode manuel

**Fichiers :**
- Modifier : `ui-app/src/board/world.ts:343`
- Créer : `ui-app/src/board/manuel/mode.ts`
- Créer : `ui-app/src/board/manuel/mode.test.ts`
- Modifier : `Fusion/marvel-lcg-src/public/js/prepare/app.js:3883`
- Modifier : `Fusion/marvel-lcg-src/public/js/prepare/launcher.js:25`

**Interfaces :**
- Produit : `World.mode_manuel?: boolean` dans le type du plateau.
- Produit : `estModeManuel(world: World | undefined): boolean`.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/mode.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { estModeManuel } from './mode'
import type { World } from '../world'

describe('reconnaitre une partie manuelle', () => {
  it('vaut faux sans monde', () => {
    expect(estModeManuel(undefined)).toBe(false)
  })

  it('vaut faux en partie ordinaire', () => {
    expect(estModeManuel({} as World)).toBe(false)
  })

  it('vaut faux en bac a sable seul', () => {
    expect(estModeManuel({ mode_sandbox: true } as World)).toBe(false)
  })

  it('vaut vrai quand le moteur le dit', () => {
    expect(estModeManuel({ mode_manuel: true } as World)).toBe(true)
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm test -- src/board/manuel/mode.test.ts
```

Attendu : ROUGE, `Failed to resolve import './mode'`.

- [ ] **Étape 3 : écrire le module**

Créer `ui-app/src/board/manuel/mode.ts` :

```ts
// mode.ts — la reconnaissance du mode manuel, en un seul endroit.
//
// Le mode manuel N'EST PAS le bac à sable, même si les deux partagent le menu
// d'intervention : le bac à sable est une partie normale qu'on truque, le mode
// manuel est une table où le moteur ne joue plus. Les confondre ferait taire le
// plateau d'une partie qui se joue encore aux règles.
import type { World } from '../world'

export function estModeManuel(world: World | undefined): boolean {
  return world?.mode_manuel === true
}
```

Dans `ui-app/src/board/world.ts`, après le champ `mode_sandbox` :

```ts
  /**
   * Mode manuel. Posé par la règle `mode_manuel` du descripteur. Le moteur ne
   * conduit plus rien : le plateau masque tout ce qui parlait en son nom.
   */
  mode_manuel?: boolean
```

- [ ] **Étape 4 : relancer, voir VERT**

```bash
npm test -- src/board/manuel/mode.test.ts
```

Attendu : 4 tests verts.

- [ ] **Étape 5 : allumer le mode depuis l'écran de préparation**

Dans `Fusion/marvel-lcg-src/public/js/prepare/app.js`, juste avant le `return`
du bloc « Avancé », après la constante `v16` :

```js
    // Partie manuelle : combinable avec Solo, Coop locale et Campagne, donc une
    // CASE et non une tuile de mode. Le moteur pose la table puis se tait.
    const manuel = el("label", { class: "cj-chk" },
        el("input", {
            type: "checkbox",
            checked: state.modeManuel === true || undefined,
            onchange: (e) => { state.modeManuel = e.target.checked; },
        }),
        el("span", {}, t("Le moteur pose la table, puis ne joue plus")));
```

et, dans la liste des lignes du bloc, après `ligne(t("Règles v16"), v16, null)` :

```js
            ligne(t("Partie manuelle"), manuel,
                  t("Tu appliques toutes les règles toi-même")),
```

Dans `Fusion/marvel-lcg-src/public/js/prepare/launcher.js`, dans `buildRules`,
après la ligne `mode_sandbox` :

```js
    // Partie manuelle : apres la mise en place, le moteur ne conduit plus et ne
    // declenche plus rien. Comme les autres modes, le drapeau passe par `rules`
    // et survit donc au chargement d'une sauvegarde.
    if (state.modeManuel === true) rules.push("mode_manuel");
```

- [ ] **Étape 6 : vérifier que rien n'est cassé**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm run typecheck && npm test
```

Attendu : typecheck vert, toute la batterie verte.

- [ ] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/world.ts ui-app/src/board/manuel/ \
        Fusion/marvel-lcg-src/public/js/prepare/app.js \
        Fusion/marvel-lcg-src/public/js/prepare/launcher.js
git commit -m "feat(manuel): le plateau reconnait le mode, la preparation l'allume"
```

---

### Tâche 2 : le plateau se tait

**Fichiers :**
- Modifier : `ui-app/src/board.tsx` (lignes 1312, 1319, 3044, 3102, 3180, 3185,
  3262, 3330, 3656)
- Modifier : `ui-app/src/board/moteur.ts:986`
- Modifier : `ui-app/src/board/rapport-bug.ts:113` et `:304`
- Créer : `ui-app/src/board/manuel/plateau-muet.test.tsx`

**Interfaces :**
- Consomme : `estModeManuel` (tâche 1).
- Produit : rien de nouveau. Neuf gardes, un filtre de hauts faits, un champ de
  rapport.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/plateau-muet.test.tsx` :

```tsx
// Le plateau manuel ne montre RIEN de ce que le moteur disait.
//
// On vise les classes CSS plutot que les composants : c'est ce que le joueur
// voit, et ca ne bouge pas quand un composant est renomme.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { PagePartie } from '../PagePartie'
import { mondeDeTest } from './fixture-monde'

describe('le plateau manuel se tait', () => {
  it('ne montre pas le bandeau de phase', () => {
    const { container } = render(<PagePartie monde={mondeDeTest({ mode_manuel: true })} />)
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('ne montre pas le deroule de phase', () => {
    const { container } = render(<PagePartie monde={mondeDeTest({ mode_manuel: true })} />)
    expect(container.querySelector('.deroule-phase')).toBeNull()
  })

  it('montre encore ces reperes en partie ordinaire', () => {
    const { container } = render(<PagePartie monde={mondeDeTest({})} />)
    expect(container.querySelector('.deroule-phase')).not.toBeNull()
  })
})
```

⚠ `mondeDeTest` et le montage exact de `PagePartie` sont à calquer sur
`ui-app/src/board/PagePartie.test.tsx`, qui monte déjà cette page avec un monde
factice. Créer `ui-app/src/board/manuel/fixture-monde.ts` qui réexporte ce
monde factice en acceptant un fragment à fusionner, plutôt que d'en réécrire un
second.

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm test -- src/board/manuel/plateau-muet.test.tsx
```

Attendu : ROUGE, le bandeau et le déroulé sont présents en mode manuel.

- [ ] **Étape 3 : poser les gardes**

Dans `ui-app/src/board.tsx`, près du calcul de `triche` (ligne 2040) :

```tsx
  // Le mode manuel : tout ce qui parlait au nom du moteur disparait. Une garde
  // par endroit, greppable et retirable d'un bloc.
  const manuel = estModeManuel(etat.monde)
```

et, à chacune des neuf lignes listées ci-dessus, envelopper l'élément :

```tsx
      {manuel ? null : (
        <BandeauPhase ... />
      )}
```

Les neuf éléments concernés sont `BandeauPhase` (deux fois), `DeroulePhase`
(deux fois), `DemandeCentrale` (deux fois), `AssistantAction`,
`RecapPhaseMechant` et `BarreAction`.

- [ ] **Étape 4 : couper les hauts faits et marquer le rapport de bug**

Dans `ui-app/src/board/moteur.ts`, remplacer

```ts
    if (this.etat.monde?.mode_sandbox === true) return
```

par

```ts
    // Ni en bac a sable, ni en manuel : un haut fait obtenu sur une table ou
    // le moteur ne verifie rien ne vaut pas davantage qu'un haut fait truque.
    if (this.etat.monde?.mode_sandbox === true) return
    if (this.etat.monde?.mode_manuel === true) return
```

Dans `ui-app/src/board/rapport-bug.ts`, ajouter au type (ligne 113) :

```ts
  manuel: boolean
```

le remplir (ligne 304) :

```ts
      manuel: monde.mode_manuel === true,
```

et l'afficher dans la même liste que `'bac à sable'` (ligne 402) :

```ts
    c.manuel ? 'mode manuel' : undefined,
```

- [ ] **Étape 5 : montrer toutes les mains**

Le plateau ne montre aujourd'hui que la main du joueur actif. En manuel il n'y
a qu'un opérateur pour plusieurs héros : il lui faut les voir toutes. `Board`
accepte déjà `mainVisibleForcee` (`ui-app/src/board/Board.tsx:794`). Dans
`ui-app/src/board.tsx`, le passer à vrai en mode manuel :

```tsx
        mainVisibleForcee={manuel || mainVisibleForcee}
```

Et ajouter le cas au test de la tâche :

```tsx
  it('montre la main de chaque heros', () => {
    const { container } = render(<PagePartie monde={mondeDeTest({ mode_manuel: true })} />)
    expect(container.querySelectorAll('[data-pile="main"]').length).toBeGreaterThan(0)
  })
```

- [ ] **Étape 6 : relancer, voir VERT**

```bash
npm test -- src/board/manuel/plateau-muet.test.tsx src/board/rapport-bug.test.ts
npm run typecheck
```

Attendu : vert partout.

- [ ] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board.tsx ui-app/src/board/moteur.ts \
        ui-app/src/board/rapport-bug.ts ui-app/src/board/manuel/
git commit -m "feat(manuel): le plateau se tait, et ne compte aucun haut fait"
```

---

### Tâche 3 : le menu de triche devient le menu normal

**Fichiers :**
- Modifier : `ui-app/src/board/CoucheTriche.tsx:87` et `:172`
- Modifier : `ui-app/src/board/MenuTriche.tsx`
- Modifier : `ui-app/src/board/triche.ts`
- Créer : `ui-app/src/board/manuel/menu-manuel.test.tsx`

**Interfaces :**
- Consomme : `estModeManuel` (tâche 1).
- Produit : `triche.deplacerVers(id: number, zone: string, position?: 'Top' | 'Bottom')`,
  `triche.melanger(zone: string)`, `triche.attacher(id: number, cible: number)`,
  `triche.engager(id: number)`.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/menu-manuel.test.tsx` :

```tsx
import { describe, expect, it, vi, beforeEach } from 'vitest'
import * as triche from '../triche'

describe('les gestes manuels parlent au moteur', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('deplace une carte vers une pile nommee', async () => {
    await triche.deplacerVers(42, 'EncounterDeck')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
    }))
  })

  it('depose une carte sous une pile quand on le demande', async () => {
    await triche.deplacerVers(42, 'EncounterDeck', 'Bottom')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Bottom')"] }),
    }))
  })

  it('melange une pile', async () => {
    await triche.melanger('PlayerDeck')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('PlayerDeck')"] }),
    }))
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
npm test -- src/board/manuel/menu-manuel.test.tsx
```

Attendu : ROUGE, `triche.deplacerVers is not a function`.

- [ ] **Étape 3 : ajouter les quatre gestes au canal**

Dans `ui-app/src/board/triche.ts`, à la fin du fichier :

```ts
// --- Les gestes du mode manuel ---------------------------------------------

/** Envoie une carte dans n'importe quelle pile, sans aucune vérification. */
export const deplacerVers = (
  id: number,
  zone: string,
  position: 'Top' | 'Bottom' = 'Top'
) => envoyer([`Puzzle.MoveTo(${id}, ${texte(zone)}, ${texte(position)})`])

export const melanger = (zone: string) => envoyer([`Puzzle.Shuffle(${texte(zone)})`])

export const attacher = (id: number, cible: number) =>
  envoyer([`Puzzle.Attach(${id}, ${cible})`])

export const engager = (id: number) => envoyer([`Puzzle.Engage(${id})`])
```

- [ ] **Étape 4 : ouvrir le menu en mode manuel, sans bandeau de triche**

Dans `ui-app/src/board/CoucheTriche.tsx`, remplacer

```ts
  const actif = world?.mode_sandbox === true
```

par

```ts
  // Le menu s'ouvre dans les DEUX modes : bac à sable (on truque une partie qui
  // se joue aux règles) et manuel (il n'y a plus que lui pour jouer).
  const actif = world?.mode_sandbox === true || world?.mode_manuel === true
```

et, dans `CoucheTriche`, remplacer le bandeau par :

```tsx
      {/* Le bandeau ne s'affiche qu'en bac à sable : il dit qu'une partie
          normale a été truquée. En manuel, il n'y a rien à dénoncer, et la
          spec demande un plateau nu. */}
      {manuel ? null : (
        <div className="bandeau-triche" role="status">
          <span className="bandeau-triche-marque">{t('Bac à sable')}</span>
          <span className="bandeau-triche-aide">
            {t('Clic droit sur une carte ou une pile')}
          </span>
        </div>
      )}
```

`manuel` est passé en accessoire depuis `useTriche`, qui le calcule avec
`estModeManuel(world)`.

- [ ] **Étape 5 : ajouter les entrées au menu**

Dans `ui-app/src/board/MenuTriche.tsx`, ajouter un sous-menu « Déplacer vers »
listant les piles atteignables, et une entrée « Mélanger » sur les cibles qui
sont des piles. Les noms de piles sont ceux de `DeckType` côté moteur, traduits
à l'affichage :

```tsx
/** Les piles atteignables, nom moteur puis libellé affiché. */
export const PILES_MANUELLES: ReadonlyArray<readonly [string, string]> = [
  ['HandsArea', t('Main')],
  ['PlayerDeck', t('Deck du héros')],
  ['DiscardPile', t('Pile de défausse')],
  ['AlliesArea', t('Alliés')],
  ['SupportsArea', t('Soutiens')],
  ['EngagedEnemiesArea', t('Ennemis engagés')],
  ['EncounterDeck', t('Deck Rencontre')],
  ['EncounterDiscardPile', t('Défausse Rencontre')],
  ['SideSchemesArea', t('Manigances annexes')],
  ['VillainArea', t('Zone du vilain')],
  ['RemovedArea', t('Retirées de la partie')],
  ['VictoryDisplay', t('Pile de victoire')],
  ['AsideDeck', t('Cartes écartées')],
]
```

Chaque entrée appelle `triche.deplacerVers(cible.id, nomMoteur)` puis
`onIntervention(...)` pour le journal, exactement comme les entrées existantes.

- [ ] **Étape 6 : traduire**

Ajouter dans `ui-app/src/board/dico-en.ts` la contrepartie anglaise de chaque
texte nouveau : `Déplacer vers`, `Mélanger`, `Sous la pile`, `Alliés`,
`Soutiens`, `Ennemis engagés`, `Manigances annexes`, `Zone du vilain`,
`Cartes écartées`, `Le moteur pose la table, puis ne joue plus`,
`Partie manuelle`, `Tu appliques toutes les règles toi-même`.

- [ ] **Étape 7 : relancer, voir VERT**

```bash
npm test && npm run typecheck
```

Attendu : vert partout, gate des textes en dur comprise.

- [ ] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/triche.ts ui-app/src/board/CoucheTriche.tsx \
        ui-app/src/board/MenuTriche.tsx ui-app/src/board/dico-en.ts \
        ui-app/src/board/manuel/
git commit -m "feat(manuel): le menu de triche devient le menu normal"
```

---

### Tâche 4 : les raccourcis clavier

**Fichiers :**
- Créer : `ui-app/src/board/manuel/clavier.ts`
- Créer : `ui-app/src/board/manuel/clavier.test.ts`
- Modifier : `ui-app/src/board/CoucheTriche.tsx`

**Interfaces :**
- Consomme : les gestes de `triche.ts` (tâche 3).
- Produit : `interpreterTouche(touche: Touche, cible: CibleClavier): GesteClavier | undefined`,
  fonction PURE, testée sans DOM.

```ts
export type Touche = { cle: string; majuscule: boolean }
export type CibleClavier =
  | { genre: 'carte'; id: number; jetonNaturel: 'degats' | 'menace' | 'aucun' }
  | { genre: 'pile'; zone: string }
export type GesteClavier =
  | { geste: 'retourner'; id: number }
  | { geste: 'incliner'; id: number }
  | { geste: 'melanger'; zone: string }
  | { geste: 'piocher'; zone: string; nombre: number }
  | { geste: 'jetons'; id: number; nature: 'degats' | 'menace'; nombre: number }
```

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/clavier.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import { interpreterTouche } from './clavier'

const VILAIN = { genre: 'carte', id: 7, jetonNaturel: 'degats' } as const
const MANIGANCE = { genre: 'carte', id: 9, jetonNaturel: 'menace' } as const
const DECK = { genre: 'pile', zone: 'PlayerDeck' } as const

describe('les touches du mode manuel', () => {
  it('F retourne la carte survolee', () => {
    expect(interpreterTouche({ cle: 'f', majuscule: false }, VILAIN))
      .toEqual({ geste: 'retourner', id: 7 })
  })

  it('Q incline la carte survolee', () => {
    expect(interpreterTouche({ cle: 'q', majuscule: false }, VILAIN))
      .toEqual({ geste: 'incliner', id: 7 })
  })

  it('R melange la pile survolee', () => {
    expect(interpreterTouche({ cle: 'r', majuscule: false }, DECK))
      .toEqual({ geste: 'melanger', zone: 'PlayerDeck' })
  })

  it('R ne melange pas une carte', () => {
    expect(interpreterTouche({ cle: 'r', majuscule: false }, VILAIN)).toBeUndefined()
  })

  it('un chiffre sur une pile prend ce nombre de cartes', () => {
    expect(interpreterTouche({ cle: '5', majuscule: false }, DECK))
      .toEqual({ geste: 'piocher', zone: 'PlayerDeck', nombre: 5 })
  })

  it('un chiffre sur un personnage pose des degats', () => {
    expect(interpreterTouche({ cle: '3', majuscule: false }, VILAIN))
      .toEqual({ geste: 'jetons', id: 7, nature: 'degats', nombre: 3 })
  })

  it('un chiffre sur une manigance pose de la menace', () => {
    expect(interpreterTouche({ cle: '3', majuscule: false }, MANIGANCE))
      .toEqual({ geste: 'jetons', id: 9, nature: 'menace', nombre: 3 })
  })

  it('Maj plus chiffre retire autant', () => {
    expect(interpreterTouche({ cle: '3', majuscule: true }, VILAIN))
      .toEqual({ geste: 'jetons', id: 7, nature: 'degats', nombre: -3 })
  })

  it('ne devine pas le jeton d une carte qui n en a pas', () => {
    const evenement = { genre: 'carte', id: 4, jetonNaturel: 'aucun' } as const
    expect(interpreterTouche({ cle: '3', majuscule: false }, evenement)).toBeUndefined()
  })

  it('ignore une touche inconnue', () => {
    expect(interpreterTouche({ cle: 'z', majuscule: false }, VILAIN)).toBeUndefined()
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
npm test -- src/board/manuel/clavier.test.ts
```

Attendu : ROUGE, module introuvable.

- [ ] **Étape 3 : écrire l'interprète**

Créer `ui-app/src/board/manuel/clavier.ts` :

```ts
// clavier.ts — ce que veut dire une touche, quand on survole quelque chose.
//
// Calqué sur Tabletop Simulator : F retourne, R mélange, Q pivote, un chiffre
// agit sur ce qu'on survole. Fonction PURE : elle ne touche ni au DOM ni au
// réseau, elle dit seulement quel geste la touche demande. Le branchement vit
// dans CoucheTriche, et se teste ailleurs.
//
// ⚠ ON NE DEVINE PAS le jeton d'une carte qui n'en a pas de naturel : mieux
// vaut ne rien poser que poser la mauvaise chose sur une carte qu'on ne
// relira pas. Le clic droit, lui, nomme chaque jeton.

export type Touche = { cle: string; majuscule: boolean }

export type CibleClavier =
  | { genre: 'carte'; id: number; jetonNaturel: 'degats' | 'menace' | 'aucun' }
  | { genre: 'pile'; zone: string }

export type GesteClavier =
  | { geste: 'retourner'; id: number }
  | { geste: 'incliner'; id: number }
  | { geste: 'melanger'; zone: string }
  | { geste: 'piocher'; zone: string; nombre: number }
  | { geste: 'jetons'; id: number; nature: 'degats' | 'menace'; nombre: number }

export function interpreterTouche(
  touche: Touche,
  cible: CibleClavier
): GesteClavier | undefined {
  const cle = touche.cle.toLowerCase()

  if (cle === 'f' && cible.genre === 'carte') return { geste: 'retourner', id: cible.id }
  if (cle === 'q' && cible.genre === 'carte') return { geste: 'incliner', id: cible.id }
  if (cle === 'r' && cible.genre === 'pile') return { geste: 'melanger', zone: cible.zone }

  const chiffre = /^[1-9]$/.test(cle) ? Number(cle) : undefined
  if (chiffre === undefined) return undefined

  if (cible.genre === 'pile') {
    return { geste: 'piocher', zone: cible.zone, nombre: chiffre }
  }
  if (cible.jetonNaturel === 'aucun') return undefined
  return {
    geste: 'jetons',
    id: cible.id,
    nature: cible.jetonNaturel,
    nombre: touche.majuscule ? -chiffre : chiffre,
  }
}
```

- [ ] **Étape 4 : relancer, voir VERT**

```bash
npm test -- src/board/manuel/clavier.test.ts
```

Attendu : 10 tests verts.

- [ ] **Étape 5 : brancher le clavier**

Dans `ui-app/src/board/CoucheTriche.tsx`, dans `useTriche`, ajouter une écoute
`keydown` au niveau du document, active uniquement en mode manuel, qui résout
la cible sous le pointeur (le même `closest('[data-card-id]')` que le clic
droit, et `[data-pile]` pour les piles), appelle `interpreterTouche`, puis
envoie le geste correspondant :

```tsx
  useEffect(() => {
    if (!manuel) return
    const surTouche = (evenement: KeyboardEvent) => {
      const cible = cibleSousLePointeur()
      if (!cible) return
      const geste = interpreterTouche(
        { cle: evenement.key, majuscule: evenement.shiftKey },
        cible
      )
      if (!geste) return
      evenement.preventDefault()
      void executer(geste)
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [manuel, executer])
```

`executer` traduit chaque geste en appel de `triche.ts` : `retourner`,
`incliner`, `melanger`, `deplacerVers` en boucle pour `piocher`, `blesser` ou
`poserMenace` pour `jetons`, et note chaque geste dans le journal.

`cibleSousLePointeur` suit la position du pointeur via un écouteur
`pointermove` au niveau du document, et rend `undefined` quand rien n'est
survolé.

- [ ] **Étape 6 : Alt agrandit tout de suite**

Le plateau ouvre déjà un aperçu au survol, après un délai (`apercuId`,
`ui-app/src/board/Board.tsx:852`). Sur Tabletop Simulator, Alt l'ouvre sans
attendre. Dans `Board.tsx`, ouvrir l'aperçu de la carte pointée dès que Alt est
enfoncée, et le refermer au relâchement :

```tsx
  // Alt : l'apercu tout de suite, sans le delai du survol. Convention Tabletop
  // Simulator, et le seul raccourci qui ne change pas l'etat de la partie.
  useEffect(() => {
    const surAlt = (evenement: KeyboardEvent) => {
      if (evenement.key !== 'Alt') return
      if (evenement.type === 'keydown') setApercuId(pointee.current)
      else setApercuId(null)
    }
    document.addEventListener('keydown', surAlt)
    document.addEventListener('keyup', surAlt)
    return () => {
      document.removeEventListener('keydown', surAlt)
      document.removeEventListener('keyup', surAlt)
    }
  }, [])
```

- [ ] **Étape 7 : vérifier**

```bash
npm test && npm run typecheck
```

Attendu : vert partout.

- [ ] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manuel/ ui-app/src/board/CoucheTriche.tsx \
        ui-app/src/board/Board.tsx
git commit -m "feat(manuel): les raccourcis clavier, calques sur Tabletop Simulator"
```

---

### Tâche 5 : le glisser-déposer libre

**Fichiers :**
- Créer : `ui-app/src/board/manuel/glisser-manuel.ts`
- Créer : `ui-app/src/board/manuel/glisser-manuel.test.ts`
- Modifier : `ui-app/src/board/zones.ts` (marquer les piles)
- Modifier : `ui-app/src/board/Board.tsx:383` (poser `data-pile`)
- Modifier : `ui-app/src/board.tsx` (choisir les réglages de glisser)

**Interfaces :**
- Consomme : `deplacerVers` (tâche 3), le type `ReglagesGlisser`
  (`ui-app/src/board/Board.tsx:776`), `CibleSurvolee`
  (`ui-app/src/board/glisser/useGlisser.ts:23`).
- Produit : `reglagesGlisserManuel(noter: (libelle: string) => void): ReglagesGlisser`.
- Produit : `PILE_PAR_ZONE: Record<string, string>`, la correspondance entre la
  clé de pile dessinée par le plateau et le nom de pile du moteur.

⚠ **Le plateau ne nomme aujourd'hui que onze emplacements**
(`CleEmplacement`, `ui-app/src/board/zones.ts:88`), trop gros pour viser une
pile précise : `piles-joueur` couvre le deck ET la défausse. Les groupes, eux,
portent déjà une clé fine (`deck`, `defausse`, `encounter-deck`,
`encounter-discard`, `victoire`, `retirees`, `nemesis`, `set-aside-scenario`,
`deck-special`). Cette tâche pose donc un attribut `data-pile` sur chaque
groupe, à côté du `data-zone` existant sur l'emplacement.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/glisser-manuel.test.ts` :

```ts
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { reglagesGlisserManuel, PILE_PAR_ZONE } from './glisser-manuel'

describe('le glisser du mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('souleve n importe quelle carte', () => {
    const reglages = reglagesGlisserManuel(() => {})
    expect(reglages.estSource(1)).toBe(true)
    expect(reglages.estSource(999)).toBe(true)
  })

  it('n allume aucune cible : tout est permis, rien n est suggere', () => {
    const reglages = reglagesGlisserManuel(() => {})
    expect(reglages.ciblesLegales(1).size).toBe(0)
  })

  it('accepte toutes les piles connues', () => {
    const reglages = reglagesGlisserManuel(() => {})
    expect(reglages.zonesLegales(1).has('deck')).toBe(true)
    expect(reglages.zonesLegales(1).has('encounter-deck')).toBe(true)
  })

  it('traduit la pile du plateau en pile du moteur', () => {
    expect(PILE_PAR_ZONE['encounter-deck']).toBe('EncounterDeck')
    expect(PILE_PAR_ZONE['defausse']).toBe('DiscardPile')
  })

  it('envoie le deplacement au lacher', () => {
    const reglages = reglagesGlisserManuel(() => {})
    expect(reglages.onDepot(42, { zone: 'encounter-deck' })).toBeUndefined()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
    }))
  })

  it('refuse poliment un lacher dans le vide', () => {
    const reglages = reglagesGlisserManuel(() => {})
    expect(reglages.onDepot(42, {})).toBe('Lâche la carte sur une pile')
  })

  it('depose sous la pile quand Maj est enfoncee', () => {
    const reglages = reglagesGlisserManuel(() => {}, () => true)
    reglages.onDepot(42, { zone: 'encounter-deck' })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Bottom')"] }),
    }))
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
npm test -- src/board/manuel/glisser-manuel.test.ts
```

Attendu : ROUGE, module introuvable.

- [ ] **Étape 3 : écrire les réglages**

Créer `ui-app/src/board/manuel/glisser-manuel.ts` :

```ts
// glisser-manuel.ts — glisser n'importe quelle carte vers n'importe quelle pile.
//
// Même forme que les réglages du glisser ordinaire (`ReglagesGlisser`), et
// c'est tout l'intérêt : le plateau ne change pas, seule la politique change.
// Ici il n'y a aucune politique : tout se soulève, tout s'accueille, rien ne
// s'allume. Une cible mise en valeur voudrait dire « c'est ici qu'il faut
// poser », et le mode manuel ne sait rien de ce qu'il faut.
import type { ReglagesGlisser } from '../Board'
import type { CibleSurvolee } from '../glisser/useGlisser'
import { t } from '../langue'
import { deplacerVers } from '../triche'

/** La pile dessinée par le plateau, et son nom côté moteur. */
export const PILE_PAR_ZONE: Record<string, string> = {
  'main': 'HandsArea',
  'deck': 'PlayerDeck',
  'defausse': 'DiscardPile',
  'deck-special': 'AdditionalDeck',
  'reserve': 'ReserveArea',
  'nemesis': 'AsideDeck',
  'set-aside-scenario': 'AsideDeck',
  'encounter-deck': 'EncounterDeck',
  'encounter-discard': 'EncounterDiscardPile',
  'victoire': 'VictoryDisplay',
  'retirees': 'RemovedArea',
  'terrain-combat': 'EngagedEnemiesArea',
  'terrain-soutien': 'SupportsArea',
  'complots-secondaires': 'SideSchemesArea',
  'complot-principal': 'MainSchemesArea',
}

export function reglagesGlisserManuel(
  noter: (libelle: string) => void,
  /**
   * Maj enfoncee au moment du lacher : la carte va SOUS la pile. On le demande
   * a l'appelant plutot que de lire un evenement, pour que la fonction reste
   * testable sans DOM.
   */
  sousLaPile: () => boolean = () => false
): ReglagesGlisser {
  return {
    estSource: () => true,
    ciblesLegales: () => new Set<number>(),
    zonesLegales: () => new Set(Object.keys(PILE_PAR_ZONE)),
    libelle: (_source: number, cible: CibleSurvolee) => {
      const pile = cible.zone ? PILE_PAR_ZONE[cible.zone] : undefined
      return pile ? t('Déplacer ici') : undefined
    },
    onDepot: (sourceId: number, cible: CibleSurvolee) => {
      const pile = cible.zone ? PILE_PAR_ZONE[cible.zone] : undefined
      if (!pile) return t('Lâche la carte sur une pile')
      void deplacerVers(sourceId, pile, sousLaPile() ? 'Bottom' : 'Top').then((reussi) => {
        noter(`${t('Déplacée')} → ${pile}${reussi ? '' : ` (${t('refusé')})`}`)
      })
      return undefined
    },
  }
}
```

- [ ] **Étape 4 : poser `data-pile` sur les groupes dessinés**

Dans `ui-app/src/board/Board.tsx`, à l'endroit où chaque groupe d'un
emplacement est rendu (juste sous le `data-zone` de la ligne 387), ajouter :

```tsx
      // La pile PRECISE, pour le mode manuel : `data-zone` ne distingue pas le
      // deck de sa défausse, qui partagent un emplacement.
      data-pile={groupe.cle}
```

et faire descendre `cle` depuis `zones.ts` jusqu'au groupe rendu, en ajoutant
le champ au type `GroupeDePile` s'il n'y est pas déjà présent à ce niveau.

Dans `ui-app/src/board/glisser/useGlisser.ts`, dans `cibleSousLePoint`, viser
la pile avant l'emplacement :

```ts
  const pile = sous.closest<HTMLElement>('[data-pile]')?.dataset.pile
  const zone = pile || sous.closest<HTMLElement>('[data-zone]')?.dataset.zone
```

- [ ] **Étape 5 : brancher les réglages manuels**

Dans `ui-app/src/board.tsx`, là où la prop `glisser` est construite, choisir
selon le mode :

```tsx
  // Maj est lue au moment du lacher : un drapeau tenu a jour par deux ecoutes
  // clavier, plutot qu'un evenement qui n'arrive pas jusqu'ici.
  const majEnfoncee = useRef(false)
  useEffect(() => {
    const suivre = (e: KeyboardEvent) => { majEnfoncee.current = e.shiftKey }
    document.addEventListener('keydown', suivre)
    document.addEventListener('keyup', suivre)
    return () => {
      document.removeEventListener('keydown', suivre)
      document.removeEventListener('keyup', suivre)
    }
  }, [])

  const reglagesGlisser = manuel
    ? reglagesGlisserManuel(historique.ajouterTriche, () => majEnfoncee.current)
    : reglagesGlisserOrdinaire
```

- [ ] **Étape 6 : vérifier**

```bash
npm test && npm run typecheck
```

Attendu : vert partout, y compris `src/board/glisser/cibles.test.ts` et
`geste.test.tsx`, qui ne doivent pas bouger.

- [ ] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manuel/ ui-app/src/board/Board.tsx \
        ui-app/src/board/zones.ts ui-app/src/board/glisser/useGlisser.ts \
        ui-app/src/board.tsx
git commit -m "feat(manuel): glisser n'importe quelle carte vers n'importe quelle pile"
```

---

### Tâche 6 : la recherche catalogue et l'annulation

**Fichiers :**
- Créer : `ui-app/src/board/manuel/CatalogueManuel.tsx`
- Créer : `ui-app/src/board/manuel/CatalogueManuel.test.tsx`
- Modifier : `ui-app/src/board/triche.ts`
- Modifier : `ui-app/src/board/CoucheTriche.tsx`

**Interfaces :**
- Consomme : `envoyer` (`triche.ts`), la route `POST /manuel_undo` (plan
  moteur, tâche 6).
- Produit : `triche.creerCarte(cardId: string)` et `triche.annulerDernierGeste()`.
- Produit : `<CatalogueManuel catalogue={...} onFermer={...} onPoser={...} />`.
- Produit : `Catalogue.chercherParNom(fragment, limite?)`.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/CatalogueManuel.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { CatalogueManuel } from './CatalogueManuel'
import { catalogueVide } from '../catalogue'

const CARTES = [
  { card_id: '01001a', name: 'Spider-Man' },
  { card_id: '01094', name: 'Rhino' },
]

const catalogue = {
  ...catalogueVide,
  chercherParNom: (fragment: string) =>
    fragment.length < 2
      ? []
      : CARTES.filter((c) => c.name.toLowerCase().includes(fragment.toLowerCase())),
}

describe('la recherche dans le catalogue', () => {
  it('ne montre rien tant qu on n a pas cherche', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    expect(screen.queryByText('Rhino')).toBeNull()
  })

  it('ne cherche pas sur une seule lettre', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'r' } })
    expect(screen.queryByText('Rhino')).toBeNull()
  })

  it('montre les cartes qui correspondent', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'rhi' } })
    expect(screen.getByText('Rhino')).toBeTruthy()
  })

  it('pose la carte choisie', () => {
    const poser = vi.fn()
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={poser} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'rhi' } })
    fireEvent.click(screen.getByText('Rhino'))
    expect(poser).toHaveBeenCalledWith('01094')
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
npm test -- src/board/manuel/CatalogueManuel.test.tsx
```

Attendu : ROUGE, module introuvable.

- [ ] **Étape 3 : écrire le catalogue et les deux gestes**

Dans `ui-app/src/board/triche.ts`, à la fin :

```ts
/** Fait apparaître sur la table une carte qui n'était pas dans la partie. */
export const creerCarte = (cardId: string) =>
  envoyer([`Puzzle.PutIntoPlay(${texte(cardId)})`])

/** Ctrl+Z : retire le dernier geste et rejoue la partie sans lui. */
export async function annulerDernierGeste(): Promise<boolean> {
  try {
    const reponse = await fetch('/manuel_undo', { method: 'POST' })
    return reponse.ok
  } catch {
    return false
  }
}
```

Le catalogue du plateau (`ui-app/src/board/catalogue.ts`) ne sait aujourd'hui
que répondre à un identifiant. Lui ajouter une recherche par nom, dans le type
`Catalogue`, dans `catalogueVide` et dans `construire` :

```ts
  /**
   * Les cartes dont le nom contient ce fragment, au plus `limite`. Sert au mode
   * manuel, seul endroit où l'on cherche une carte qui n'est pas dans la partie.
   */
  chercherParNom(fragment: string, limite?: number): Array<{ card_id: string; name: string }>
```

```ts
  // dans `catalogueVide`
  chercherParNom: () => [],
```

```ts
  // dans `construire`, sur l'index déjà bâti par la fonction
  chercherParNom: (fragment, limite = 40) => {
    const cherche = fragment.trim().toLowerCase()
    if (cherche.length < 2) return []
    const trouves: Array<{ card_id: string; name: string }> = []
    for (const [card_id, carte] of index) {
      if (!carte.name?.toLowerCase().includes(cherche)) continue
      trouves.push({ card_id, name: carte.name })
      if (trouves.length >= limite) break
    }
    return trouves
  },
```

Écrire ensuite `CatalogueManuel.tsx` : un champ `role="searchbox"`, un appel à
`chercherParNom` à chaque frappe, une liste de résultats cliquables, et
`onPoser(card_id)` au clic. La recherche ne part qu'à partir de deux caractères
saisis, pour ne pas rendre les 6217 cartes.

- [ ] **Étape 4 : brancher Ctrl+Z et l'ouverture du catalogue**

Dans `ui-app/src/board/CoucheTriche.tsx`, dans l'écoute `keydown` du mode
manuel, avant l'appel à `interpreterTouche` :

```tsx
      if (evenement.ctrlKey && evenement.key.toLowerCase() === 'z') {
        evenement.preventDefault()
        void annulerDernierGeste().then((reussi) => {
          noter(reussi ? t('Dernier geste annulé') : t('Rien à annuler'))
        })
        return
      }
```

et une entrée « Faire apparaître une carte » dans le menu, qui ouvre
`<CatalogueManuel>`.

- [ ] **Étape 5 : traduire, vérifier, commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm test && npm run typecheck
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manuel/ ui-app/src/board/triche.ts \
        ui-app/src/board/CoucheTriche.tsx ui-app/src/board/dico-en.ts
git commit -m "feat(manuel): faire apparaitre une carte, et annuler un geste"
```

---

### Tâche 7 : la fin de partie et le journal de campagne

**Fichiers :**
- Créer : `ui-app/src/board/manuel/FinManuelle.tsx`
- Créer : `ui-app/src/board/manuel/FinManuelle.test.tsx`
- Modifier : `ui-app/src/board/CoucheTriche.tsx`
- Modifier : l'écran de fin de scénario de campagne, qui rend les cases `auto`
  en lecture seule.

**Interfaces :**
- Consomme : `envoyer` (`triche.ts`).
- Produit : `<FinManuelle onDeclarer={(gagne: boolean) => void} />`.
- Produit : `triche.declarerFin(gagne: boolean)`, qui envoie
  `Puzzle.End('victoire')` ou `Puzzle.End('defaite')`.

- [ ] **Étape 1 : écrire le test rouge**

Créer `ui-app/src/board/manuel/FinManuelle.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { FinManuelle } from './FinManuelle'

describe('declarer la fin d une partie manuelle', () => {
  it('propose victoire et defaite', () => {
    render(<FinManuelle onDeclarer={() => {}} />)
    expect(screen.getByText('Victoire')).toBeTruthy()
    expect(screen.getByText('Défaite')).toBeTruthy()
  })

  it('previent avant de declarer', () => {
    const declarer = vi.fn()
    render(<FinManuelle onDeclarer={declarer} />)
    fireEvent.click(screen.getByText('Victoire'))
    expect(declarer).not.toHaveBeenCalled()
    fireEvent.click(screen.getByText('Confirmer'))
    expect(declarer).toHaveBeenCalledWith(true)
  })
})
```

- [ ] **Étape 2 : lancer, voir ROUGE**

```bash
npm test -- src/board/manuel/FinManuelle.test.tsx
```

Attendu : ROUGE, module introuvable.

- [ ] **Étape 3 : écrire le panneau et le geste**

Dans `ui-app/src/board/triche.ts` :

```ts
/** Déclare la fin d'une partie manuelle. Le moteur ne surveille plus rien. */
export const declarerFin = (gagne: boolean) =>
  envoyer([`Puzzle.End(${texte(gagne ? 'victoire' : 'defaite')})`])
```

Écrire `FinManuelle.tsx` : deux boutons, puis une confirmation. La
confirmation n'est pas du zèle : une fin de partie déclarée par erreur ne se
reprend pas, et le Ctrl+Z ne la rattrape pas.

- [ ] **Étape 4 : ouvrir les cases `auto` du journal de campagne**

À l'écran de fin de scénario, quand `mode_manuel` est vrai, rendre saisissables
les cases dont le type est `auto` : le moteur n'est plus en mesure de les
constater. Ajouter une ligne d'aide qui le dit, pour qu'on ne cherche pas
pourquoi rien ne s'est rempli tout seul.

- [ ] **Étape 5 : vérifier et commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm test && npm run typecheck
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manuel/ ui-app/src/board/triche.ts \
        ui-app/src/board/CoucheTriche.tsx ui-app/src/board/dico-en.ts
git commit -m "feat(manuel): declarer la fin, et saisir le journal de campagne"
```

---

### Tâche 8 : la preuve à l'écran

**Fichiers :**
- Créer : `ui-check/tests/mode-manuel.spec.ts`

**Interfaces :**
- Consomme : tout ce qui précède.

⚠ Cette tâche **lance une partie sur le serveur de jeu**, comme
`ui-check/tests/glisser-plateau.spec.ts`. Elle se lance à la main, jamais dans
les captures, et **jamais pendant que quelqu'un joue**. Prévenir avant.

- [ ] **Étape 1 : écrire le test**

Créer `ui-check/tests/mode-manuel.spec.ts`, calqué sur
`glisser-plateau.spec.ts` : créer une partie manuelle (règle `mode_manuel` dans
la charge), attendre la table, puis vérifier, dans cet ordre :

1. aucun `.bandeau-phase`, aucun `.deroule-phase`, aucune demande centrale ;
2. le compteur de tour ne bouge pas après dix secondes ;
3. un glisser d'une carte de la main vers la défausse Rencontre la fait bien
   changer de pile ;
4. survoler le vilain et taper `3` lui pose trois dégâts ;
5. Ctrl+Z les lui retire.

- [ ] **Étape 2 : le lancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
npx playwright test tests/mode-manuel.spec.ts
```

Attendu : vert. Rappel du guide : Playwright tourne sous Windows, `WSLENV` doit
être posé.

- [ ] **Étape 3 : la capture**

Prendre une capture du plateau manuel réel et la ranger dans `ui-check/`.
C'est l'étape 8 bis de `PROCESSUS-CARTE.md` : un moteur vert ne prouve rien sur
le rendu.

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-check/tests/mode-manuel.spec.ts ui-check/mode-manuel.png
git commit -m "test(manuel): la preuve a l'ecran, du glisser au Ctrl+Z"
```

---

### Tâche 7 bis : le sélecteur de héros

**Ajoutée le 19/09/2026**, après une découverte de la tâche 2 : le plateau ne
construit qu'UNE zone « main », celle du joueur regardé (`zones.ts`, un seul
`emplacement('main', ...)` bâti sur `notre?.hand_cards`). La spec promettait
« toutes les mains visibles, puisqu'il n'y a qu'un opérateur » : c'est
structurellement impossible sans refondre le rendu.

**Décision de l'utilisateur** : une main à l'écran, et un sélecteur pour passer
d'un héros à l'autre.

**Fichiers :**
- Créer : `ui-app/src/board/manuel/SelecteurHeros.tsx` et son test
- Modifier : `ui-app/src/board.tsx` (poser `vueForcee` depuis le sélecteur)

**Interfaces :**
- Consomme : `estModeManuel` (tâche 1), `vueForcee` (`board.tsx:1629`), qui
  entre déjà dans le calcul du joueur regardé.
- Produit : `<SelecteurHeros joueurs={...} regarde={n} onRegarder={(n) => ...} />`

⚠ **Le mécanisme existe déjà, il lui manque un bouton.** En mode automatique,
la vue suit le joueur à qui le moteur pose une question (`etat.joueurDemande`).
En manuel il ne demande plus rien : la vue resterait figée sur le siège du
client. Ne pas inventer un second chemin de vue, poser `vueForcee`.

- [ ] **Étape 1 : écrire le test rouge**

Un composant qui liste les héros de la partie, marque celui qu'on regarde, et
appelle `onRegarder` avec le bon index au clic. Trois cas : la liste montre un
bouton par héros ; celui qu'on regarde est marqué ; un clic sur un autre appelle
`onRegarder` avec son index.

- [ ] **Étape 2 : le voir rouge, écrire le composant, le voir vert**

- [ ] **Étape 3 : le brancher**

Dans `board.tsx`, ne le rendre qu'en mode manuel et seulement s'il y a plus d'un
héros : à un seul héros, un sélecteur à une entrée n'apprend rien et prend de la
place.

- [ ] **Étape 4 : vérifier et commiter**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npm test && npm run typecheck
```

---

### Tâche 4 bis : les piles écartées du SCÉNARIO, atteignables

**Ajoutée le 19/09/2026**, sur un constat de la revue de la tâche 3, qui a lu le
dossier de la tâche 5 en vérifiant autre chose.

**Le défaut.** La table `PILE_PAR_ZONE` du dossier de la tâche 5 fait pointer
DEUX zones visuellement distinctes du plateau vers le même nom moteur
`'AsideDeck'` : « nemesis » (le set némésis du héros) et « set-aside-scenario »
(les cartes mises de côté par le scénario). Or côté moteur, `ZONES_MONDE`
(`game/puzzle/puzzle.py`) n'a AUCUNE entrée `AsideDeck` : `_ZoneParNom` retombe
donc sur `ZONES_JOUEUR['AsideDeck']`, c'est-à-dire le set némésis du héros.
Lâcher une carte sur « Mises de côté du scénario » l'enverrait silencieusement
dans le tas du héros. Pas d'erreur, pas de trace, une carte ailleurs.

C'est exactement ce que la table des piles devait empêcher, et c'est le
troisième cas de la même famille sur ce chantier.

**Le fond du problème.** `world.aside_deck` et `world.aside_modular`
(`game/world/world.py:84-85`) existent, portent bien `DeckType.AsideDeck`, et ne
sont atteignables par aucun geste manuel. Ce sont des zones que le mode manuel
promet de savoir remplir, puisqu'il promet que toute carte va dans toute pile.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/puzzle/puzzle.py` (`ZONES_MONDE`)
- Modifier : `Fusion/marvel-lcg-src/src/game/puzzle/puzzle_.py` (rien à changer,
  la signature de `MoveTo` ne bouge pas ; vérifier seulement)
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py` (un cas)

**Interfaces :**
- Produit : deux noms de zone nouveaux, `'AsideScenario'` (→ `w.aside_deck`) et
  `'AsideModular'` (→ `w.aside_modular`), consommés par la tâche 5.

⚠ **Ne renomme PAS `'AsideDeck'`**, qui désigne déjà la pile du joueur et qui
est utilisée. On ajoute, on ne déplace pas.

⚠ Le dossier de jeu jetable `.game-src-par8` a été supprimé à la fin du plan
moteur. Le recréer avant de lancer le harnais (voir la tâche 0 du plan
`2026-09-18-mode-manuel-moteur.md`), et le supprimer après.

- [ ] **Étape 1 : écrire le cas rouge**

Dans `tools/test_mode_manuel.py`, un cas qui envoie une carte vers
`'AsideScenario'` et vérifie qu'elle arrive dans `world.aside_deck`, ET
**qu'elle n'est PAS** dans le set némésis du héros. Le second contrôle est le
plus important : c'est lui qui prouve qu'on ne retombe pas sur la pile du
joueur, et c'est précisément le défaut qu'on répare.

- [ ] **Étape 2 : le voir rouge**

Attendu : la carte atterrit dans le set némésis du héros, ou `KeyError` sur une
zone inconnue.

- [ ] **Étape 3 : ajouter les deux entrées, le voir vert**

- [ ] **Étape 4 : relancer la batterie du harnais, puis commiter**

---

### Tâche 4 ter : un geste refusé doit se voir

**Ajoutée le 19/09/2026**, sur un signalement de la tâche 4 bis, et déjà
pressentie par la revue finale du plan moteur.

**Le défaut.** Quand un geste manuel échoue, rien ne le dit au joueur. La route
`/sandbox_command` répond « déposé » tout de suite, l'exécution a lieu plus tard
sur le fil du jeu, et l'erreur atterrit dans `device_manager.sandbox_last_error`
où personne ne va la chercher. Le joueur voit une table qui ne réagit pas, sans
savoir si son geste est parti, s'il a été refusé, ou si l'application est
figée.

Ça n'était pas critique tant que le mode manuel se prouvait au harnais. Ça le
devient maintenant : **le plateau est le seul moyen de jouer**, et la tâche 5
va multiplier les gestes refusables (lâcher une carte dans le vide, sur une
zone sans correspondance, sur une carte qui n'accepte pas d'attache).

C'est aussi une règle du projet : pas de repli silencieux.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/render/descriptor/world.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/to_descriptor.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py` (`ManualLoop`)
- Modifier : `ui-app/src/board/world.ts`, `ui-app/src/board/CoucheTriche.tsx`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Produit : `WorldDescriptor.manuel_refus: str`, vide quand tout va bien, et
  portant le motif du dernier geste refusé sinon.
- Produit, côté plateau : le refus s'affiche et entre au journal avec sa marque.

⚠ **Le piège est dans la boucle manuelle.** Elle ne redessine aujourd'hui que
lorsqu'un geste a été appliqué. Un geste REFUSÉ ne déclenche donc aucun rendu,
et le motif ne partirait jamais vers le plateau. Il faut redessiner aussi quand
le drain rend une liste vide mais qu'une erreur a été posée. C'est LE point de
cette tâche, le reste est du câblage.

⚠ **Le motif ne doit pas rester collé.** Une fois le refus publié et vu, le
champ doit repartir à vide, sinon le plateau affichera éternellement la même
erreur. Le moteur remet déjà `sandbox_last_error` à vide au drain suivant qui
réussit : vérifier que ça suffit, et le dire dans le rapport.

- [ ] **Étape 1 : le cas rouge, côté moteur**

Dans `tools/test_mode_manuel.py` : déposer un geste invalide (une zone inconnue),
et vérifier que le descripteur publié porte le motif du refus. Puis qu'un geste
valide qui suit le fait repartir à vide.

- [ ] **Étape 2 : le voir rouge, poser le champ et le rendu, le voir vert**

- [ ] **Étape 3 : côté plateau, le montrer**

Le refus entre au journal des interventions avec sa marque, comme les gestes
refusés le font déjà, et s'affiche brièvement à l'écran. Discret : ce n'est pas
une erreur de l'application, c'est une réponse à un geste.

- [ ] **Étape 4 : relancer les deux batteries, puis commiter**

---

### Tâche 8 bis : le silence commence avec la BOUCLE, pas avec la règle

**Ajoutée le 19/09/2026**, sur la découverte de la tâche 8, la seule qui ait
regardé l'écran.

**Le défaut, et il rend le mode inutilisable.** Une partie manuelle créée depuis
l'écran de préparation reste bloquée POUR TOUJOURS au premier mulligan. Le
moteur pose bien la question, comme décidé (mise en place intégrale, mulligan
compris), mais le plateau masque le panneau qui la pose. Le joueur est devant sa
première main sans rien à cliquer, et la partie ne démarrera jamais.

**La cause.** Le plateau masque les couches du moteur sur `estModeManuel`,
c'est-à-dire sur la RÈGLE. Or la règle est vraie dès la création de la partie,
mise en place comprise. Le moteur, lui, distingue deux choses :

- `rule.mode_manuel` : cette partie EST manuelle ;
- `world.manuel_actif` : le moteur S'EST TU, posé seulement à l'entrée de la
  boucle manuelle, après la mise en place.

Le plan moteur insistait sur cette distinction, et la trame ne publie pourtant
que la règle. Le plan plateau a donc masqué trop tôt.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/render/descriptor/world.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/to_descriptor.py`
- Modifier : `ui-app/src/board/world.ts`, `ui-app/src/board/manuel/mode.ts`
- Modifier : les appelants qui masquent ou activent (board.tsx, CoucheTriche)
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Produit : `WorldDescriptor.manuel_actif: bool`, faux pendant la mise en place,
  vrai dès que la boucle manuelle a pris la main.
- Produit : `leMoteurSeTait(world)` côté plateau, distinct de `estModeManuel`.

**Ce qui se règle sur quoi**, et c'est le cœur de la tâche :

- **Sur l'ÉTAT (`manuel_actif`)** : le masquage des couches du moteur, et les
  gestes manuels eux-mêmes (menu, clavier, glisser). Pendant la mise en place,
  la partie se comporte normalement : le joueur répond aux questions, il ne
  manipule pas encore la table.
- **Sur la RÈGLE (`mode_manuel`)** : ce qui décrit la NATURE de la partie et ne
  dépend pas du moment — le refus d'enregistrer un haut fait, la mention au
  rapport de bug, la saisie du journal de campagne.

⚠ **Le bouton « Fin du tour » reste affiché** en mode manuel, signalé par la
tâche 8 sans être testé. Même famille : à masquer avec le reste, et à couvrir.

- [ ] **Étape 1 : le cas rouge, côté moteur**

Le descripteur publié pendant la mise en place porte `manuel_actif` à faux, et
à vrai une fois la boucle manuelle entrée.

- [ ] **Étape 2 : publier le champ, le voir vert**

- [ ] **Étape 3 : le cas rouge, côté plateau**

Pendant la mise en place d'une partie manuelle, la demande centrale est VISIBLE.
Une fois le moteur tu, elle ne l'est plus. C'est le témoin qui prouve que le
mulligan est atteignable.

- [ ] **Étape 4 : basculer les appelants, le voir vert**

- [ ] **Étape 5 : le test de bout en bout doit le prouver aussi**

`ui-check/tests/mode-manuel.spec.ts` crée sa partie en contournant l'écran de
préparation. Il doit désormais passer par le même chemin qu'un joueur, mulligan
compris, sinon il continuera de ne pas voir ce défaut.

- [ ] **Étape 6 : relancer les deux batteries, puis commiter**
