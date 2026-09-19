// CoucheTriche.test.tsx — le bandeau, la pile et la résolution différée d'un
// geste, isolés du plateau entier.
//
// Le crochet `useTriche` a besoin d'un monde complet ; les tests du bandeau et
// de la pile visent directement le composant `<CoucheTriche>`, avec une
// `couche` construite à la main. C'est ce que `useTriche` lui donnerait de
// toute façon : `{ menu, pile, setMenu, setPile, emettreGeste, avisRefus }`.
// Les tests de résolution (plus bas) ont besoin du VRAI `useTriche`, sur le
// modèle de `board/manuel/clavier-wiring.test.tsx`.
import { act, fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from './CoucheTriche'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

function coucheVide() {
  return {
    menu: undefined,
    pile: undefined,
    setMenu: vi.fn(),
    setPile: vi.fn(),
    // Appelle vraiment le déposeur, comme le ferait le `emettreGeste` réel de
    // `useTriche` : sans ça, `triche.melanger` ne serait jamais invoqué dans
    // le test « la pile ouverte propose de la mélanger » plus bas, et `fetch`
    // ne verrait jamais passer la commande.
    emettreGeste: vi.fn(async (_libelle: string, deposer: () => Promise<boolean>) => {
      await deposer()
    }),
    avisRefus: undefined as string | undefined,
  }
}

const CARTE: WorldCard = { id: 1, name: 'Carte test', card_type: 'Ally' } as WorldCard

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})

describe('le bandeau ne dénonce que le bac à sable', () => {
  it('s’affiche en bac à sable', () => {
    const { container } = render(<CoucheTriche actif manuel={false} couche={coucheVide()} />)
    expect(container.querySelector('.bandeau-triche')).not.toBeNull()
  })

  it('ne s’affiche pas en mode manuel : il n’y a rien à dénoncer', () => {
    const { container } = render(<CoucheTriche actif manuel couche={coucheVide()} />)
    expect(container.querySelector('.bandeau-triche')).toBeNull()
  })
})

describe('la pile ouverte propose de la mélanger', () => {
  it('mélange la pile visée quand on clique dessus', async () => {
    const couche = {
      ...coucheVide(),
      pile: { titre: 'Deck Rencontre', cartes: [CARTE], duJoueur: false, zone: 'EncounterDeck' },
    }
    const { getByText } = render(<CoucheTriche actif manuel couche={couche} />)
    fireEvent.click(getByText('Mélanger'))
    await Promise.resolve()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('EncounterDeck')"] }),
    }))
  })
})

describe('l’avis de refus ne se montre qu’en mode manuel', () => {
  it('reste invisible sans avis à montrer', () => {
    const { container } = render(<CoucheTriche actif manuel couche={coucheVide()} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
  })

  it('s’affiche quand un avis est posé, en mode manuel', () => {
    const couche = { ...coucheVide(), avisRefus: 'Retourner — Rhino (refusé)' }
    const { container, getByText } = render(<CoucheTriche actif manuel couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).not.toBeNull()
    expect(getByText('Retourner — Rhino (refusé)')).toBeTruthy()
  })

  it('reste masqué hors mode manuel, même avec un avis posé', () => {
    // Défensif : `useTriche` ne pose `avisRefus` qu'en mode manuel, mais le
    // composant ne doit pas dépendre de cette seule discipline de l'appelant.
    const couche = { ...coucheVide(), avisRefus: 'Retourner — Rhino (refusé)' }
    const { container } = render(<CoucheTriche actif manuel={false} couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
  })
})

// --- La résolution différée d'un geste (correction du 19/09/2026) ---------
//
// ÉCART CORRIGÉ : la version d'origine de la tâche 4 ter écrivait la ligne du
// geste tout de suite (sur le succès du DÉPÔT HTTP), et une ligne GÉNÉRIQUE
// séparée quand le moteur refusait plus tard — deux lignes qui pouvaient se
// contredire, sans dire quel geste était visé. Ici, la ligne n'est écrite
// qu'une fois, au rendu qui connaît l'issue réelle.
//
// Harnais calqué sur board/manuel/clavier-wiring.test.tsx : `useTriche` a
// besoin d'un monde complet pour observer son effet sur `render_id` et
// `manuel_refus`, pas d'une `couche` construite à la main.
const VILAIN = carteSurTable(7, '01001a', 'EncounterVillain', 'Rhino')
const AUTRE = carteSurTable(8, '01002a', 'EncounterVillain', 'Klaw')

function mondeManuel(surcharge: Partial<World> = {}): World {
  return tableAvec(siege(), {
    mode_manuel: true,
    render_id: 1,
    manuel_refus: '',
    villains: [VILAIN, AUTRE],
    ...surcharge,
  } as never)
}

function Harness({ world, ajouterAuJournal }: { world: World; ajouterAuJournal?: (l: string) => void }) {
  const triche = useTriche(world, 0, ajouterAuJournal)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

function survoler(id: number): void {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  fireEvent.pointerMove(noeud)
}

/** Laisse toutes les promesses en chaîne (fetch, triche.ts, emettreGeste) se résoudre. */
const attendreLeReseau = () => act(() => new Promise((resolve) => setTimeout(resolve, 0)))

describe('un geste manuel refusé se voit, sans jamais dire l’inverse (correction du 19/09/2026)', () => {
  it('n’écrit rien tant que l’issue n’est pas connue', async () => {
    const ajouterAuJournal = vi.fn()
    render(<Harness world={mondeManuel()} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalled()
    expect(ajouterAuJournal).not.toHaveBeenCalled()
  })

  it('écrit la ligne SANS marque quand le rendu suivant dit que le geste est passé', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino')
  })

  it('écrit la ligne AVEC sa marque quand le moteur refuse — jamais l’inverse, jamais deux lignes', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { container, rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()

    const suivant = {
      ...avant,
      render_id: 2,
      manuel_refus: "KeyError: 'zone inconnue : ZoneInconnue'",
    } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })

    // UNE SEULE ligne — jamais la ligne « faite » d'abord, puis une ligne de
    // refus générique ensuite (c'est exactement le défaut corrigé).
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (refusé)')
    expect(container.textContent).toContain('Retourner — Rhino (refusé)')
    // Le motif technique ne s'affiche jamais tel quel.
    expect(container.textContent).not.toContain('KeyError')
    expect(container.textContent).not.toContain('ZoneInconnue')
  })

  it('un dépôt qui échoue (réseau) reste immédiat : aucun rendu futur ne le concernera jamais', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false }) as Response))
    const ajouterAuJournal = vi.fn()
    render(<Harness world={mondeManuel()} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (refusé)')
  })

  it('ne devine pas quand deux gestes sont en vol au même rendu : issue inconnue pour chacun', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    survoler(7)
    fireEvent.keyDown(document, { key: 'f' }) // Retourner — Rhino
    survoler(8)
    fireEvent.keyDown(document, { key: 'q' }) // Incliner — Klaw
    await attendreLeReseau()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })

    // Un seul drainage moteur peut regrouper les deux commandes : impossible
    // de savoir laquelle a réussi. Ni succès ni refus inventés.
    expect(ajouterAuJournal).toHaveBeenCalledTimes(2)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (issue inconnue)')
    expect(ajouterAuJournal).toHaveBeenCalledWith('Incliner — Klaw (issue inconnue)')
  })

  it('ignore un rendu qui ne concerne aucun geste en attente (par ex. un autre joueur)', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    const suivant = { ...avant, render_id: 2, manuel_refus: "KeyError: 'zone inconnue : X'" } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).not.toHaveBeenCalled()
  })

  it('ne rejoue rien sur un rendu React qui ne change pas render_id', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)

    // Même `render_id` : un second rendu React (pas un nouveau rendu moteur)
    // ne doit rien rejouer.
    await act(async () => {
      rerender(<Harness world={{ ...suivant }} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
  })
})
