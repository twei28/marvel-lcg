// CoucheTriche.test.tsx — le bandeau et la pile, isolés du plateau entier.
//
// Le crochet `useTriche` a besoin d'un monde complet ; ces tests visent
// directement le composant `<CoucheTriche>`, en lui fournissant une `couche`
// construite à la main. C'est ce que `useTriche` lui donnerait de toute
// façon : `{ menu, pile, setMenu, setPile, noter }`.
import { act, fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from './CoucheTriche'
import { siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

function coucheVide() {
  return {
    menu: undefined,
    pile: undefined,
    setMenu: vi.fn(),
    setPile: vi.fn(),
    noter: vi.fn(),
    avisRefus: undefined,
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
    const couche = { ...coucheVide(), avisRefus: 'Geste refusé par la table' }
    const { container, getByText } = render(<CoucheTriche actif manuel couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).not.toBeNull()
    expect(getByText('Geste refusé par la table')).toBeTruthy()
  })

  it('reste masqué hors mode manuel, même avec un avis posé', () => {
    // Défensif : `useTriche` ne pose `avisRefus` qu'en mode manuel, mais le
    // composant ne doit pas dépendre de cette seule discipline de l'appelant.
    const couche = { ...coucheVide(), avisRefus: 'Geste refusé par la table' }
    const { container } = render(<CoucheTriche actif manuel={false} couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
  })
})

// Harnais calqué sur board/manuel/clavier-wiring.test.tsx : `useTriche` a
// besoin d'un monde complet pour observer son effet sur `render_id` et
// `manuel_refus`, pas d'une `couche` construite à la main.
function Harness({ world, ajouterAuJournal }: { world: World; ajouterAuJournal?: (l: string) => void }) {
  const triche = useTriche(world, 0, ajouterAuJournal)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

describe('un geste manuel refusé se voit (tâche 4 ter)', () => {
  it('inscrit un avis au journal et l’affiche quand un nouveau rendu porte un refus', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = tableAvec(siege(), { mode_manuel: true, render_id: 1, manuel_refus: '' } as never)
    const { container, rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const refuse = {
      ...avant,
      render_id: 2,
      manuel_refus: "KeyError: 'zone inconnue : ZoneInconnue'",
    } as World
    await act(async () => {
      rerender(<Harness world={refuse} ajouterAuJournal={ajouterAuJournal} />)
    })

    expect(container.querySelector('.avis-refus-manuel')).not.toBeNull()
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Geste refusé par la table')
    // Le motif TECHNIQUE ne s'affiche jamais tel quel : il s'adresse à qui
    // débogue, pas à qui joue.
    expect(container.textContent).not.toContain('KeyError')
    expect(container.textContent).not.toContain('ZoneInconnue')
  })

  it('ne rejoue pas le même refus sur un rendu qui ne change rien', async () => {
    const ajouterAuJournal = vi.fn()
    const refuse = tableAvec(siege(), {
      mode_manuel: true,
      render_id: 5,
      manuel_refus: "KeyError: 'zone inconnue : X'",
    } as never)
    const { rerender } = render(<Harness world={refuse} ajouterAuJournal={ajouterAuJournal} />)
    await act(async () => { await Promise.resolve() })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)

    // Même `render_id`, même refus : un second rendu React (pas un nouveau
    // rendu MOTEUR) ne doit pas re-signaler le même événement.
    await act(async () => {
      rerender(<Harness world={{ ...refuse }} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
  })

  it('ne se déclenche jamais en bac à sable, seulement en mode manuel', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = tableAvec(siege(), {
      mode_manuel: false,
      mode_sandbox: true,
      render_id: 1,
      manuel_refus: '',
    } as never)
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    const refuse = { ...avant, render_id: 2, manuel_refus: "KeyError: 'zone inconnue : X'" } as World
    await act(async () => {
      rerender(<Harness world={refuse} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).not.toHaveBeenCalled()
  })
})
