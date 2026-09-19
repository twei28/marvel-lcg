// CoucheTriche.test.tsx — le bandeau et la pile, isolés du plateau entier.
//
// Le crochet `useTriche` a besoin d'un monde complet ; ces tests visent
// directement le composant `<CoucheTriche>`, en lui fournissant une `couche`
// construite à la main. C'est ce que `useTriche` lui donnerait de toute
// façon : `{ menu, pile, setMenu, setPile, noter }`.
import { fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche } from './CoucheTriche'
import type { WorldCard } from './world'

function coucheVide() {
  return { menu: undefined, pile: undefined, setMenu: vi.fn(), setPile: vi.fn(), noter: vi.fn() }
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
