// Lot 5 du 07/10/2026 : multi-selection du mode manuel, comme OCTGN.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import * as triche from '../triche'
import { MenuTriche } from '../MenuTriche'
import { cartesDuGeste, selection } from './selection'
import { cartesDansLeRectangle } from './CoucheSelection'
import { ecran as screen } from '../../test-textes'

afterEach(() => {
  selection.vider()
  vi.unstubAllGlobals()
  document.body.innerHTML = ''
})

describe('la selection', () => {
  it('Ctrl+clic ajoute puis retire', () => {
    selection.basculer(4)
    selection.basculer(5)
    expect([...selection.lire()]).toEqual([4, 5])
    selection.basculer(4)
    expect([...selection.lire()]).toEqual([5])
  })
  it('un geste sur une carte selectionnee vaut pour toute la selection, sinon pour elle seule', () => {
    selection.remplacer([4, 5, 6])
    expect(cartesDuGeste(5)).toEqual([4, 5, 6])
    expect(cartesDuGeste(9)).toEqual([9])
    selection.remplacer([4])
    expect(cartesDuGeste(4)).toEqual([4])
  })
})

describe('le rectangle', () => {
  it('prend les cartes de la table qu il touche, ni la main ni les piles', () => {
    document.body.innerHTML = `
      <div class="plateau-scene">
        <div class="plateau-unite"><div class="scan-card" data-card-id="1"></div></div>
        <div class="plateau-unite"><div class="scan-card" data-card-id="2"></div></div>
        <div class="plateau-unite" data-pile="deck"><div class="scan-card" data-card-id="3"></div></div>
        <section class="zone-main"><div class="plateau-unite"><div class="scan-card" data-card-id="4"></div></div></section>
      </div>`
    const poser = (id: string, left: number) => {
      ;(document.querySelector(`[data-card-id="${id}"]`) as HTMLElement).getBoundingClientRect = () =>
        ({ left, right: left + 100, top: 0, bottom: 100, width: 100, height: 100 }) as DOMRect
    }
    poser('1', 0)
    poser('2', 300)
    poser('3', 50)
    poser('4', 60)
    expect(cartesDansLeRectangle({ gauche: 10, haut: 10, droite: 150, bas: 50 })).toEqual([1])
  })
})

describe('un lot = une seule commande (un seul Ctrl+Z)', () => {
  it('les commandes de plusieurs cartes partent jointes, en un seul envoi', async () => {
    const fetchMock = vi.fn(async () => ({ ok: true }) as Response)
    vi.stubGlobal('fetch', fetchMock)
    await triche.enLot([() => triche.incliner(4), () => triche.incliner(5), () => triche.blesser(6, 1)])
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const corps = JSON.parse((fetchMock.mock.calls[0] as unknown as [string, RequestInit])[1].body as string)
    expect(corps.commands).toEqual(['Puzzle.Exhaust(4)\nPuzzle.Exhaust(5)\nPuzzle.Damage(6, 1)'])
  })

  it('le menu d une carte selectionnee agit sur toute la selection', async () => {
    const fetchMock = vi.fn(async () => ({ ok: true }) as Response)
    vi.stubGlobal('fetch', fetchMock)
    const emettreGeste = vi.fn(async (_libelle: string, deposer: () => Promise<boolean>) => {
      await deposer()
    })
    render(
      <MenuTriche
        cible={{ id: 4, nom: 'Black Cat', estManigance: false, estPersonnage: true }}
        x={0}
        y={0}
        onFermer={() => {}}
        emettreGeste={emettreGeste}
        manuel
        ids={[4, 5]}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: /^Incliner$/ }))
    await vi.waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
    expect(emettreGeste.mock.calls[0][0]).toContain('×2')
    const corps = JSON.parse((fetchMock.mock.calls[0] as unknown as [string, RequestInit])[1].body as string)
    expect(corps.commands).toEqual(['Puzzle.Exhaust(4)\nPuzzle.Exhaust(5)'])
  })
})
